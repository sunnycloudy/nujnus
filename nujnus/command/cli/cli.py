# login.py
import click
from nujnus.common.error import handle_exceptions
from nujnus.common.helper import helper
from nujnus.command.predefined_command import *
from nujnus.version import __version__


@click.command(help=helper("创建nujnus目录", "nujnus init"))
@handle_exceptions
def init():
    call_nujnus_command(Init())


# --------------------


@click.command(help=helper("ssh-copy-id到节点", "nujnus sendkey node1"))
@click.argument("nodename")
@handle_exceptions
def sendkey(nodename):
    call_nujnus_command(Sendkey(nodename=nodename))


@click.command(help=helper("登录虚拟机", "nujnus login node1"))
@click.argument("nodename")
@handle_exceptions
def login(nodename):
    call_nujnus_command(Login(nodename=nodename))


@click.command(
    help=helper(
        "配置资源",
        "nujnus config <resource_name>",
    )
)
@click.argument("nodename")
@handle_exceptions
def config(nodename):

    call_nujnus_command(Config(nodename=nodename))


@click.command(help=helper("树形结构显示所有节点", "nujnus build"))
@click.argument("nodename")
@click.argument("file_path")
@handle_exceptions
def get(nodename, file_path):
    call_nujnus_command(Get(nodename=nodename, file_path=file_path))


@click.command(help=helper("更新./secrets/known_hosts", "nus scan"))
@handle_exceptions
def scan():
    call_nujnus_command(Scan())


@click.command(help=helper("显示vagrant虚拟机和docker容器状态", "nujnus status"))
@click.argument("nodename")
@handle_exceptions
def status(nodename):

    call_nujnus_command(Status(nodename=nodename))


# --------------------


@click.command(help=helper("安装role依赖", "nus version"))
@click.option(
    "--requirements",
    default="./requirements.yml",
    help="Path to the requirements file.",
    show_default=True,
)
@click.option(
    "--roles-path",
    default="./roles",
    help="Path where roles should be installed.",
    show_default=True,
)
@handle_exceptions
def install(requirements, roles_path):
    """
    This script runs the ansible-galaxy install command.
    """
    check_file_exists_in_current_directory("nujnus.yml")
    command = f"ansible-galaxy install -r {requirements} -p {roles_path}"
    click.echo(f"Executing: {command}")
    subprocess.run(command, shell=True)


@click.command(help=helper("查看nujnus版本", "nus version"))
@handle_exceptions
def version():
    """显示版本号"""
    click.echo(f"当前版本: {__version__}")


@click.command(help=helper("树形结构显示所有节点", "nujnus tree"))
@handle_exceptions
def tree():
    call_nujnus_command(Tree())


@click.command(help=helper("树形结构显示所有节点", "nujnus build"))
@handle_exceptions
def build():
    call_nujnus_command(Build())


@click.command(help=helper("显示所有节点名", "nujnus ls"))
@handle_exceptions
def ls():
    call_nujnus_command(Ls())


@click.command(help=helper("生成hosts文件", "nus new hosts"))
@handle_exceptions
def hosts():
    call_nujnus_command(Hosts())


# 用来给vscode生成remote deveop配置,
# 生成一个目录包含了ssh_config和各种key和known_hosts文件,
# 直接下载到~/.nujnus_config中,
# 然后指定vscode使用这个目录的配置即可
@click.command(help=helper("生成ssh_config配置", "nus new ssh_config"))
@handle_exceptions
def ssh_config():
    call_nujnus_command(SshConfig())


@click.command(help=helper("在roles目录生成role", "nus new role <rolename>"))
@click.argument("rolename")
@handle_exceptions
def role(rolename):
    call_nujnus_command(Role(rolename=rolename))


@click.group()
def new():
    pass


new.add_command(role)
new.add_command(hosts)
new.add_command(ssh_config)

# --------------------------------


@click.command(help=helper("创建和启动虚拟机, 若已经创建, 则仅启动虚拟机", ""))
@click.option("--namespace", "namespace_name", default=None, help="node in namespace")
@click.option("--group", "group_name", default=None, help="node in group")
@click.option("--node", "node_name", default=None, help="search node by name")
@handle_exceptions
def up(namespace_name, group_name, node_name):
    call_nujnus_command(
        Up(namespace_name=namespace_name, group_name=group_name, nodename=node_name)
    )


@click.command(help=helper("关闭虚拟机", ""))
@click.option("--namespace", "namespace_name", default=None, help="node in namespace")
@click.option("--group", "group_name", default=None, help="node in group")
@click.option("--node", "node_name", default=None, help="search node by name")
@handle_exceptions
def down(namespace_name, group_name, node_name):
    call_nujnus_command(
        Down(namespace_name=namespace_name, group_name=group_name, nodename=node_name)
    )


@click.command(help=helper("删除虚拟机", ""))
@click.option("--namespace", "namespace_name", default=None, help="node in namespace")
@click.option("--group", "group_name", default=None, help="node in group")
@click.option("--node", "node_name", default=None, help="search node by name")
@handle_exceptions
def remove(namespace_name, group_name, node_name):
    call_nujnus_command(
        Remove(namespace_name=namespace_name, group_name=group_name, nodename=node_name)
    )


@click.command(help=helper("重新载入虚拟机", ""))
@click.option("--namespace", "namespace_name", default=None, help="node in namespace")
@click.option("--group", "group_name", default=None, help="node in group")
@click.option("--node", "node_name", default=None, help="search node by name")
@handle_exceptions
def reload(namespace_name, group_name, node_name):
    call_nujnus_command(
        Reload(namespace_name=namespace_name, group_name=group_name, nodename=node_name)
    )


# -------


@click.command(help=helper("运行", "nus run <namespace> <command_name>"))
@click.option("-d", "dependency_name", default=None, help="运行依赖")
@click.option("-s", "suite", default=None, help="suite名")
@click.option("-r", "recursive", is_flag=True, help="运行依赖")
@click.argument("args", nargs=-1)
@handle_exceptions
def run(dependency_name, suite, recursive, args):

    if len(args) == 2:
        namespace = args[0]
        command_name = args[1]
    elif len(args) == 1:
        namespace = args[0]
        command_name = None
    elif len(args) == 0:
        namespace = None
        command_name = None
    else:
        raise NujnusError(message="错误的参数数量")

    call_nujnus_command(
        Run(
            suite = suite,
            command_name=command_name,
            namespace=namespace,
            dependency_name=dependency_name,
            recursive=recursive,
        )
    )


@click.command(help=helper("显示预定义变量", "nus vars <namespace> "))
@click.argument("namespace")
@handle_exceptions
def vars(namespace):

    call_nujnus_command(Vars(namespace=namespace))
