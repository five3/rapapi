#!/usr/bin/env python
# coding=utf-8
from setuptools import setup, find_packages
from RapAPI import __version__
# http://www.cnblogs.com/UnGeek/p/5922630.html
# http://blog.konghy.cn/2018/04/29/setup-dot-py/
# python setup.py sdist
# python setup.py bdist
# python setup.py bdist_egg
# python setup.py bdist_wheel
setup(
    name="RapAPI",
    version=__version__,
    keywords=["API Testing", "HTTP Recording", "HTTP Replay"],
    description="Record And Replay API Tool",
    long_description="The Tool can be use to Record and Replay API request for API testing without write script by human",
    license="GPL V3",

    url="https://github.com/five3/rapapi",
    author="five3",
    author_email="five3@163.com",

    package_dir={'RapAPI': 'RapAPI'},         # 指定哪些包的文件被映射到哪个源码包
    packages=['RapAPI'],       # 需要打包的目录。如果多个的话，可以使用find_packages()自动发现
    include_package_data=True,
    package_data={'RapAPI': ['static/*', 'templates/*']},
    py_modules=[],          # 需要打包的python文件列表
    data_files=[    # 打包时需要打包的数据文件
        'RapAPI/static/images/favicon.png',
        'RapAPI/templates/index.html'
    ],
    platforms="any",
    install_requires=[      # 需要安装的依赖包
        'mitmproxy>=4.0.4',
        'pymongo>=3.7.2',
        'flask>=1.0.2',
        'gunicorn>=19.9.0',
        'gevent>=1.4.0',
        'threadpool>=1.3.2'
    ],
    scripts=[],             # 安装时需要执行的脚本列表
    entry_points={
        'console_scripts': [    # 配置生成命令行工具及入口
            'rapapi.replay = RapAPI:replay',
            'rapapi.web = RapAPI:web',
            'rapapi.record = RapAPI:record'
        ]
    },
    classifiers=[           # 程序的所属分类列表
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    zip_safe=False
)
