def get_vagrant_extra_vars(node_list):

    extra_vars = []
    for node in node_list:
        sshkey = None
        if node.sshkey != None and node.sshkey != "":
            with open("{}.pub".format(node.sshkey), "r") as f:
                sshkey = f.read()
        extra_vars.append(
            {
                "ip": node.ip,
                "name": node.name,
                "username": node.username,
                "netdev": node.netdev,
                "cpu": node.cpu,
                "memory": node.memory,
                "box_name": node.box_name,
                "password": node.password,
                "sshkey": sshkey,
                "vagrant_base_path": node.path,
            }
        )
    return {"vagrants": extra_vars}
