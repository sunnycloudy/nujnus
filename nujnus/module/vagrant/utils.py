import subprocess
import click

def ssh_login_and_cd_to_dir(provider_node, path_to_known_hosts, cd_to_dir):

    ip, username, sshkey, password = (
        provider_node.ip,
        provider_node.username,
        provider_node.sshkey,
        provider_node.password,
    )

    if sshkey:
        # 构建SSH命令，附加切换目录的命令，并且使用-t选项强制分配伪终端
        command = f"ssh -t -i {sshkey} -o StrictHostKeyChecking=no -o UserKnownHostsFile={path_to_known_hosts} {username}@{ip} 'cd {cd_to_dir}; bash'"
        # 使用subprocess运行命令
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            click.echo(f"SSH连接失败: {e}")

    else:
        # 构建SSH命令，附加切换目录的命令，并且使用-t选项强制分配伪终端
        command = f"sshpass -p {password} ssh -t -o StrictHostKeyChecking=no -o UserKnownHostsFile={path_to_known_hosts} {username}@{ip} 'cd {cd_to_dir}; bash'"
        # 使用subprocess运行命令
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            click.echo(f"SSH连接失败: {e}")
