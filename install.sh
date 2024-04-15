# 在 Python 项目中，python setup.py sdist 命令用于创建项目的源代码分发包（source distribution）。简单来说，这个命令会打包你的项目，包括所有的 Python 文件、模块、相关的元数据等，生成一个可以分发的压缩文件。这个压缩文件通常用于后续的安装或分发给其他用户。
# 
# sdist 的含义
# sdist：代表 "source distribution"，即源代码分发。它不仅包含源代码，还包括了项目的元数据（如作者、版本号等信息），以及一个 setup.py 文件，后者包含了包的安装指令和依赖关系。
# 使用 sdist 的目的
# 分发：通过创建一个 sdist，开发者可以轻松地将项目打包并分享给其他开发者或用户。其他人可以使用该分发包安装项目及其依赖。
# 安装：用户可以使用 pip 或其他安装工具，通过源代码分发包来安装项目。比如，使用 pip install package.tar.gz 命令安装一个 sdist 包。
# pip install . --upgrade
# pip install .：这个命令用于安装当前目录下的 Python 项目。. 指的是当前目录。如果在项目的根目录下执行这个命令，它会根据 setup.py 文件安装该项目及其所有依赖。
# --upgrade：这个选项告诉 pip 更新已安装的包到最新版本。如果不加这个选项，pip 会检查如果包已安装，则跳过安装步骤。加上 --upgrade，即使已安装，pip 也会尝试安装当前目录下的版本，从而更新到这个版本。
# 综上所述，python setup.py sdist 用于创建项目的源代码分发包，而 pip install . --upgrade 用于安装或更新当前目录下的项目。

python setup.py sdist
pip install . --upgrade