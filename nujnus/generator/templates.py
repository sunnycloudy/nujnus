commands_yml_content = """
- desc: "list kubespray tasks"
  namespace: "kubespray"
  command_name: "list"
  playbook: "/home/nujnus/workspace/workspace_for_devops/working/test/d2632bc5-311b-4ec5-85ae-390ab33b372e/generated/kubespray/playbooks/cluster.yml"
  inventory: "/home/nujnus/workspace/workspace_for_devops/working/test/d2632bc5-311b-4ec5-85ae-390ab33b372e/generated/kubespray/inventory/mycluster/inventory.ini"
  overwrite: True
  workdir: "/home/nujnus/workspace/workspace_for_devops/working/test/d2632bc5-311b-4ec5-85ae-390ab33b372e/generated/kubespray/"
  known_hosts: "./secrets/known_hosts"
  args:
    - "--list-tasks"
- desc: "kubespray check mode"
  namespace: "kubespray"
  command_name: "check"
  playbook: "/home/nujnus/workspace/workspace_for_devops/working/test/d2632bc5-311b-4ec5-85ae-390ab33b372e/generated/kubespray/playbooks/cluster.yml"
  inventory: "/home/nujnus/workspace/workspace_for_devops/working/test/d2632bc5-311b-4ec5-85ae-390ab33b372e/generated/kubespray/inventory/mycluster/inventory.ini"
  overwrite: True
  workdir: "/home/nujnus/workspace/workspace_for_devops/working/test/d2632bc5-311b-4ec5-85ae-390ab33b372e/generated/kubespray/"
  known_hosts: "./secrets/known_hosts"
  args:
    - "-C"
- desc: "kubespray install k8s"
  namespace: "kubespray"
  command_name: "install"
  playbook: "/home/nujnus/workspace/workspace_for_devops/working/test/d2632bc5-311b-4ec5-85ae-390ab33b372e/generated/kubespray/playbooks/cluster.yml"
  inventory: "/home/nujnus/workspace/workspace_for_devops/working/test/d2632bc5-311b-4ec5-85ae-390ab33b372e/generated/kubespray/inventory/mycluster/inventory.ini"
  overwrite: True
  workdir: "/home/nujnus/workspace/workspace_for_devops/working/test/d2632bc5-311b-4ec5-85ae-390ab33b372e/generated/kubespray/"
  known_hosts: "./secrets/known_hosts"
"""

verify_yml_content = """

# nujnus verify 会调用本文件
---
- name: Example playbook with assert
  hosts: vagrants
  tasks:
    - name: Assert condition example
      assert:
        that:
          - "1 == 1"
        success_msg: "Assertion passed, the condition is true."
        fail_msg: "Assertion failed, the condition is not true."

#---
#- name: Example playbook with assert
#  hosts: node1
#  tasks:
#    - name: Assert condition example
#      assert:
#        that:
#          - "1 == 1"
#        success_msg: "Assertion passed, the condition is true."
#        fail_msg: "Assertion failed, the condition is not true."

#---
#- name: Example playbook with assert
#  hosts: node1
#  tasks:
#    - name: Assert condition example
#      assert:
#        that:
#          - "1 == 1"
#        success_msg: "Assertion passed, the condition is true."
#        fail_msg: "Assertion failed, the condition is not true."
    """


gitignore_content = """

"""

nujnus_yml_content = """
- name: "server0"
  type: "PhysicalParser" # 可以是host, 也可以是provider
  ip: "192.168.121.55"
  username: "root"
  sshkey: "secrets/id_rsa"

- ip: "192.168.121.91"
  type: "VagrantResourceParser"
  provider: "server0"
  netdev: "enp2s0f0"
  name: "test1"
  cpu: 6
  memory: 8192
  username: "root"
  box_name: "generic_centos8"
  sshkey: "secrets/id_rsa"
  meta:
    - namespace: kubespray
      groups:
        - kube_control_plane
        - etcd
        - kube_node

- ip: "192.168.121.92"
  type: "VagrantResourceParser"
  provider: "server0"
  netdev: "enp2s0f0"
  name: "test2"
  box_name: "generic_centos8"
  cpu: 6
  memory: 8192
  username: "root"
  sshkey: "secrets/id_rsa"
  meta:
    - namespace: kubespray
      groups:
        - kube_control_plane
        - etcd
        - kube_node

- ip: "192.168.121.95"
  type: "VagrantResourceParser"
  provider: "server0"
  netdev: "enp2s0f0"
  name: "test3"
  box_name: "generic_centos8"
  cpu: 6
  memory: 8192
  username: "root"
  sshkey: "secrets/id_rsa"
  meta:
    - namespace: kubespray
      groups:
        - kube_control_plane
        - etcd
        - kube_node

- namespace: kubespray
  before_txt: |
    # 注释: 测试nujnus.yml

- namespace: kubespray
  after_txt: |
    [calico_rr]

    [k8s_cluster:children]
    kube_control_plane
    kube_node
    calico_rr
"""

