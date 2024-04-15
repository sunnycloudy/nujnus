from abc import ABC, abstractmethod
from nujnus.common.error import NujnusError
import subprocess
from functools import lru_cache
import copy
from nujnus.generator.generator import generate_inventory
from nujnus.command.customized_command import CustomizedCommand
import os


class Node(ABC):
    """
    确定了用来生成ansible inventory的基本数据结构.
    """

    _instances = []  # 用于存储所有实例的类变量
    current_namespace = None
    NO_CRUD = False

    def __init__(
        self, ip, username, sshkey, password, name, provider_name=None
    ) -> None:
        # ---------
        # 基本的ssh部署层面依赖的信息:
        self.ip = ip
        self.username = username
        self.sshkey = sshkey
        self.password = password
        self.provider_name = provider_name
        # ---------
        # 资源组织创建层面依赖的信息:
        self.name = name
        self.type = None
        self.provider_node = None

        self.namespace_vars_map = {}
        self.namespace_inivars_map = {}
        self.hosts_mapping = {}

        Node._instances.append(self)  # 创建实例时添加到_instances列表

    def add_domain(self, key, domain):
        self.hosts_mapping[key] = domain

    def get_domain(self, key):
        if key not in self.hosts_mapping:
            raise NujnusError("hosts_mapping中不存在的key")
        return self.hosts_mapping[key]

    @classmethod
    def get_hosts_mapping(cls):
        hosts_mapping = {}
        for node in cls._instances:
            for key, domain in node.hosts_mapping.items():
                hosts_mapping[domain] = node.ip
        return hosts_mapping

    def update_vars(self, namespace_name, vars):
        self.namespace_vars_map[namespace_name] = vars

    def vars_of(self, namespace_name):
        return copy.deepcopy(self.namespace_vars_map.get(namespace_name, {}))

    @classmethod
    def change_current_namesapce(cls, namespace):
        cls.current_namespace = namespace

    @property
    def inivars(self):
        """这是一个只读属性"""
        if Node.current_namespace == None:
            raise NujnusError("Node.current_namespace未设置")
        return copy.deepcopy(
            self.namespace_inivars_map.get(Node.current_namespace.name, {})
        )

    @inivars.setter
    def inivars(self, value):
        """设置vars的值"""
        if Node.current_namespace == None:
            raise NujnusError("Node.current_namespace未设置")
        self.namespace_inivars_map[Node.current_namespace.name] = value

    @property
    def vars(self):
        """这是一个只读属性"""
        if Node.current_namespace == None:
            raise NujnusError("Node.current_namespace未设置")
        return copy.deepcopy(
            self.namespace_vars_map.get(Node.current_namespace.name, {})
        )

    @vars.setter
    def vars(self, value):
        """设置vars的值"""
        if Node.current_namespace == None:
            raise NujnusError("Node.current_namespace未设置")
        self.namespace_vars_map[Node.current_namespace.name] = value

    def get_node_type(self):
        return self.type

    def get_provider_node(self):
        return self.provider_node

    def is_in_namespace(self, namespace_name):  # 从Namespace中找
        # 检查该node是否在namespace中
        namespace = Namespace.find_by_name(namespace_name)
        if namespace:
            if "all" in namespace.groups.keys():
                for node in namespace.groups["all"].nodes:
                    if self == node:
                        return True
        return False

    def is_in_group(self, namespace_name, group_name):
        # 检查该node是否在group中
        namespace = Namespace.find_by_name(namespace_name)
        if namespace:
            if group_name in namespace.groups.keys():
                for node in namespace.groups[group_name].nodes:
                    if self == node:
                        return True
        return False

    @classmethod
    def get_all_nodes(cls):
        return cls._instances

    @classmethod
    def find_by_name(cls, name):
        """
        根据nodename 获取node信息
        """
        for instance in cls._instances:
            if instance.name == name:
                return instance
        return None

    @classmethod
    def find_roots(cls):
        return [
            instance for instance in cls._instances if instance.provider_name == None
        ]

    @classmethod
    def find_by_provider_name(cls, provider_name):
        """
        找特定provider之下的node
        """
        return [
            instance
            for instance in cls._instances
            if instance.provider_name == provider_name
        ]

    @classmethod
    def check_duplicate(cls):
        """
        检查是否有重名的资源
        """
        names = set()

        # 遍历解析后的数据，检查 name 值
        for instance in cls._instances:
            # 检查主服务器的 name
            if instance.name in names:
                raise NujnusError(message=f"Duplicate name found: {instance.name}")
            else:
                names.add(instance.name)

    @classmethod
    def find_by_namespace(cls, namespace_name):
        """
        根据namespace_name 获取node信息
        """
        return [
            instance
            for instance in cls._instances
            if instance.is_in_namespace(namespace_name)
        ]

    @classmethod
    def find_by_group(cls, namespace_name, group_name):
        """
        根据namespace_name, group_name 获取node信息
        """
        return [
            instance
            for instance in cls._instances
            if instance.is_in_group(namespace_name, group_name)
        ]

    @classmethod
    def print_node_tree(cls, indent=""):
        providers = cls.find_roots()
        for provider in providers:
            print(f"{indent}Provider: {provider.name}")
            nodes = cls.find_by_provider_name(provider_name=provider.name)
            for node in nodes:
                print(f"{indent}    └─ nodes: {node.name}")

    @classmethod
    def print_node_plain(cls):
        providers = cls.find_roots()
        for provider in providers:
            print(f"{provider.name}")
            nodes = cls.find_by_provider_name(provider_name=provider.name)
            for node in nodes:
                print(f"{node.name}")

    @classmethod
    def generate_hosts_file_content(cls):
        # 初始化一个空字符串用于存储 hosts 文件的内容
        hosts_content = """
127.0.0.1 localhost
::1       localhost
"""

        # for node in cls.get_all_nodes():
        #    # 添加 provider/host
        #    hosts_content += f"{node.ip} {node.name}\n"

        for domain, ip in cls.get_hosts_mapping().items():
            hosts_content += f"{ip} {domain}\n"

        return hosts_content

    @classmethod
    def scan(cls):
        for node in cls.get_all_nodes():
            print(f"[{node.name}]:")
            try:
                command = "ssh-keyscan -H {} >> ./secrets/known_hosts".format(node.ip)
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Scan时出错: {e}")

    def get_file(self, file_path, local_path, path_to_known_hosts):

        ip, username, sshkey, password = (
            self.ip,
            self.username,
            self.sshkey,
            self.password,
        )

        if sshkey:
            # 构建SSH命令，使用sshpass来自动输入密码
            # 安装sshpass可能需要额外的步骤，具体取决于你的操作系统
            command = f"scp -i {sshkey} -o StrictHostKeyChecking=no -o UserKnownHostsFile={path_to_known_hosts} {username}@{ip}:{file_path} {local_path}"

        else:
            # 构建SSH命令，使用sshpass来自动输入密码
            # 安装sshpass可能需要额外的步骤，具体取决于你的操作系统
            command = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile={path_to_known_hosts}  {username}@{ip}:{file_path} {local_path}"

        # 执行命令
        subprocess.run(command, shell=True, check=True)

    def send_ssh_key_to_node(self, id_rsa_pub_path, known_hosts_path):
        """
        使用ssh-copy-id发送SSH公钥到目标节点。
        :param id_rsa_pub_path: id_rsa.pub文件的路径
        :param known_hosts_path: known_hosts文件的路径
        """
        # 构建ssh-copy-id命令
        command = [
            "ssh-copy-id",
            "-i",
            id_rsa_pub_path,
            "-o",
            f"UserKnownHostsFile={known_hosts_path}",
            "-p",
            str(22),
            f"{self.username}@{self.ip}",
        ]

        # 执行命令
        subprocess.run(command, check=True)

    def status(self):
        print("当前节点无此功能")

    def ssh_login(self, path_to_known_hosts):

        ip, username, sshkey, password = (
            self.ip,
            self.username,
            self.sshkey,
            self.password,
        )

        if sshkey:
            # 构建SSH命令，使用sshpass来自动输入密码
            # 安装sshpass可能需要额外的步骤，具体取决于你的操作系统
            command = f"ssh -i {sshkey} -o StrictHostKeyChecking=no -o UserKnownHostsFile={path_to_known_hosts} {username}@{ip}"

        else:
            # 构建SSH命令，使用sshpass来自动输入密码
            # 安装sshpass可能需要额外的步骤，具体取决于你的操作系统
            command = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile={path_to_known_hosts}  {username}@{ip}"
        # 使用subprocess运行命令
        subprocess.run(
            command, shell=True, check=True
        )  # stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

    def config(self):
        print("当前节点无此功能")

    def up(self):
        print("当前节点无此功能")

    def reload(self):
        print("当前节点无此功能")

    def down(self):
        print("当前节点无此功能")

    def remove(self):
        print("当前节点无此功能")


