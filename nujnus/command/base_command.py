from abc import ABC, abstractmethod
from nujnus.node.node import Node
from nujnus.common.ruamel_yaml_config import yaml

# 在Python中，ABC是Abstract Base Classes的缩写，它是Python的abc模块中的一个特殊类。Abstract Base Classes（抽象基类）用于创建一个基础框架，允许你定义一些方法和属性，这些方法和属性在子类中必须被实现或定义。这有助于确保子类遵循特定的接口或实现特定的行为。
#
# 使用抽象基类可以做到以下几点：
#
# 强制子类实现特定的方法。如果子类没有实现所有的抽象方法，那么在尝试实例化该子类时，Python将抛出TypeError。
# 提供共享的代码实现。抽象基类可以提供一些方法的实现，子类可以直接使用或覆盖这些实现。
# 作为一种类型检查工具。你可以检查某个实例是否实现了特定的抽象基类，这在需要确保某个对象支持特定接口或方法时非常有用。
# 在Python中使用abc.ABC创建抽象基类的一个简单例子如下：
from nujnus.common.utils import check_file_exists_in_current_directory
from nujnus.common.utils import *

from nujnus.version import __version__
from nujnus.common.error import *
from nujnus.yml_parser.nujnus_yml_parser import ResourceListParser
from functools import lru_cache


# ----------------------------------------------------
class NujnusCommand(ABC):
    """
    NujnusCommand类和其子类确定了: 执行一条命令的流程模版是怎样的.
    1.如何进行必要的检查.
    2.如何调用parser去检查配置的语法, 生成node对象, 和其他资源对象.

    而具体的命令子类, 则实现了execute_command成员方法:
    具体的子类会根据参数, 从parser的结果中获取必要的信息.
    在Parser执行后, Node的缓存也会保存很多信息.
    从而确定了:
    1. 要调用的对想的, 确定要调用的对象, 和要调用的参数.
    2. 确定了调用的对象的方法.
    """

    def check_environment(self):
        check_file_exists_in_current_directory("nujnus.yml")

    @lru_cache(maxsize=None)
    def parse_config(self):
        # 从文件中读取YAML内容
        # with open("nujnus.yml", "r", encoding="utf-8") as file:
        #    #raw_data = yaml.safe_load(file)
        #    raw_data = yaml.load(file)

        self.parser = ResourceListParser.create()
        self.parser.parse()

    def before_execute(self):
        # 定位目标node
        # 构建参数
        # 根据各种资源的特性, 将paser中的结果, 构造成参数
        pass

    @abstractmethod
    def execute_command(self):
        pass

    def after_execute(self):
        pass


class NodeCommand(NujnusCommand):

    def __init__(self, nodename) -> None:
        super().__init__()
        self.nodename = nodename
        self.provider_node = None
        self.node = None

    def parse_config(self):
        super().parse_config()

        self.node = Node.find_by_name(self.nodename)

        if self.node.provider_name == None:
            self.provider_node = None
        else:
            self.provider_node = Node.find_by_name(self.node.provider_name)


class FileCommand(NodeCommand):
    def __init__(self, nodename, file_path) -> None:
        super().__init__(nodename=nodename)
        self.file_path = file_path


class CRUDCommand(NujnusCommand):
    """
    # 根据参数,
    # 决定期望的资源.
    # 检查涉及到的目标对象.
    # 依次调用目标对象的参数添加函数, 添加到参数中, 检查是否能合并操作.
    # 依次调用目标对象的执行函数.
    """

    def __init__(self, namespace_name, group_name, nodename) -> None:
        super().__init__()
        self.nodename = nodename
        self.namespace_name = namespace_name
        self.group_name = group_name
        self.target_provider_list = []
        self.target_nodes = []

    def parse_config(self):
        super().parse_config()

        if self.namespace_name != None:
            if self.nodename != None:
                raise NujnusError(message="错误的参数组合")
            if self.group_name != None:
                # 根据group+namespace找到相关node
                nodes = Node.find_by_group(
                    namespace_name=self.namespace_name, group_name=self.group_name
                )
            else:
                # 根据namespace, 找到所有相关node
                nodes = Node.find_by_namespace(namespace_name=self.namespace_name)
        else:
            if self.group_name != None:
                raise NujnusError(message="错误的参数组合")
            else:
                if self.nodename != None:
                    node = Node.find_by_name(name=self.nodename)
                    if node:
                        nodes = [node]
                    else:
                        nodes = []

        self.target_nodes = nodes


    def execute_command(self):
        # 调用操作
        # 对所有保存的provider, 逐个调用操作函数
        pass

    def before_execute(self):
        pass


# 函数模板
# 实现了NujnusCommand的生命周期:
def call_nujnus_command(command: NujnusCommand):
    command.check_environment()
    command.parse_config()
    command.before_execute()
    command.execute_command()
    command.after_execute()


def just_execute(command: NujnusCommand):
    command.before_execute()
    command.execute_command()
    command.after_execute()
