.PHONY: install uninstall clean

# 安装脚本和卸载脚本的位置
INSTALL_SCRIPT = install.sh
UNINSTALL_SCRIPT = uninstall.sh
CLEAN_SCRIPT = clean.sh

# 安装命令
install:
	@bash $(INSTALL_SCRIPT)

# 卸载命令
uninstall:
	@bash $(UNINSTALL_SCRIPT)

# 清理命令，用于删除临时文件或构建文件等
clean:
	@bash $(CLEAN_SCRIPT)
