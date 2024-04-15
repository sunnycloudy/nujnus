from nujnus.yml_parser.nujnus_yml_parser import MetaParser
from .schema import terraform_node_pool_schema
from .terraform_node import TerraformNode
import json


class TerraformNodePoolParser(MetaParser):
    """
        # 兼容的Terraform版本:
        # Terraform v1.7.4
        # on linux_amd64

        required_providers {
          aws = {
            source  = "hashicorp/aws"
            version = "~> 3.0"
          }
          alicloud = {
            source  = "hashicorp/alicloud"
            version = "~> 1.120"
          }
          azurerm = {
            source  = "hashicorp/azurerm"
            version = "~> 2.46"
          }
          google = {
            source  = "hashicorp/google"
            version = "~> 3.5"
          }
          tencentcloud = {
            source  = "tencentcloudstack/tencentcloud"
            version = "~> 1.60"
          }
        }

        #lock文件:

    # This file is maintained automatically by "terraform init".
    # Manual edits may be lost in future updates.

    provider "registry.terraform.io/hashicorp/alicloud" {
      version     = "1.218.0"
      constraints = "~> 1.120"
      hashes = [
        "h1:6tFBGLkis3eQAitkfvsLmFBqwe7wZZKUlhA8zuVhCKk=",
        "zh:04f2b39c3b6832369141982bde8a488c72a9fdef87dc4cf6d1c434b3a7a6372e",
        "zh:10100b166963c1ec3ab530fbd1394cc0f154819be6b038eadaebd6f38ae3cd14",
        "zh:48e5170a74226ec6b29c4c7f2a7d61653510a9082dec51ce912d073e7d47ebcc",
        "zh:5bc2ecdfd4d61c16e58502bd69394d0feaad86ddaece8391dba70592b37022f5",
        "zh:8e17d325b88f993883187e8e2c99f98c7d0e9e8fd145191a53131ef23a6a952b",
        "zh:9a4b72b05361bccb081cb3b2c4423e960619fe23ee8e4dfa6ac4a68e55ecf8fe",
        "zh:9ffd306d9adb27037d7504e526b3c99aed7d7cf84a4676284a342b4bf80b4da4",
        "zh:bf31dc62a40c6c80478de7aeeead944f8ceb480c001a37cfcf4b9dc61f3f7ddc",
        "zh:c70a68d03384db7db2e5acd4749e957cac3494131cda9fbb2b12cca727a5e040",
        "zh:c989f4b43b4161e9138ce2e9d9258c71cc4c6af6899d9fc6fa0fef9811764afa",
        "zh:f3053f15bc304795c68aa63dcdeae04f10082da2b23d5f05c462e009897305e0",
      ]
    }

    provider "registry.terraform.io/hashicorp/aws" {
      version     = "3.76.1"
      constraints = "~> 3.0"
      hashes = [
        "h1:5WSHHV9CgBvZ0rDDDxLnNHsjDfm4knb7ihJ2AIGB58A=",
        "zh:1cf933104a641ffdb64d71a76806f4df35d19101b47e0eb02c9c36bd64bfdd2d",
        "zh:273afaf908775ade6c9d32462938e7739ee8b00a0de2ef3cdddc5bc115bb1d4f",
        "zh:2bc24ae989e38f575de034083082c69b41c54b8df69d35728853257c400ce0f4",
        "zh:53ba88dbdaf9f818d35001c3d519a787f457283d9341f562dc3d0af51fd9606e",
        "zh:5cdac7afea68bbd89d3bdb345d99470226482eff41f375f220fe338d2e5808da",
        "zh:63127808890ac4be6cff6554985510b15ac715df698d550a3e722722dc56523c",
        "zh:97a1237791f15373743189b078a0e0f2fa4dd7d7474077423376cd186312dc55",
        "zh:9b12af85486a96aedd8d7984b0ff811a4b42e3d88dad1a3fb4c0b580d04fa425",
        "zh:a4f625e97e5f25073c08080e4a619f959bc0149fc853a6b1b49ab41d58b59665",
        "zh:b56cca54019237941f7614e8d2712586a6ab3092e8e9492c70f06563259171e9",
        "zh:d4bc33bfd6ac78fb61e6d48a61c179907dfdbdf149b89fb97272c663989a7fcd",
        "zh:e0089d73fa56d128c574601305634a774eebacf4a84babba71da10040cecf99a",
        "zh:e957531f1d92a6474c9b02bd9200da91b99ba07a0ab761c8e3176400dd41721c",
        "zh:eceb85818d57d8270db4df7564cf4ed51b5c650a361aaa017c42227158e1946b",
        "zh:f565e5caa1b349ec404c6d03d01c68b02233f5485ed038d0aab810dd4023a880",
      ]
    }

    provider "registry.terraform.io/hashicorp/azurerm" {
      version     = "2.99.0"
      constraints = "~> 2.46"
      hashes = [
        "h1:FXBB5TkvZpZA+ZRtofPvp5IHZpz4Atw7w9J8GDgMhvk=",
        "zh:08d81e72e97351538ab4d15548942217bf0c4d3b79ad3f4c95d8f07f902d2fa6",
        "zh:11fdfa4f42d6b6f01371f336fea56f28a1db9e7b490c5ca0b352f6bbca5a27f1",
        "zh:12376e2c4b56b76098d5d713d1a4e07e748a926c4d165f0bd6f52157b1f7a7e9",
        "zh:31f1cb5b88ed1307625050e3ee7dd9948773f522a3f3bf179195d607de843ea3",
        "zh:767971161405d38412662a73ea40a422125cdc214c72fbc569bcfbea6e66c366",
        "zh:973c402c3728b68c980ea537319b703c009b902a981b0067fbc64e04a90e434c",
        "zh:9ec62a4f82ec1e92bceeff80dd8783f61de0a94665c133f7c7a7a68bda9cdbd6",
        "zh:bbb3b7e1229c531c4634338e4fc81b28bce58312eb843a931a4420abe42d5b7e",
        "zh:cbbe02cd410d21476b3a081b5fa74b4f1b3d9d79b00214009028d60e859c19a3",
        "zh:cc00ecc7617a55543b60a0da1196ea92df48c399bcadbedf04c783e3d47c6e08",
        "zh:eecb9fd0e7509c7fd4763e546ef0933f125770cbab2b46152416e23d5ec9dd53",
      ]
    }

    provider "registry.terraform.io/hashicorp/google" {
      version     = "3.90.1"
      constraints = "~> 3.5"
      hashes = [
        "h1:91QFfSGwMX4wKH5u+/FEMf2W3mToJxHtw/Ty0nvrDEU=",
        "zh:07aabc8e46a5a2b29932e10677b23d4ce9d9a25f22ab61d3307a6b0e7998c84e",
        "zh:0b63cd9534a98ed0fee794da495833046ad5319bd2da3102e21a941b7e2b857e",
        "zh:17f815d57e1426edf8818323ab8e1022c8ec60dce0ced89a3b8e5dde5a95b3cc",
        "zh:37855eae3542f2ebc6416984b124533d00299e0e01dcd7d2bc2205469cb9eceb",
        "zh:579aa32a8e3fa317ddbd28c99a6449ae8864a5b7d10247bca6496f399cb36701",
        "zh:703f71e0231cfe7a025c61db361d928189adba1d4fad2fe77f783dc73c8afe30",
        "zh:afcd80c31cb1ed75ce6813269618e01ab29af68dae7aae1c51521c13acdaa678",
        "zh:b21302f65a0d37045216912695d1ef718a1fe1732c30dc5654891fe2519b8e4e",
        "zh:b69d0c8a74c2cd6233681db37e01aaaf1a6fb6bb24c83f7715bd2b456083e29d",
        "zh:d4fb305816b143cb26c1827c79e56651347fd41809a57184e4807fb3f804f510",
        "zh:fa24173ef9524bdfa1c5cada5188489554b08374f9519fe545f3fc1d3a9d9d4f",
      ]
    }

    provider "registry.terraform.io/tencentcloudstack/tencentcloud" {
      version     = "1.81.80"
      constraints = "~> 1.60"
      hashes = [
        "h1:ikKLBWDCxJ/Geea2c28YBaMoHahAU/0H3hP47BrmkN0=",
        "zh:05adf174aaf8110e7b12044b8157556b266fb53590708f6e777c883f949e8aae",
        "zh:092e274a9a41de6a997c973203d1312c3b308f791fc610aae8d3f72cd7d2d146",
        "zh:0bd3c7f2be19b0d0fb59c18706375a6e6c87dd8f5e5445ea25fa1a5cba01bdba",
        "zh:16f429664319ce45a1bd09974e24dbca3b98ca497f68689d2139515c48e92499",
        "zh:38df90077517b457244f5581f694a77504517fb0ec3f8f4944718de9b65f04b1",
        "zh:3eb00b78586352ade7ea88f184b55f7696e9ec03502644fae999ec3b98e76cc0",
        "zh:4a47f69bf633771ca679c18b1c2b330fd24bb496527837c42d18375a2859ca90",
        "zh:50b5c699dfe71f3bdfa965d23ed31105b7ec1f22c843b79ce528a6ed12327f56",
        "zh:7137b4aadd7b8c2bd36c2d43c6a058fed4e7b1ad236d6505f41379cdcde4ef8f",
        "zh:7bcb54b8dc45c9d71737d43149e99fea5681798950f81ec1500800096305a22d",
        "zh:ac7c1695e0f823e2c7f796a9b09f4b24f3e48362062bd946bf1e3e338fb1eb43",
        "zh:c16672cb7a8972c0c208443835d0a418ff2685e29f7d7644a4885711e61354d4",
        "zh:daf507a56505a9e7d8fa14b26d7dde198653e78d047695067db76fa690f69c8e",
        "zh:faf2b7cba30524049f5a5b1ba307753d59f3e6f6c3aff99c062390622de7ce51",
      ]
    }

    """

    # 本质是分析state
    # 分析到state, 才会创建node
    # 只能通过namespace和group操作,还有一个池名字, 作为资源名字

    def parse(self) -> list:

        self.validate(schema=terraform_node_pool_schema)

        # 读取配置中的tf位置.
        # 读取配置中的资源名
        # 遍历tfstate, 读取node信息
        # 生成TerraformNode

        tfstate_path = self.raw_data["state_path"]
        resource_name = self.raw_data["resource_name"]
        username = self.raw_data["username"]
        sshkey = self.raw_data["sshkey"] if "sshkey" in self.raw_data else None
        password = self.raw_data["password"] if "password" in self.raw_data else None

        tfstate = read_tfstate(tfstate_path)
        host_infos = extract_host_info(tfstate, resource_name)
        result_node_list = []
        for host_info in host_infos:
            # 做一个检查,ip的取值选择: eip > public_ip > private_ip
            if "eip" in host_info and host_info["eip"] != "":
                ip = host_info["eip"]
            elif "public_ip" in host_info and host_info["public_ip"] != "":
                ip = host_info["public_ip"]
            elif "private_ip" in host_info and host_info["private_ip"] != "":
                ip = host_info["private_ip"]

            node = TerraformNode(
                id=host_info["id"],
                ip=ip,
                username=username,
                sshkey=sshkey,
                password=password,
                name=host_info["name"],
                tf_path=tfstate_path,
                resource_name=resource_name,
            )
            self.parse_meta(node)
            result_node_list.append(node)

        return result_node_list


