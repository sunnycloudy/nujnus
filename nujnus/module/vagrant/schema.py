from nujnus.yml_parser.schema import meta_schema

vagrant_resource_schema = {
    "ip": {
        "type": "string",
        "required": True,
        "regex": r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
    },
    "type": {
        "type": "string",
        "required": True,
    },
    "netdev": {"type": "string", "required": True},
    "provider": {"type": "string", "required": True},
    "name": {"type": "string", "required": True},
    "box_name": {"type": "string", "required": True},
    "cpu": {"type": "integer", "required": True},
    "memory": {"type": "integer", "required": True},
    "disk": {"type": "integer", "required": False},
    "username": {"type": "string", "required": True},
    "password": {"type": "string", "required": False},
    "sshkey": {"type": "string", "required": True},
    "path": {"type": "string", "required": True},
    "meta": meta_schema,
}

vagrant_provider_resource_schema = {
    "name": {"type": "string", "required": True},
    "ip": {
        "type": "string",
        "required": True,
        "regex": r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
    },
    "type": {
        "type": "string",
        "required": True,
    },
    "username": {"type": "string", "required": True},
    "password": {"type": "string", "required": False},
    "sshkey": {"type": "string", "required": True},
    "meta": meta_schema,
}
