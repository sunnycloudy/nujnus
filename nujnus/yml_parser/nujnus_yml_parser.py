import copy
from cerberus import Validator
from nujnus.common.error import NujnusError
from .schema import (
    physical_resource_schema,
    before_text_schema,
    after_text_schema,
)

from abc import ABC, abstractmethod
from nujnus.node.node import Node, Namespace
from functools import lru_cache

from nujnus.module.config import package_name_list

import importlib
import pkgutil
from nujnus.common.ruamel_yaml_config import yaml


class NujnusParser(ABC):
    def __init__(self, raw_data) -> None:
        """
        raw_data为待解析的数据
        """
        super().__init__()
        self.raw_data = raw_data

    @abstractmethod
    def parse(self) -> list:
        pass

    def validate(self, schema):
        validator = Validator(schema)
        if validator.validate(self.raw_data, schema):
            return True
        raise NujnusError(message=validator.errors)


class MetaParser(NujnusParser):
    def __init__(self, raw_data) -> None:
        super().__init__(raw_data)

    # TerraformNodePoolParser 之类的可能会反复调用, lru_cache用来避免副作用持续增加
    # @lru_cache(maxsize=None)
    def parse_meta(self, node):
        # 分析meta
        # 创建namespace
        # 创建group
        # 返回namespace对象列表
        if "meta" in self.raw_data:
            for one_namespace_info in self.raw_data["meta"]:
                if "namespace" in one_namespace_info:
                    namespace = Namespace.create(
                        name=one_namespace_info["namespace"]
                    )  # (((这里需要lru, 并且查询或创建后注册当前node到all组))) # 如果已经注册,报错
                    group = namespace.find_or_create_group("all")
                    group.append_node(node)
                    if "vars" in one_namespace_info:
                        node.update_vars(namespace.name, one_namespace_info["vars"])
                    if "groups" in one_namespace_info:
                        for group_name in one_namespace_info["groups"]:
                            group = namespace.find_or_create_group(group_name)
                            group.append_node(node)
                else:
                    raise NujnusError(message="错误的meta元素")


class PhysicalParser(MetaParser):

    def parse(self) -> list:

        self.validate(schema=physical_resource_schema)

        node = Node(
            ip=self.raw_data["ip"],
            username=self.raw_data["username"],
            sshkey=self.raw_data["sshkey"] if "sshkey" in self.raw_data else None,
            password=(
                self.raw_data["password"] if "password" in self.raw_data else None
            ),
            name=self.raw_data["name"],
        )

        self.parse_meta(node)

        return [node]


class BeforeTextParser(NujnusParser):

    def parse(self) -> list:
        self.validate(schema=before_text_schema)

        namespace = Namespace.find_by_name(name=self.raw_data["namespace"])
        if namespace:
            namespace.before_text = self.raw_data["before_txt"]


class AfterTextParser(NujnusParser):

    def parse(self) -> list:
        self.validate(schema=after_text_schema)

        namespace = Namespace.find_by_name(name=self.raw_data["namespace"])
        if namespace:
            namespace.after_text = self.raw_data["after_txt"]


class ResourceListParser(NujnusParser):
    """
    parser用来保存, 通过分析得到的所有顶层资源对象
    """

    # known_parsers = ["VagrantResourceParser", "PhysicalParser", "VagrantProviderParser"]

    # 工厂函数, 避免反复创建
    @classmethod
    @lru_cache(maxsize=None)
    def create(cls):
        with open("nujnus.yml", "r", encoding="utf-8") as file:
            # raw_data = yaml.safe_load(file)
            raw_data = yaml.load(file)

        return ResourceListParser(raw_data=raw_data)

    def __init__(self, raw_data) -> None:
        super().__init__(raw_data)
        self.resource_list = []

    # 获取对应的parser类
    def get_parser(self, parser_name):
        # if parser_name in ResourceListParser.known_parsers:
        parser_class = globals().get(parser_name)
        if parser_class == None:
            raise NujnusError(message="The parser is not known")
        return parser_class

    # else:
    #    raise NujnusError(message="The parser is not known")

    def load_package(self, package_name):
        my_package = importlib.import_module(package_name)
        # 遍历 my_package 包中的所有模块
        for importer, modname, ispkg in pkgutil.iter_modules(
            my_package.__path__, my_package.__name__ + "."
        ):
            # 动态导入模块
            module = importlib.import_module(modname)
            # 遍历模块中的所有属性，查找类并将它们注册到全局命名空间中
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if isinstance(attribute, type):  # 检查这个属性是否是一个类
                    globals()[attribute_name] = attribute  # 注册类到全局命名空间

    @lru_cache(maxsize=None)
    def parse(self) -> list:
        # 假设 my_package 是你的包名，它位于你要动态导入的文件夹中
        for package_name in package_name_list:
            self.load_package(package_name)

        # self.validate(schema=resouce_list_schema)
        if isinstance(self.raw_data, list):
            for resource_data in self.raw_data:
                if isinstance(resource_data, dict):
                    # 根据type名, 获取parser_class
                    if "type" in resource_data:
                        parser_class = self.get_parser(resource_data["type"])
                    else:
                        if "before_txt" in resource_data:
                            parser_class = BeforeTextParser
                        if "after_txt" in resource_data:
                            parser_class = AfterTextParser

                # 生成具体的parser对象
                parser = parser_class(resource_data)
                # 用parser对象生成具体的单个资源序列
                parser.parse()

            # 检查是否有重名的node
            Node.check_duplicate()
            return "ok"

        raise NujnusError(message="错误的格式")
