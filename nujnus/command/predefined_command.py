# 在Python中，ABC是Abstract Base Classes的缩写，它是Python的abc模块中的一个特殊类。Abstract Base Classes（抽象基类）用于创建一个基础框架，允许你定义一些方法和属性，这些方法和属性在子类中必须被实现或定义。这有助于确保子类遵循特定的接口或实现特定的行为。
#
# 使用抽象基类可以做到以下几点：
#
# 强制子类实现特定的方法。如果子类没有实现所有的抽象方法，那么在尝试实例化该子类时，Python将抛出TypeError。
# 提供共享的代码实现。抽象基类可以提供一些方法的实现，子类可以直接使用或覆盖这些实现。
# 作为一种类型检查工具。你可以检查某个实例是否实现了特定的抽象基类，这在需要确保某个对象支持特定接口或方法时非常有用。
# 在Python中使用abc.ABC创建抽象基类的一个简单例子如下：
import click
import uuid
import subprocess
from nujnus.common.utils import *
from nujnus.generator.generator import (
    generate_inventories,
    generate_ssh_config,
    generate_ansible_command,
    generate_ansible_inventory_command,
)
from nujnus.generator.templates import *
from nujnus.yml_parser.commands_yml_parser import load_commands_from_yaml
from nujnus.version import __version__
from nujnus.command.base_command import *
from nujnus.node.node import *
from nujnus.common.helper import *
from nujnus.command.customized_command import *


# ------------------------------------------------
#
#  通用的
#
# ------------------------------------------------


class Tree(NujnusCommand):
    def execute_command(self):
        Node.print_node_tree()


class Ls(NujnusCommand):
    def execute_command(self):
        Node.print_node_plain()


class Hosts(NujnusCommand):

    def execute_command(self):

        hosts_content = Node.generate_hosts_file_content()

        with open("secrets/hosts", "w", encoding="utf-8") as file:
            file.write(hosts_content)

        click.echo(hosts_content)
        # 打印结果或进行其他处理
        click.echo("Hosts file 已经被保存在: /secrets/hosts文件中.")


