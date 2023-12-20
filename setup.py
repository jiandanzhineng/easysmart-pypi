import os

import setuptools
import time
import datetime

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

EASYSMART_VERSION = '20231220203851'
time_version = EASYSMART_VERSION
# time_version = datetime.datetime.now().strftime('%Y%m%d')

setuptools.setup(
    # 包的分发名称，使用字母、数字、_、-
    name="easysmart",
    # 版本号, 版本号规范：https://www.python.org/dev/peps/pep-0440/
    # version="0.0.5",
    version=time_version,
    # 作者名
    author="jiandanzhineng",
    # 作者邮箱
    author_email="jiandanzhineng@outlook.com",
    # 包的简介描述
    description="简单智能官方实现",
    # 包的详细介绍(一般通过加载README.md)
    long_description=long_description,
    # 和上条命令配合使用，声明加载的是markdown文件
    long_description_content_type="text/markdown",
    # 项目开源地址
    url="http://easysmart.top",
    # 如果项目由多个文件组成，我们可以使用find_packages()自动发现所有包和子包，而不是手动列出每个包，在这种情况下，包列表将是example_pkg
    packages=setuptools.find_packages(),
    install_requires=['paho-mqtt', 'zeroconf', 'requests'],
    # 关于包的其他元数据(metadata)
    classifiers=[
        # 该软件包仅与Python3兼容
        "Programming Language :: Python :: 3",
        # 根据MIT许可证开源
        "License :: OSI Approved :: MIT License",
        # 与操作系统无关
        "Operating System :: Microsoft :: Windows",
    ],
)
