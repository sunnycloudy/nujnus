from nujnus.common.error import NujnusError
import os


def _generate_provider_inventory_(provider_node, output_path):
    """
    # 输入1: python数据结构形式的 来自nujnus.yml的数据
    # 输入2: 生成的inventory的path
    # 输出: None
    """
    # 从文件中读取YAML内容

    inventory_content = ""

    if provider_node.sshkey != None and provider_node.sshkey != "":
        inventory_content = f"provider ansible_host={provider_node.ip} ansible_ssh_user={provider_node.username} ansible_ssh_private_key_file={provider_node.sshkey} ansible_ssh_port=22 ansible_become=true ansible_become_method=sudo\n"
    elif provider_node.password != None and provider_node.password != "":
        inventory_content = f"provider ansible_host={provider_node.ip} ansible_ssh_user={provider_node.username} ansible_ssh_pass={provider_node.password} ansible_ssh_port=22 ansible_become=true ansible_become_method=sudo\n"
    else:
        raise NujnusError(message="nujnus.yml的provider配置中缺少sshkey或password")

    # 将转换后的内容保存到指定的输出文件
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(inventory_content)