class Role(NujnusCommand):

    def __init__(self, rolename) -> None:
        super().__init__()
        self.rolename = rolename

    def execute_command(self):
        """
        ├── README.md
        ├── defaults
        │   └── main.yml
        ├── files
        ├── handlers
        │   └── main.yml
        ├── meta
        │   └── main.yml
        ├── tasks
        │   └── main.yml
        ├── templates
        ├── tests
        │   ├── inventory
        │   └── test.yml
        └── vars
            └── main.yml
        """

        check_file_exists_in_current_directory("nujnus.yml")
        playbook_base_path = create_dir(".", "playbooks")
        check_directory_exists(playbook_base_path)

        create_file_if_notexist(
            playbook_base_path,
            "{}.yml".format(self.rolename),
            playbook_template.format(self.rolename),
        )

        # 生成command的脚手架
        absolute_base_path = os.path.abspath(".")
        append_file(
            ".",
            "commands.draft",
            commands_draft_content.format(
                rolename=self.rolename, project_base=absolute_base_path
            ),
        )

        roles_base_path = create_dir(".", "roles")
        role_dir = os.path.join(roles_base_path, self.rolename)
        check_directory_exists(role_dir)

        role_dir = create_dir(roles_base_path, self.rolename)

        def generate_role(
            role_dir,
            reamde_template="",
            defaults_main_template="",
            vars_main_template="",
            meta_main_template="",
            tasks_main_template="",
            verifications_main_template="",
            # verifications_install_template="",
            handlers_main_template="",
            # tasks_install_template="",
            # tasks_uninstall_template="",
            # tasks_backup_template="",
            # tasks_restore_template="",
            # tasks_start_template="",
            # tasks_stop_template="",
            # tasks_enable_template="",
            # tasks_disable_template="",
            # verifications_uninstall_template="",
            # verifications_backup_template="",
            # verifications_restore_template="",
            # verifications_start_template="",
            # verifications_stop_template="",
            # verifications_disable_template="",
            # verifications_enable_template="",
        ):
            create_file(role_dir, "README.md", reamde_template)
            # 变量和元数据:
            defaults_dir = create_dir(role_dir, "defaults")
            create_file(defaults_dir, "main.yml", defaults_main_template)
            vars_dir = create_dir(role_dir, "vars")
            create_file(vars_dir, "main.yml", vars_main_template)
            meta_dir = create_dir(role_dir, "meta")
            create_file(meta_dir, "main.yml", meta_main_template)

            # tasks:
            tasks_path = create_dir(role_dir, "tasks")
            create_file(tasks_path, "main.yml", tasks_main_template)
            # create_file(tasks_path, "install.yml", tasks_install_template)
            # create_file(tasks_path, "uninstall.yml", tasks_uninstall_template)
            # create_file(tasks_path, "stop.yml", tasks_stop_template)
            # create_file(tasks_path, "start.yml", tasks_start_template)
            # create_file(tasks_path, "enable.yml", tasks_enable_template)
            # create_file(tasks_path, "disable.yml", tasks_disable_template)
            # create_file(tasks_path, "backup.yml", tasks_backup_template)
            # create_file(tasks_path, "restore.yml", tasks_restore_template)

            # 测试文件:
            verifications_path = create_dir(role_dir, "verifications")
            create_file(verifications_path, "main.yml", verifications_main_template)
            # create_file(
            #    verifications_path, "install.yml", verifications_install_template
            # )
            # create_file(
            #    verifications_path, "uninstall.yml", verifications_uninstall_template
            # )
            # create_file(verifications_path, "backup.yml", verifications_backup_template)
            # create_file(
            #    verifications_path, "restore.yml", verifications_restore_template
            # )
            # create_file(verifications_path, "start.yml", verifications_start_template)
            # create_file(verifications_path, "stop.yml", verifications_stop_template)
            # create_file(
            #    verifications_path, "disable.yml", verifications_disable_template
            # )
            # create_file(verifications_path, "enable.yml", verifications_enable_template)

            # 回调任务:
            handler_path = create_dir(role_dir, "handlers")
            create_file(handler_path, "main.yml", handlers_main_template)

        if self.rolename == "demo":
            generate_role(
                role_dir=role_dir,
                defaults_main_template=defaults_demo,
                vars_main_template=vars_demo,
                tasks_main_template=tasks_demo,
                handlers_main_template=handlers_demo,
            )
            # 文件:
            files_dir = create_dir(role_dir, "files")
            create_file(files_dir, "example.py", file_demo)
            templates_dir = create_dir(role_dir, "templates")
            create_file(templates_dir, "script_config.j2", template_demo)

        if self.rolename == "print_vars":
            generate_role(
                role_dir=role_dir,
                defaults_main_template="",
                vars_main_template="",
                tasks_main_template=print_vars_demo,
                handlers_main_template="",
            )
            # 文件:
            files_dir = create_dir(role_dir, "files")
            templates_dir = create_dir(role_dir, "templates")

        else:
            generate_role(role_dir=role_dir)
            # 文件:
            create_dir(role_dir, "files")
            create_dir(role_dir, "templates")

        # 提示:
        click.echo(f" ./roles/")
        click.echo(f"    └─ {self.rolename}/")
        click.echo(f"{self.rolename}目录结构生成完毕")


class Init(NujnusCommand):

    def execute_command(self):
        self.create_uuid_dir()

    # 用python写一个函数, 用来生成一个uuid, 然后以这个uuid为名创建一个目录

    # 用python写一个函数创建如下目录和文件:
    # uuid/           #
    #     ├── nujnus.yml    #环境配置
    #     ├── files/         #ansible任务需要的文件
    #     ├── templates/     #ansible任务需要的模版
    #     ├── vars/          #ansible任务需要的变量
    #     ├── playbooks/     #自定义ansible任务
    #     ├── verifications/ #自定义ansible用于验证的任务
    #       ├── example.yml  #自定义脚本
    #     ├── roles/         #ansible角色脚本
    #     ├── generated/     #nujnus存放其他生成内容的目录
    #     ├── logs/          #所有的执行日志

    def create_uuid_dir(self):
        # Generate a UUID
        unique_id = str(uuid.uuid4())
        # Create a directory with the UUID as its name
        os.makedirs(unique_id)

        base_path = unique_id
        create_file(
            base_path=base_path, filename="nujnus.yml", content=nujnus_yml_content
        )
        create_file(
            base_path=base_path, filename="commands.yml", content=commands_yml_content
        )
        create_file(
            base_path=base_path, filename=".gitignore", content=gitignore_content
        )
        create_dir(base_path, "roles")
        create_dir(base_path, Namespace.generated_path())
        # create_dir(base_path, "files")
        # create_dir(base_path, "templates")
        # create_dir(base_path, "vars")
        playbooks_path = create_dir(base_path, "playbooks")
        create_file(
            base_path=playbooks_path, filename="example.yml", content=example_yml
        )
        verifications_path = create_dir(base_path, "verifications")
        create_file(
            base_path=verifications_path,
            filename="example.yml",
            content=verify_yml_content,
        )
        create_dir(base_path, "logs")
        self.create_rsa_and_known_hosts(base_path)
        click.echo(f"Directory named {unique_id} has been created.")

    def create_rsa_and_known_hosts(self, base_path):
        # 定义secrets目录的路径
        secrets_dir = os.path.join(base_path, "secrets")

        # 如果secrets目录不存在，则创建它
        if not os.path.exists(secrets_dir):
            os.makedirs(secrets_dir)

        # 定义RSA密钥对和known_hosts文件在secrets目录中的路径
        rsa_key_path = os.path.join(secrets_dir, "id_rsa")
        known_hosts_path = os.path.join(secrets_dir, "known_hosts")

        # 使用ssh-keygen命令生成RSA密钥对
        # '-f' 参数指定密钥文件的路径
        # '-t' 参数指定密钥类型，这里使用'rsa'
        # '-N' 参数后跟空字符串''，表示生成密钥时不设置密码
        subprocess.run(
            ["ssh-keygen", "-f", rsa_key_path, "-t", "rsa", "-N", ""], check=True
        )

        # 创建一个空的known_hosts文件
        open(known_hosts_path, "a").close()

        # print(f"RSA密钥路径: {rsa_key_path}")
        # print(f"known_hosts文件路径: {known_hosts_path}")


