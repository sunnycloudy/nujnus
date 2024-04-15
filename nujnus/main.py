import click
from nujnus.command.cli.cli import (
    init,
    login,
    sendkey,
    config,
    get,
    scan,
    status,
    ls,
    tree,
    new,
    version,
    build,
    ssh_config,
    install,
    up,
    down,
    reload,
    remove,
    run,
    vars,
)


@click.group()
@click.pass_context
def cli(ctx):
    """使用说明

    \b
    init        创建nujnus目录
    config      进入节点对应的配置目录
    sendkey     ssh-copy-id到节点
    login       登录节点
    up          创建和启动节点, 若已经创建, 则仅启动节点
    down        关闭节点
    reload      重新载入节点
    remove      删除节点
    status      显示节点状态
    new         生成
    build       生成基于namespace和group的inventory文件
    run         根据commands.yml运行playbook
    """

    # 设置帮助文本的最大宽度为80字符
    ctx.max_content_width = 160


cli.add_command(tree)
cli.add_command(ls)
cli.add_command(build)  # 用来生成inventory.  # inventory名字
cli.add_command(config)
cli.add_command(init)
cli.add_command(login)
cli.add_command(get)
cli.add_command(scan)
cli.add_command(sendkey)
cli.add_command(ssh_config)
cli.add_command(status)
cli.add_command(new)  # 可能废弃
cli.add_command(install)
cli.add_command(version)
cli.add_command(run)
cli.add_command(vars)
cli.add_command(up)
cli.add_command(down)
cli.add_command(reload)
cli.add_command(remove)

# 未来增加一个export


if __name__ == "__main__":
    cli()