example_yml = """
---
- name: 列出 /tmp 目录下的文件
  hosts: all
  tasks:
    - name: 使用 ls 命令列出 /tmp 目录内容
      ansible.builtin.command: ls /tmp
      register: ls_result

    - name: 打印 ls 命令的输出
      ansible.builtin.debug:
        msg: "{{ ls_result.stdout_lines }}"

"""

#    create_file(role_dir, "README.md", "")
#    create_file(defaults_dir, "main.yml", "")
#    create_file(var_dir, "main.yml", "")
#    create_file(meta_dir, "main.yml", "")
#
#    create_file(tasks_path, "main.yml", "")
#    create_file(tasks_path, "install.yml", "")
#    create_file(tasks_path, "uninstall.yml", "")
#    create_file(tasks_path, "backup.yml", "")
#    create_file(tasks_path, "restore.yml", "")
#    create_file(tasks_path, "start.yml", "")
#    create_file(tasks_path, "stop.yml", "")
#    create_file(tasks_path, "disable.yml", "")
#    create_file(tasks_path, "enable.yml", "")
#    create_file(tasks_path, "verification.yml", "")
#
#
#    create_file(handler_path, "main.yml", "")

task_main_sample = """---
# tasks file for simple_role
- name: Create a text file
  ansible.builtin.file:
    path: "/tmp/simple_role_test.txt"
    state: touch
"""

# ------------
role_invoker = """---
- name: 在主机{{nodename}}上调用role
  hosts: {{nodename}}
  become: yes
  vars:
    roles_to_include:
      - demo

  tasks:
    - name: Include role based on variable
      include_role:
        name: "{{ item }}"
      loop: "{{ roles_to_include }}"
"""


defaults_demo = """python_script_name: example.py
python_script_config_template: script_config.j2

"""
file_demo = """#!/usr/bin/env python
print("Hello from Python script!")
"""

template_demo = """[DEFAULT]
greeting = Hello from Python script with config!
"""

handlers_demo = """---
- name: python script run
  ansible.builtin.debug:
    msg: "Python script ran successfully"

- name: python script run with config
  ansible.builtin.debug:
    msg: "Python script with config ran successfully"
"""

tasks_demo = """---
- name: Copy Python script to target
  ansible.builtin.copy:
    src: "{{ python_script_name }}"
    dest: "/tmp/{{ python_script_name }}"
    mode: '0755'

- name: Generate script configuration
  ansible.builtin.template:
    src: "{{ python_script_config_template }}"
    dest: "/tmp/{{ python_script_name }}.config"

- name: Run Python script
  ansible.builtin.command:
    cmd: "python3 /tmp/{{ python_script_name }}"
  notify: python script run

- name: Run Python script with config
  ansible.builtin.shell:
    cmd: "python3 /tmp/{{ python_script_name }} /tmp/{{ python_script_name }}.config"
  notify: python script run with config
"""

handlers_demo = """---
- name: python script run
  ansible.builtin.debug:
    msg: "Python script ran successfully"

- name: python script run with config
  ansible.builtin.debug:
    msg: "Python script with config ran successfully"
"""

vars_demo = """# 可以在这里覆盖默认变量或定义新变量

"""

playbook_template = """---
- hosts: all
  roles:
    - {}

"""

print_vars_demo = """# print_vars/tasks/main.yml
- name: Print all host_vars for the current host
  debug:
    var: hostvars[inventory_hostname]
"""


commands_draft_content = """- desc: "install {rolename}"
  namespace: "<namespace>"
  command_name: "install"
  playbook: "{project_base}/playbooks/{rolename}.yml"
  inventory: "{project_base}/generated/<namespace>/inventory.ini"
  overwrite: True
  roles_path: "{project_base}/roles/"
  cfg: "{project_base}/generated/<namespace>/debug.cfg"
  workdir: "./"
"""