class ProviderNode(Node):
    def __init__(
        self, ip, username, sshkey, password, name, provider_name=None
    ) -> None:
        super().__init__(ip, username, sshkey, password, name, provider_name)

    def up(self):
        print("当前节点无此功能")

    def reload(self):
        print("当前节点无此功能")

    def down(self):
        print("当前节点无此功能")

    def remove(self):
        print("当前节点无此功能")


class Group:

    def __init__(self, group_name) -> None:
        self.name = group_name
        self.namespace = None
        self.nodes = []
        self.vars = {}

    def append_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)

    def extend_nodes(self, nodes):
        for node in nodes:
            if node not in self.nodes:
                self.nodes.append(node)


class Groups(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        """自定义__str__方法，用于打印字典的字符串表示"""
        return f"Groups: {dict.__str__(self)}"

    # 如果遇到未定义的字段, 如果value是一个group类型, 就创建为group, 否则报错.

    # ||def __setattr__(self, key: str, value: Group):
    # ||    # 等价于:
    # ||    # with clean_namespace("test") as n:
    # ||    #   all = Group("all")
    # ||    #   all.nodes = [Node.find_by_name("controller")]
    # ||    #   n.groups["all"] = all

    # ||    if key in self:
    # ||        self[key].nodes = value
    # ||    else:
    # ||        self[key] = Group(group_name=key)
    # ||        self[key].nodes = value

    # 如果遇到未定义的字段, 如果name是在groups中的, 就返回对应group,否则报错.
    def __getattr__(self, name: str):
        if name not in self:
            self[name] = Group(group_name=name)
        return self[name]


from io import StringIO
from nujnus.common.ruamel_yaml_config import yaml


class Namespace:

    _instances = []  # 用于存储所有实例的类变量
    command_history = []

    BUILD_ONLY = False
    SUITE = "default"

    @classmethod
    def generated_path(cls):
        return f"./generated/{cls.SUITE}/"

    # 决定了save_history的范围
    RUN_FROM = None
    RUN_TILL = None

    @classmethod
    def save_command_list(cls):
        os.makedirs(Namespace.generated_path(), exist_ok=True)
        command_yaml = os.path.join(Namespace.generated_path(), "commands.yml")
        with open(command_yaml, "w") as f:
            for cmd in cls.command_history:
                cmd_yaml = cmd.to_yaml()
                f.write(cmd_yaml)

    @classmethod
    @lru_cache(maxsize=None)
    def create(cls, name):
        return Namespace(name)

    def find_or_create_group(self, group_name):
        for g_name, group in self.groups.items():
            if g_name == group_name:
                return group
        group = Group(group_name=group_name)
        self.groups[group_name] = group
        return group

    def __init__(self, name) -> None:
        self.name = name
        self.before_text = ""
        self.after_text = ""
        self.groups = Groups()  # group_name :  group_object
        self.run_list = []
        Namespace._instances.append(self)  # 创建实例时添加到_instances列表

    @classmethod
    def get_all_namespaces(cls):
        return cls._instances

    @classmethod
    def find_by_name(cls, name):
        """
        根据nodename 获取node信息
        """
        for instance in cls._instances:
            if instance.name == name:
                return instance
        return None

    def has_group(self, group_name):
        """
        检查当前<namespace>是否包含叫<group_name>的组.
        """
        for group in self.groups:
            if group.name == group_name:
                return True
        return False

    # 创建对应command并且run, run之前会先build.
    def run(
        self,
        name,
        workdir,
        playbook,
        inventory=None,
        desc="",
        log_path=None,
        roles_path=None,
        args=[],
        cfg=None,
        deps=[],
    ):

        if cfg == None:
            cfg = "./default.cfg"
        if roles_path == None:
            roles_path = "./roles/"
        if inventory == None:
            inventory = "{}/{}/inventory.ini".format(
                Namespace.generated_path(), self.name
            )
            overwrite = False
        else:
            overwrite = True

        self.run_list.append(
            CustomizedCommand(
                generated_namespace_path=Namespace.generated_path(),
                desc=desc,
                namespace=self.name,
                command_name=name,
                playbook=playbook,
                inventory=inventory,
                overwrite=overwrite,
                workdir=workdir,
                log_path=log_path,
                roles_path=roles_path,
                args=args,
                cfg=cfg,
                deps=deps,
            )
        )

    @classmethod
    def have_group(cls, namespace_name, group_name):
        """
        检查叫<namespace_name>的namespace们是否包含叫<group_name>的组.
        """
        for instance in cls._instances:
            if instance.name == namespace_name:
                for g_name, group in instance.groups.items():
                    if g_name == group_name:
                        return True
        return False


class safe_namespace:
    def __init__(self, name):
        self.name = name
        namespace = Namespace.find_by_name(name)
        if namespace:
            raise NujnusError(message="Namespace: {} 已经存在".format(name))
        self.namespace = Namespace.create(name=name)  # 创建一个新的命名空间实例

    def __enter__(self):
        # 进入with语句块时执行的代码
        # 这里返回命名空间实例，允许在with块中进行操作
        Node.change_current_namesapce(self.namespace)
        return self.namespace

    def __exit__(self, exc_type, exc_value, traceback):
        # 离开with语句块时执行的代码
        # 先generate_inventory
        # 退出前,执行run_list.
        # 执行完run_list 加入到Namespace的run_history中
        generate_inventory(Namespace.generated_path(), self.namespace)
        for command in self.namespace.run_list:
            if Namespace.BUILD_ONLY == False:
                command.execute()
            Namespace.command_history.append(command)
        Node.current_namespace = None