# 读取Terraform状态文件
def read_tfstate(tfstate_path):
    with open(tfstate_path, "r") as file:
        tfstate = json.load(file)
    return tfstate


# 从.tfstate文件中提取ECS实例和EIP的信息
def extract_host_info(tfstate, ecs_resource_name):
    host_infos = []  # 存储ECS实例信息
    eip_associations = {}  # 存储EIP和ECS实例的关联信息

    # 遍历资源以提取ECS实例信息
    for resource in tfstate["resources"]:
        # 先搜索符合 ecs_resource_name 名的resource, 并且是'alicloud_instance'类型的resource
        if (
            resource["type"] == "alicloud_instance"
            and resource["name"] == ecs_resource_name
        ):
            # 一旦找到, 就将对应的instance信息, 存入host_infos中
            for instance in resource["instances"]:
                attributes = instance["attributes"]
                host_info = {
                    "id": attributes["id"],  # 实例ID
                    "name": attributes["instance_name"],  # 实例名称
                    "private_ip": attributes.get("private_ip", ""),  # 私有IP
                    "public_ip": attributes.get("public_ip", ""),  # 私有IP
                    "eip": "",  # EIP将在后续步骤中关联
                }
                host_infos.append(host_info)

    # 提取EIP与ECS实例的关联信息
    for resource in tfstate["resources"]:
        # 然后在所有的resource中, 寻找alicloud_eip_association类型的resource
        if resource["type"] == "alicloud_eip_association":
            # 一旦找到, 则把eip的信息都以instance_id为key存入 eip_associations中
            for instance in resource["instances"]:
                attributes = instance["attributes"]
                # 这里 allocation_id 就是eip的id
                # 形成一个  instance_id 和 allocation_id 的映射字典
                eip_associations[attributes["instance_id"]] = attributes[
                    "allocation_id"
                ]

    # 关联EIP到ECS实例
    for resource in tfstate["resources"]:
        # 找到eip类型的资源
        if resource["type"] == "alicloud_eip":
            # 遍历所有eip资源
            for instance in resource["instances"]:
                # 找到eip的 id 存入 allocation_id
                allocation_id = instance["attributes"]["id"]
                # 遍历局部变量host_infos中保存的instance信息, 根据id去找eip_associations中保存的eip连接信息,
                for host_info in host_infos:
                    # 一旦 eip_associations 中的 allocation_id 和 eip的id匹配, 就将对应的eip地址, 写入 host_info 中
                    if eip_associations.get(host_info["id"]) == allocation_id:
                        host_info["eip"] = instance["attributes"].get("ip_address", "")
    return host_infos
