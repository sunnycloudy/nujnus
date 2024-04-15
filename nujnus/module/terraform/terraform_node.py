from nujnus.node.node import Node
import subprocess
from nujnus.common.utils import *
from nujnus.invoker.ansible_runner import run_builtin_playbook


class TerraformNode(Node):

    def __init__(
        self,
        id,  # 来自于tfstate
        ip,  # 来自于tfstate
        username,  # 来自于nujnus.yml
        sshkey,  # 来自于nujnus.yml
        password,  # 来自于nujnus.yml
        name,  # 来自于tfstate
        tf_path,  # 来自于nujnus.yml
        resource_name,  # 来自于nujnus.yml
    ) -> None:
        super().__init__(ip, username, sshkey, password, name, provider_name=None)
        self.tf_path = tf_path
        self.resource_name = resource_name
        self.id = id
