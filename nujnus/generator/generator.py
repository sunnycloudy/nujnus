import os

# import yaml
from nujnus.common.error import NujnusError
from nujnus.common.utils import (
    create_dir,
    overwrite,
    check_directory_exists,
)
from nujnus.common.ruamel_yaml_config import yaml
from io import StringIO


def get_absolute_path(relative_path):
    # 获取相对路径的绝对路径
    absolute_path = os.path.abspath(relative_path)
    return absolute_path


def generate_ansible_inventory_command(generated_path, commands, namespace):
    """
    调用 ansible-inventory 来显示变量
    """

    # 在命令列表中查找匹配的命令和命名空间
    for command in commands:

        if "namespace" in command and command["namespace"] == namespace:
            check_directory_exists(command["workdir"])
            # 构建ansible-playbook命令的参数列表
            ansible_command = [
                "ansible-inventory",
                "-i",
                command["inventory"],
                "--list",
            ]

            # 指定环境变量
            env = os.environ.copy()
            if "roles_path" in command:
                env["ANSIBLE_ROLES_PATH"] = "{}".format(command["roles_path"])

            if "log_path" in command:
                log_path = command["log_path"]
                abs_log_path = os.path.abspath(log_path)
                os.makedirs(os.path.dirname(abs_log_path), exist_ok=True)
                env["ANSIBLE_LOG_PATH"] = "{}".format(abs_log_path)
                print(abs_log_path)

            if "cfg" in command:
                env["ANSIBLE_CONFIG"] = "{}".format(command["cfg"])
            # known_hosts_abs_path = get_absolute_path("./secrets/known_hosts")
            # ansible_command.append(
            #    "--ssh-common-args='-o UserKnownHostsFile={}'".format(
            #        known_hosts_abs_path
            #    )
            # )
            if "overwrite" in command:
                if command["overwrite"] == True:

                    source_file_path = "{}/{}/inventory.ini".format(
                        generated_path, command["namespace"]
                    )
                    destination_file_path = command["inventory"]

                    overwrite(source_file_path, destination_file_path)

            return ansible_command, command["workdir"], env
            # 如果没有找到匹配的命令
    raise NujnusError(message=f"No command found with namespace {namespace}")


def generate_ansible_command(generated_path, command):
    # 在命令列表中查找匹配的命令和命名空间
    check_directory_exists(command.workdir)
    # 构建ansible-playbook命令的参数列表
    ansible_command = [
        "ansible-playbook",
        "--become",
        "-i",
        command.inventory,
        command.playbook,
    ]

    # 指定环境变量
    env = os.environ.copy()
    if command.roles_path:
        env["ANSIBLE_ROLES_PATH"] = "{}".format(command.roles_path)

    if command.log_path:
        log_path = command.log_path
        abs_log_path = os.path.join(os.path.abspath(command.workdir), log_path)
        os.makedirs(os.path.dirname(abs_log_path), exist_ok=True)
        env["ANSIBLE_LOG_PATH"] = "{}".format(abs_log_path)

    if command.cfg:
        env["ANSIBLE_CONFIG"] = "{}".format(command.cfg)

    env["BREAK_LIST_FILE_PATH"] = get_absolute_path(
        "{}/{}/breaklist.yml".format(generated_path, command.namespace)
    )

    # 如果有额外的args参数，将它们添加到命令中
    if command.args:
        ansible_command.extend(command.args)

    known_hosts_abs_path = get_absolute_path("./secrets/known_hosts")
    ansible_command.append(
        "--ssh-common-args='-o UserKnownHostsFile={}'".format(known_hosts_abs_path)
    )

    if command.overwrite == True:
        ## 定义源文件和目标文件的路径
        # 示例用法
        # source_directory = "./secrets"
        # destination_directory = command["workdir"]
        # copy_directory_to_inside(source_directory, destination_directory)

        # 1.改成使用nujnus当前位置的known_hosts文件
        # 2.改成使用绝对路径的ssh_key

        source_file_path = "{}/{}/inventory.ini".format(
            generated_path, command.namespace
        )
        destination_file_path = os.path.join(
            os.path.abspath(command.workdir), command.inventory
        )

        overwrite(source_file_path, destination_file_path)
    return ansible_command, command.workdir, env


