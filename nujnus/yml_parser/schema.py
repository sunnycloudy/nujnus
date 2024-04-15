# (((这个优点是简单)))
# dependencies:
#    - name: xxxx
#      cmds:
#        - "nus run harbor install"
#        - "nus run nginx verifies "
#        - "nus run harbor verifies"
#    - name: xxxx
#      cmds:
#        - "nus run harbor install"
#        - "nus run nginx verifies "
#        - "nus run harbor verifies"


# command_dependencies = {
#    "type": "list",
#    "schema": {
#        "type": "dict",
#        "schema": {
#            "name": {"type": "string", "required": True},
#            "cmds": {"type": "list", "schema": {"type": "string", "required": True}},
#        },
#    },
# }


command_dependencies = {
    "type": "list",
    "schema": {
        "type": "dict",
        "schema": {
            "name": {"type": "string", "required": True},
            "do": {
                "type": "list",
                "schema": {
                    "type": "dict",
                    "schema": {
                        "namespace": {"type": "string", "required": True},
                        "cmd": {"type": "string", "required": True},
                    },
                },
            },
        },
    },
}

# (((这个优点是可以递归排查问题)))
# command_dependencies = {
#    "required": False,
#    "empty": True,
#    "type": "list",
#    "schema": {
#        "type": "dict",
#        "schema": {
#            "namespace": {"type": "string", "required": True},
#            "commands": {
#                "type": "list",
#                "schema": {"type": "string"},
#                "required": False,
#            },
#            "verify_commands": {
#                "type": "list",
#                "schema": {"type": "string"},
#                "required": False,
#            },
#        },
#    },
# }

one_command_schema = {
    "type": "dict",
    "schema": {
        "namespace": {"type": "string", "required": True},
        "command_name": {"type": "string", "required": True},
        "playbook": {"type": "string", "required": True},
        "inventory": {"type": "string", "required": True},
        "overwrite": {"type": "boolean", "required": True},
        "workdir": {"type": "string"},
        "desc": {"type": "string"},
        "args": {"type": "list", "schema": {"type": "string"}},
        "cfg": {"type": "string", "required": False},
        "roles_path": {"type": "string", "required": False},
        "log_path": {"type": "string", "required": False},
        "deps": command_dependencies,
    },
}


commands_schema = {
    "command_list": {
        "type": "list",
        "schema": {
            "anyof": [one_command_schema]
        },  # 这里anyof表示,元素符合任意一个子模式即可.
    }
}

meta_schema = {
    "required": False,
    "empty": True,
    "type": "list",
    "schema": {
        "type": "dict",
        "schema": {
            "namespace": {"type": "string"},
            "vars": {
                "type": "dict",
                "keysrules": {"type": "string"},
                "required": False,
            },
            "groups": {"type": "list", "schema": {"type": "string"}},
        },
    },
}

physical_resource_schema = {
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


before_text_schema = {
    "namespace": {"type": "string", "required": True},
    "before_txt": {"type": "string", "required": True},
}

after_text_schema = {
    "namespace": {"type": "string", "required": True},
    "after_txt": {"type": "string", "required": True},
}