class SshConfig(NujnusCommand):

    def execute_command(self):
        ssh_config = generate_ssh_config(node_list=Node.get_all_nodes())

        # 将转换后的内容保存到指定的输出文件
        with open("secrets/ssh_config", "w", encoding="utf-8") as file:
            file.write(ssh_config)
        click.echo(ssh_config)
        click.echo(
            "ssh_cofnig已经保存在./secrets/ssh_config中,  复制整个secrets目录到本地~/.nujnus目录下"
        )


class Version(NujnusCommand):
    pass


class Login(NodeCommand):

    def execute_command(self):
        click.echo("Logging2 in...")

        try:
            self.node.ssh_login(
                path_to_known_hosts="./secrets/known_hosts",
            )
        except subprocess.CalledProcessError as e:
            click.echo(f"SSH连接失败: {e}")


class Get(FileCommand):

    def execute_command(self):

        try:
            create_dir("./", "downloads")
            self.node.get_file(
                file_path=self.file_path,
                local_path="./downloads",
                path_to_known_hosts="./secrets/known_hosts",
            )
        except subprocess.CalledProcessError as e:
            click.echo(f"SSH连接失败: {e}")


class Scan(NujnusCommand):

    def execute_command(self):
        click.echo("Scanning...")

        try:
            Node.scan()
            click.echo(f"已经更新./secrets/known_hosts")
        except subprocess.CalledProcessError as e:
            click.echo(f"Scan时出错: {e}")


class Sendkey(NodeCommand):

    def execute_command(self):
        click.echo("Sending key...")

        try:
            self.node.send_ssh_key_to_node(
                id_rsa_pub_path="./secrets/id_rsa.pub",
                known_hosts_path="./secrets/known_hosts",
            )

            click.echo(f"SSH公钥已成功发送")
        except subprocess.CalledProcessError as e:
            click.echo(f"发送SSH公钥时出错: {e}")


class Build(NujnusCommand):

    # 当和just_execute一起使用时, 要传入parser, 因为和其他command一起使用,避免重复创建parser
    def __init__(self, parser=None) -> None:
        super().__init__()
        self.parser = parser

    def execute_command(self):
        generate_inventories(
            Namespace.generated_path(),
            Namespace.get_all_namespaces(),
        )


