from nujnus.yml_parser.nujnus_yml_parser import MetaParser
from .vagrant_node import (
    VagrantNode,
    VagrantProviderNode,
)
from .schema import vagrant_resource_schema, vagrant_provider_resource_schema


class VagrantResourceParser(MetaParser):

    def parse(self) -> list:

        self.validate(schema=vagrant_resource_schema)

        node = VagrantNode(
            ip=self.raw_data["ip"],
            username=self.raw_data["username"],
            sshkey=self.raw_data["sshkey"] if "sshkey" in self.raw_data else None,
            password=(
                self.raw_data["password"] if "password" in self.raw_data else None
            ),
            path=(self.raw_data["path"]),
            name=self.raw_data["name"],
            provider_name=self.raw_data["provider"],
            netdev=self.raw_data["netdev"],
            cpu=self.raw_data["cpu"],
            memory=self.raw_data["memory"],
            box_name=self.raw_data["box_name"],
        )
        self.parse_meta(node)

        return [node]


class VagrantProviderParser(MetaParser):

    def parse(self) -> list:

        self.validate(schema=vagrant_provider_resource_schema)

        node = VagrantProviderNode(
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
