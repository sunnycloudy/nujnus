from nujnus.yml_parser.schema import meta_schema

# 执行和获取对应的name和ip, 这个name和对应instance_name可以不一致, 只是一个操作目标的名字.
# 不同的云解析操作可以不同.
terraform_node_pool_schema = {
    "type": {
        "type": "string",
        "required": True,
    },
    "state_path": {"type": "string", "required": True},
    "resource_name": {"type": "string", "required": True},
    "username": {"type": "string", "required": True},
    "sshkey": {"type": "string", "required": True},
    "password": {"type": "string", "required": True},
    "meta": meta_schema,
}