class Run(NujnusCommand):

    def __init__(
        self, suite, command_name, namespace, dependency_name, recursive
    ) -> None:
        super().__init__()
        self.suite = suite
        self.command_name = command_name
        self.namespace = namespace
        self.dependency_name = dependency_name
        self.recursive = recursive
        self.commands = []

    def execute_command(self):
        if self.suite != None:
            Namespace.SUITE = self.suite
        # 检查nujnus.yml文件是否存在
        check_file_exists_in_current_directory("nujnus.yml")
        # 执行build, 建立inventory
        just_execute(Build(parser=self.parser))
        # 解析commands.yml
        command_yaml = os.path.join(Namespace.generated_path(), "commands.yml")
        commands = load_commands_from_yaml(command_yaml)
        # 创建CustomizedCommand对象
        for c in commands:
            self.commands.append(
                CustomizedCommand(
                    generated_namespace_path=Namespace.generated_path(),
                    desc=c["desc"],
                    namespace=c["namespace"],
                    command_name=c["command_name"],
                    playbook=c["playbook"],
                    inventory=c["inventory"],
                    workdir=c["workdir"],
                    args=c.get("args", []),
                    cfg=c.get("cfg", None),
                    deps=c.get("deps", []),
                    log_path=c.get("log_path", None),
                    roles_path=c.get("roles_path", None),
                    overwrite=c.get("overwrite", False),
                )
            )

        # 如果两个参数都没有, 打印介绍
        if not self.command_name and not self.namespace:
            ns = [namespace.name for namespace in Namespace._instances]
            ns = sorted(set(ns))
            for n in ns:
                print("\n")
                print(command_desc(f"{n}", "desc", sp="|"))
                print(command_desc("------", "------", sp="|"))
                for command in self.commands:
                    if command.namespace == n:
                        print(command_desc(command.command_name, command.desc))
            CustomizedCommand.assemble_all_deps()
            CustomizedCommand.print_all_tree()

        # 如果只有一个参数, 打印介绍
        elif not self.command_name:
            for command in self.commands:
                if command.namespace == self.namespace:
                    print(command_desc(command.command_name, command.desc))

        # 如果dependency_name为真, 则执行依赖:
        elif self.dependency_name:
            CustomizedCommand.assemble_all_deps()
            command = CustomizedCommand.find_command(self.namespace, self.command_name)
            dep = command.find_dep(self.dependency_name)
            # print(dep.name)
            if self.recursive:
                for d in dep.do:
                    # self.execute_one_command(d.namespace, d.cmd)
                    self.recursive_execute(d.namespace, d.cmd, self.dependency_name)
            else:
                for d in dep.do:
                    self.execute_one_command(d.namespace, d.cmd)
            print("assembled")

        # 如果dependency_name为非真, 且参数齐全, 执行命令:
        else:
            self.execute_one_command(self.namespace, self.command_name)
            # 从YAML文件中加载命令定义

    # 递归调用
    def recursive_execute(self, namespace, command_name, dependency_name):
        command = CustomizedCommand.find_command(namespace, command_name)
        dep = command.find_dep_or_not(dependency_name)
        # 存在依赖的话就先调用依赖
        if dep:
            for d in dep.do:
                self.recursive_execute(d.namespace, d.cmd, dependency_name)

        self.execute_one_command(namespace, command_name)

    # 生成命令, 调用命令
    def execute_one_command(self, namespace, command_name):
        command = CustomizedCommand.find_command(
            namespace=namespace, command_name=command_name
        )
        command.execute()


class Vars(NujnusCommand):

    def __init__(self, namespace) -> None:
        super().__init__()
        self.namespace = namespace

    def execute_command(self):

        check_file_exists_in_current_directory("nujnus.yml")
        just_execute(Build(parser=self.parser))

        # 从YAML文件中加载命令定义
        commands = load_commands_from_yaml("commands.yml")

        # 生成命令
        ansible_command, workdir, env = generate_ansible_inventory_command(
            Namespace.generated_path(), commands, self.namespace
        )

        # 执行ansible命令
        subprocess.run(ansible_command, cwd=workdir, env=env)


# ------------------------------------------------
#
#  CRUD
#
# ------------------------------------------------


class Up(CRUDCommand):

    def execute_command(self):
        # 如果通过了上述校验，则处理all_node和nodename的正常逻辑

        for node in self.target_nodes:
            node.up()


class Remove(CRUDCommand):

    def execute_command(self):

        for node in self.target_nodes:
            node.remove()


class Reload(CRUDCommand):

    def execute_command(self):

        for node in self.target_nodes:
            node.reload()


class Down(CRUDCommand):

    def execute_command(self):

        for node in self.target_nodes:
            node.down()


# ------------------------------------------------
#
#  基于子类的
#
# ------------------------------------------------
class Config(NodeCommand):

    def execute_command(self):

        click.echo("Logging in for config...")

        self.node.config()


class Status(NodeCommand):

    def execute_command(self):
        click.echo("Getting provider status...")
        try:
            self.node.status()
        except subprocess.CalledProcessError as e:
            click.echo(f"status执行失败")
