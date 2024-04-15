# utils.py
import os
import shutil
import click
from nujnus.common.error import NujnusError
import subprocess


# 创建目录
def create_dir(base_path, name):
    """
    输入1: 路径
    输入2: 文件名
    输出: 拼接的路径
    """
    generated_path = os.path.join(base_path, name)
    os.makedirs(generated_path, exist_ok=True)
    return generated_path


def create_file(base_path, filename, content):
    file_path = os.path.join(base_path, filename)
    with open(file_path, "w") as file:
        file.write(content)
    return file_path

def append_file(base_path, filename, content):
    file_path = os.path.join(base_path, filename)
    with open(file_path, "a") as file:
        file.write(content)
    return file_path



def create_file_if_notexist(base_path, filename, content):
    file_path = os.path.join(base_path, filename)
    print(file_path)
    if os.path.exists(file_path):
        pass
    else:
        with open(file_path, "w") as file:
            file.write(content)
        return file_path


def check_directory_exists(directory_path):
    # 检查路径是否存在
    if os.path.exists(directory_path):
        # 检查这个路径是否确实是一个目录
        if os.path.isdir(directory_path):
            # raise NujnusError(message=f"目录 {directory_path} 已存在。")
            pass
        else:
            raise NujnusError(
                message=f"路径 {directory_path} 已存在，但这不是一个目录。"
            )


def check_file_exists_in_current_directory(file_name):
    # 获取当前目录的路径
    current_directory = os.getcwd()
    # 构建文件的完整路径
    file_path = os.path.join(current_directory, file_name)

    # 检查文件是否存在
    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            raise NujnusError(message=f"nujnus.yml文件不存在。")
    else:
        raise NujnusError(message=f"nujnus.yml文件不存在。")


def check_file_exists(file_path):
    # 检查文件是否存在
    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            raise NujnusError(message="{}文件不存在。".format(file_path))
    else:
        raise NujnusError(message="{}文件不存在。".format(file_path))


def overwrite(source_file_path, destination_file_path):

    check_file_exists(source_file_path)
    check_directory_exists(os.path.dirname(destination_file_path))

    # 使用'with'语句确保文件正确关闭
    # 首先，打开源文件读取内容
    with open(source_file_path, "r") as source_file:
        content = source_file.read()

    # 然后，打开目标文件写入内容，'w'模式会覆盖文件的原有内容
    with open(destination_file_path, "w") as destination_file:
        destination_file.write(content)


def copy_directory_to_inside(src, dst):
    # 确保源目录存在
    if not os.path.exists(src):
        print(f"Source directory {src} does not exist.")
        raise NujnusError

    # 创建目标子目录的完整路径（在dst目录内以src同名创建子目录）
    destination_subdir = os.path.join(dst, os.path.basename(src))

    # 如果目标子目录已存在，则先删除（可根据需要选择是否执行这步）
    if os.path.exists(destination_subdir):
        print(f"目标secrets目录已存在:\n{destination_subdir}")
        print(f"继续执行...")
        return

    # 复制整个源目录到目标子目录
    shutil.copytree(src, destination_subdir)
    print(f"Directory {src} was copied to {destination_subdir}.")
