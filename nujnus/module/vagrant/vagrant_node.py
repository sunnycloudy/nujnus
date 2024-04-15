from nujnus.node.node import Node, ProviderNode, Namespace
import subprocess
from nujnus.common.utils import *
from nujnus.invoker.ansible_runner import run_builtin_playbook

from .get_playbook_extra_vars import (
    # 构建ansible参数用的:
    get_vagrant_extra_vars,
)
from .utils import ssh_login_and_cd_to_dir
from .generator import _generate_provider_inventory_


class VagrantNode(Node):

    def __init__(
        self,
        ip,
        username,
        sshkey,
        password,
        name,
        provider_name,
        netdev,
        cpu,
        memory,
        box_name,
        path,
    ) -> None:
        super().__init__(ip, username, sshkey, password, name, provider_name)
        self.netdev = netdev
        self.cpu = cpu
        self.memory = memory
        self.box_name = box_name
        self.path = path

    def config(self):
        # 拼接node的配置目录地址
        node_config_dir = "{}/{}".format(self.path, self.name)

        # 根据node的配置目录地址
        # 登录provider后切换到配置目录.
        ssh_login_and_cd_to_dir(
            provider_node=Node.find_by_name(self.provider_name)[0],
            path_to_known_hosts="./secrets/known_hosts",
            cd_to_dir=node_config_dir,
        )

    def get_provider(self):
        provider = Node.find_by_name(self.provider_name)
        if provider == None:
            raise NujnusError("不存在的provider:{}".format(self.provider_name))
        return provider

    def up(self):
        if Node.NO_CRUD == False:
            provider = self.get_provider()
            provider.up_nodes([self])

    def reload(self):
        if Node.NO_CRUD == False:
            provider = self.get_provider()
            provider.reload_nodes([self])

    def down(self):
        if Node.NO_CRUD == False:
            provider = self.get_provider()
            provider.down_nodes([self])

    def remove(self):
        if Node.NO_CRUD == False:
            provider = self.get_provider()
            provider.remove_nodes([self])


class VagrantProviderNode(ProviderNode):

    def status(self):
        # self.node.ssh_status()

        ip, username, sshkey_path = (
            self.ip,
            self.username,
            self.sshkey,
        )

        # 构建SSH命令，使用sshpass来自动输入密码
        # 安装sshpass可能需要额外的步骤，具体取决于你的操作系统
        # command = f"ssh -t -i {sshkey_path} -o StrictHostKeyChecking=no {username}@{ip} 'vagrant global-status && docker ps -a; exit'"

        remote_commands = "vagrant global-status"
        path_to_known_hosts = "./secrets/known_hosts"

        command = (
            f"ssh -t -i {sshkey_path} "
            f"-o StrictHostKeyChecking=no "
            f"-o UserKnownHostsFile={path_to_known_hosts} "
            f"{username}@{ip} "
            f"{remote_commands}"
        )

        # 使用subprocess运行命令
        subprocess.run(command, shell=True, check=True)

    def up_nodes(self, nodes):
        self.generate_provider_inventory()
        self.apply_nodes_with("up.yml", nodes)

    def reload_nodes(self, nodes):
        self.generate_provider_inventory()
        self.apply_nodes_with("reload.yml", nodes)

    def down_nodes(self, nodes):
        self.generate_provider_inventory()
        self.apply_nodes_with("down.yml", nodes)

    def remove_nodes(self, nodes):
        self.generate_provider_inventory()
        self.apply_nodes_with("remove.yml", nodes)

    def apply_nodes_with(self, builtin_playbook, nodes):

        # 使用内置的playbooks
        #  playbooks/
        #     ├── up.yml        #创建远程环境, 创建或启动
        #     ├── down.yml      #关闭远程环境
        #     ├── remove.yml    #清理远程环境
        #     ├── reload.yml    #重启远程环境

        # 调用playbook来创建环境.
        # 获取当前文件的目录路径
        current_dir = os.path.dirname(__file__)

        playbook_path = os.path.join(
            current_dir,
            "playbooks",
            builtin_playbook,
        )

        extravars = get_vagrant_extra_vars(nodes)
        run_builtin_playbook(
            playbook_path=playbook_path,
            extravars=extravars,
            inventory_path="{}/{}.ini".format(Namespace.generated_path(), self.name),
            nodename=self.name,
        )

    def generate_provider_inventory(self):
        # 后移到节点对象中:
        os.makedirs(Namespace.generated_path(), exist_ok=True)

        _generate_provider_inventory_(
            provider_node=self,
            output_path="{}/{}.ini".format(Namespace.generated_path(), self.name),
        )
