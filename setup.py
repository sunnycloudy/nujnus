from setuptools import setup, find_packages

# 定义一个空字典用来执行文件
package_info = {}
with open("nujnus/version.py") as f:
    exec(f.read(), package_info)

setup(
    name="nujnus",
    version=package_info["__version__"],
    packages=find_packages(),
    package_data={
        # 要在Python包中递归地包含nujnus/playbooks目录下的所有文件，
        # 你需要确保在setup.py文件的package_data字段中正确地指定了这些文件。
        # 你还可以通过使用MANIFEST.in文件来确保在构建和安装过程中这些文件被包括在内。
        "nujnus": ["module/vagrant/playbooks/**/*"],
    },
    entry_points={
        "console_scripts": [
            "nus=nujnus.main:cli",
            "sun=nujnus.main:cli",
            "nujnus=nujnus.main:cli",
            "sunjun=nujnus.main:cli",
            "nuj=nujnus.main:cli",
            "jun=nujnus.main:cli",
        ]
    },
    install_requires=[
        # <=：小于等于某个版本
        # >：大于某个版本
        # <：小于某个版本
        #!=：不等于某个版本
        # ~=：兼容版本。例如，~=2.2 相当于 >=2.2, ==2.*，意味着安装版本要大于等于2.2，但小于3.0。
        "click>=7.0",  # 指定click的版本
        "ansible-runner>=2.3.5",  # 指定click的版本
        #"ansible>=8.7.0",
        "ansible>=2.10.0",
        "cerberus>=1.3.5",
        "ruamel.yaml>=0.18.6",
    ],
)