def generate_inventory(generated_path, namespace):

    absolute_base_path = os.path.abspath(".")
    # 创建命名空间目录
    path = create_dir(generated_path, namespace.name)

    # 创建 host_vars 和 group_vars 目录
    host_vars_dir = os.path.join(path, "host_vars")
    group_vars_dir = os.path.join(path, "group_vars")
    os.makedirs(host_vars_dir, exist_ok=True)
    os.makedirs(group_vars_dir, exist_ok=True)

    if "all" in namespace.groups:
        for node in namespace.groups["all"].nodes:
            host_vars_file_path = os.path.join(host_vars_dir, f"{node.name}.yml")
            # if not os.path.exists(host_vars_file_path):
            with open(host_vars_file_path, "w") as host_vars_file:
                host_vars_file.write(f"# Variables for host {node.name}\n")
                # host_vars_file.write(yaml.dump(vars, allow_unicode=True))
                if namespace.name in node.namespace_vars_map.keys():
                    # 创建一个输出流
                    output = StringIO()
                    yaml.dump(node.namespace_vars_map[namespace.name], output)
                    # 从流中获取输出结果
                    output_str = output.getvalue()
                    host_vars_file.write(output_str)

    for name, group in namespace.groups.items():
        # 为每个 group 创建变量文件
        group_vars_file_path = os.path.join(group_vars_dir, f"{name}.yml")
        with open(group_vars_file_path, "w") as group_vars_file:
            group_vars_file.write(f"# Variables for group {name}\n")
            # 创建一个输出流
            output = StringIO()
            yaml.dump(group.vars, output)
            # 从流中获取输出结果
            output_str = output.getvalue()
            group_vars_file.write(output_str)

    inventory_path = os.path.join(path, "inventory.ini")
    with open(inventory_path, "w") as f:

        if namespace.before_text:
            f.write(namespace.before_text)

        # 遍历各个group:
        for name, group in namespace.groups.items():
            if name == "all":
                # 写入all_group
                f.write(f"[all]\n")
                for server in group.nodes:
                    if server.password != None and server.password != "":
                        # print(server.password)
                        server_info = f"{server.name} ansible_host={server.ip} ansible_user={server.username} ansible_ssh_private_key_file={get_absolute_path(server.sshkey)} ansible_sudo_pass={server.password}"
                    else:
                        server_info = f"{server.name} ansible_host={server.ip} ansible_user={server.username} ansible_ssh_private_key_file={get_absolute_path(server.sshkey)}"
                    for key, value in server.inivars.items():
                        server_info += f" {key}={value} "
                    f.write(server_info)
                    f.write("\n")
                f.write("\n")

            else:
                f.write(f"[{name}]\n")
                for server in group.nodes:
                    f.write(f"{server.name}\n")  # 其他组仅写入名称
                # 为每个 group 创建变量文件
                f.write(f"\n")

        if namespace.after_text:
            f.write(namespace.after_text)

    debug_cfg = os.path.join(path, "debug.cfg")
    if not os.path.exists(debug_cfg):
        with open(debug_cfg, "w") as debug_cfg_file:
            debug_cfg_file.write(
                """
    [defaults]
    callback_plugins = {}/plugins
    callbacks_enabled = nujnus_debug
                """.format(
                    absolute_base_path
                )
            )


def generate_inventories(generated_path, namespace_list):

    for namespace in namespace_list:
        generate_inventory(generated_path, namespace)


def generate_ssh_config(node_list):
    # 初始化ssh_config字符串
    ssh_config = ""

    # 遍历每个服务器配置
    for server in node_list:
        # 服务器基础配置
        ssh_config += f"Host {server.name}\n"
        ssh_config += f"    HostName {server.ip}\n"
        ssh_config += f"    User {server.username}\n"
        ssh_config += (
            f"    IdentityFile ~/.nujnus/secrets/id_rsa\n"  # 修正sshkey路径为相对路径
        )
        ssh_config += f"    UserKnownHostsFile ~/.nujnus/secrets/known_hosts\n\n"

    return ssh_config
