#################################################################
# Netmiko並列実行
#
#################################################################
from scrapli import Scrapli
import logging
from dataclasses import dataclass

# logging.basicConfig(level=logging.DEBUG, format='%(processName)s: %(message)s')

@dataclass
class COMMAND_LIST:
    commands: list

def login(config):
    try:
        connection = Scrapli(**config)
        connection.open()
        error_flag=False
    except Exception as e:
        print(f'Login Error!: {e}')
        error_flag = True
        connection = ''
    return connection, error_flag, config['host']

def logout(connect):
    connect.close()

def send_command(connection, commands, host):
    try:
        output_list = list()
        if commands:
            for command in commands:
                res_command = connection.send_command(command=command)
                output_list.append(res_command.result)
    except Exception as e:
        print(f'Send Commnad Error!: {command} >> {e}')

    responce_command_to_text(host, commands, output_list)

def responce_command_to_text(host, commands,output_list):
    filename = f"output/{host}.log"
    with open(filename, mode='a') as f:
        for co, re in zip(commands,output_list):
            f.write("="*15 + co + "="*15 + "\n")
            f.write(f"{re}\n\n")
    print(f"* CREATE => {filename}")

# NOTE: ConfigureReplaceコマンドの実装
def configure_replace_to_startup(connection):
    try:
        connection.send_command(command='configure replace nvram:startup-config list force')
    except Exception as e:
        print(f'Configure Replace Error!: {e}')

# スレッド処理の実行部分
def _run(config):
    net,error_flag, host = login(config)
    try:
        if not error_flag:
            commands = [
                "show run",
                "configure replace nvram:startup-config list force",
                "show run",
            ]
            send_command(net, commands, host)
    finally:
        logout(net)
