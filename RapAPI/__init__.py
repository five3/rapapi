import os
import sys
import getopt
from subprocess import call

from .api import *


__version__ = '0.1.{buildno}'


def usage():
    print(
f"""
Usage: {sys.argv[0]} [option]
-h or --help：显示帮助信息

[rapapi.record] optisons
-s or --script：插件脚本   例如：rapapi.record -s script.py
-p or --port：代理端口   例如：rapapi.record -p 8181
-u or --url-prefix：录制url前缀  例如：rapapi.record -u https://vr.api.autohome.com.cn/api
-v or --version：显示版本
"""
    )


port = '8181'
url_prefix = 'https://vr.api.autohome.com.cn/api'
script = os.path.join(os.path.dirname(__file__), "recorder.py")
try:
    opts, args = getopt.getopt(sys.argv[1:], "vhkp:u:s:", ["version", "help", "port=", "url-prefix=", "script="])

    for cmd, arg in opts:
        if cmd in ("-h", "--help"):
            usage()
            sys.exit()
        elif cmd in ("-p", "--port"):
            port = arg
        elif cmd in ("-u", "--url-prefix"):
            url_prefix = arg
        elif cmd in ("-s", "--script"):
            script = arg
        elif cmd in ("-v", "--version"):
            print(f"{sys.argv[0]} version {__version__}")
            exit(0)
except getopt.GetoptError as e:
    print(f"argv error, {e}")
    usage()


def replay():
    results = RunWithDebug.apply_all()
    print(f'Length of Results: {len(results)}')
    print(results)


def web():
    pass


def record():
    command = f'mitmdump -s {script} -k -p {port} "~u ^{url_prefix}.+"'
    print(f'Command: {command}')
    call(["mitmdump", "-s", script, "-k", "-p", port, f'"~u ^{url_prefix}.+"'])
