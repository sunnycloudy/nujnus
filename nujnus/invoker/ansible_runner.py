import os
import ansible_runner
import logging

from datetime import datetime
import json


def run_ansible_playbook(
    playbook_path, inventory_path, logname, extravars=None, limit=None
):
    # 如果没有日志名, 日志名就设为default
    if not logname:
        logname = "default"

    # 配置日志
    logging.basicConfig(
        filename="logs/{}.log".format(logname),
        level=logging.INFO,
        format="%(message)s",
    )
    logger = logging.getLogger()

    def del_keys_if_exist(keylist, data):
        for key in keylist:
            if key in data:
                del data[key]
        return data

    # 日志处理函数:
    def event_handler(event_data):
        try:
            # 提取主要的信息
            event_data_cared = event_data["event_data"]

            # 过滤掉不关心的字段
            event_data_cared = del_keys_if_exist(
                ["playbook_uuid", "uuid", "play_uuid", "task_uuid"], event_data_cared
            )

            if event_data["event"] in [
                "playbook_on_start",
                "runner_on_start",
                "playbook_on_task_start",
            ]:
                pass  # 过滤掉不关心的事件
            else:  # 记录下关心的事件

                # 获取当前时间
                now = datetime.now()
                # 格式化时间字符串，包括毫秒
                formatted_time = now.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
                event_data_cared = {
                    "time": formatted_time,
                    "playbook": event_data_cared["playbook"],
                    "event": event_data["event"],
                    **event_data_cared,
                }
                formatted_json_str = json.dumps(
                    event_data_cared, ensure_ascii=False, indent=4
                )

                logger.info(formatted_json_str + "\n,\n")
        except Exception as e:
            print(f"日志异常")

    # os.environ['ANSIBLE_NOCOLOR'] = '1'

    # 执行 Playbook
    if limit:
        r = ansible_runner.run(
            private_data_dir=".",
            playbook=playbook_path,
            inventory=inventory_path,
            limit=limit,
            extravars=extravars,
            event_handler=event_handler,
            # ident='4', json_mode=True,
        )
    else:
        r = ansible_runner.run(
            private_data_dir=".",
            playbook=playbook_path,
            inventory=inventory_path,
            extravars=extravars,
            event_handler=event_handler,
            # ident='4', json_mode=True,
        )

    ## 检查执行状态
    # if r.status == "successful":
    #    logging.info("Playbook 运行成功")
    # else:
    #    logging.error(f"Playbook 运行失败，状态：{r.status}")

    ## 打印详细执行结果
    # for each_host_event in r.events:
    #    logging.info(each_host_event["event"])


def run_builtin_playbook(playbook_path, extravars, inventory_path, nodename=None):

    run_ansible_playbook(
        playbook_path=playbook_path,
        inventory_path=inventory_path,
        extravars=extravars,
        logname=nodename,
    )
