#import yaml
from cerberus import Validator
from nujnus.yml_parser.schema import commands_schema
from nujnus.common.error import NujnusError
from nujnus.common.utils import check_file_exists

from nujnus.common.ruamel_yaml_config import yaml

def load_commands_from_yaml(yaml_file):
    # 从YAML文件中加载命令
    check_file_exists(yaml_file)
    with open(yaml_file, "r") as file:
        data = yaml.load(file)

    validator = Validator(commands_schema)
    if validator.validate({"command_list": data}, commands_schema):

        return data
    else:
        raise NujnusError(message=validator.errors)

