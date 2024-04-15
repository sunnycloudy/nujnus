#!/bin/bash

# 定义顶级目录
TOP_DIR="./"
SUB_DIR="${TOP_DIR}/nujnus"

# 创建子目录
mkdir -p "${SUB_DIR}"

# 创建所需的文件
touch "${SUB_DIR}/__init__.py"
touch "${SUB_DIR}/main.py"
touch "${TOP_DIR}/setup.py"
touch "${TOP_DIR}/README.md"

echo "目录结构和文件已成功创建在 ${TOP_DIR}"
