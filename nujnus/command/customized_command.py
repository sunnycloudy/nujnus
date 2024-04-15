from nujnus.common.error import *
from functools import lru_cache
import subprocess
from nujnus.generator.generator import generate_ansible_command
import os
from collections import OrderedDict


class Do:
    def __init__(self, namespace, cmd):
        self.namespace = namespace
        self.cmd = cmd


class CustomizedCommandDeps:
    def __init__(self, name, do):
        self.name = name
        self.do = [Do(namespace=d["namespace"], cmd=d["cmd"]) for d in do]
        # 再通过do, 来搜索依赖的CustomizedCommand对象.
        self.dep_customize_commands = []

    def find_customize_commands(self):
        for d in self.do:
            self.dep_customize_commands.append(
                CustomizedCommand.find_command(
                    namespace=d.namespace, command_name=d.cmd
                )
            )


def print_cmd_tree(
    cmd,
    dep_name="",
    level=0,
    is_last=True,
):
    if cmd is None:
        return

    if level == 0:
        branch = ""
        print(
            " " * 8 * level + branch + "{}:{}".format(cmd.namespace, cmd.command_name)
        )

    else:
        # 连线符号
        branch = "└── " if is_last else "├── "

        # 打印当前节点值，并根据层级进行缩进
        print(
            " " * 8 * level
            + branch
            + "[{}]:{}:{}".format(dep_name, cmd.namespace, cmd.command_name)
        )
    # 递归打印子节点
    for dep in cmd.deps:
        for i, cmd in enumerate(dep.dep_customize_commands):
            is_last_child = i == len(dep.dep_customize_commands) - 1
            print_cmd_tree(cmd, dep.name, level + 1, is_last_child)


class CustomizedCommand:
    _instances = []

    def __init__(
        self,
        generated_namespace_path,
        desc,
        namespace,
        command_name,
        playbook,
        inventory,
        overwrite,
        workdir,
        log_path,
        roles_path,
        args,
        cfg,
        deps,
    ):
        self.generated_namespace_path = generated_namespace_path
        self.desc = desc
        self.namespace = namespace
        self.command_name = command_name
        self.playbook = playbook
        self.inventory = inventory
        self.overwrite = overwrite
        self.workdir = workdir
        self.log_path = log_path
        self.roles_path = roles_path
        self.args = args
        self.cfg = cfg
        self.deps = [
            CustomizedCommandDeps(name=dep["name"], do=dep["do"]) for dep in deps
        ]
        CustomizedCommand._instances.append(self)  # 创建实例时添加到_instances列表
        self.shell_command = None

    # 还需要一个类方法, 在所有CustomizedCommand初始化完后,
    # 来让deps找到依赖的CustomizedCommand对象.
    # 各个command assemble自己的deps
    @classmethod
    @lru_cache(maxsize=None)
    def assemble_all_deps(cls):
        for command in cls._instances:
            for dep in command.deps:
                dep.find_customize_commands()

    @classmethod
    @lru_cache(maxsize=None)
    def find_command(cls, namespace, command_name):
        for command in cls._instances:
            if command.namespace == namespace and command.command_name == command_name:
                return command
        raise NujnusError(
            message="commands.yml中未找到namespace:{}或command_name:{}".format(
                namespace, command_name
            )
        )

    def find_dep(self, name):
        for dep in self.deps:
            if dep.name == name:
                return dep
        raise NujnusError(message="没有找到名为{}的dep".format(name))

    def find_dep_or_not(self, name):
        for dep in self.deps:
            if dep.name == name:
                return dep
        return None

    @classmethod
    def print_all_tree(cls):
        for command in cls._instances:
            print_cmd_tree(cmd=command)

    def to_yaml(self):
        if len(self.args) > 0:
            args = "  args:\n"
            for arg in self.args:
                args = args + (f'    - "{arg}"\n')
        else:
            args = ""
        result = f"""# nus run {self.namespace} {self.command_name}
- desc: "{self.desc}"
  namespace: "{self.namespace}"
  command_name: "{self.command_name}"
  playbook: "{self.playbook}"
  inventory: "{self.inventory}"
  overwrite: {self.overwrite}
  roles_path: "{self.roles_path}"
  workdir: "{os.path.abspath(self.workdir)}"
  cfg: "{self.cfg}"
{args}"""
        return result

    def execute(self):
        # 生成命令
        ansible_command, workdir, env = generate_ansible_command(
            self.generated_namespace_path, self
        )
        print("#"+">"*19)
        print("#")
        print("#env:{}".format(env))
        print("#")
        print("#workdir:{}".format(workdir))
        print("#")
        print("#ansible_command:{}".format(ansible_command))
        print("#")
        print("#"+">"*19)
        # 执行ansible命令
        result = subprocess.run(ansible_command, cwd=workdir, env=env)
        if result.returncode != 0:
            raise NujnusError(message="出现了错误")
