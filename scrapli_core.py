
import logging

from scrapli import Scrapli
import q
#logging.basicConfig(level=logging.DEBUG, format='%(processName)s: %(message)s')


def login(config):
    try:
        connection = Scrapli(**config)
        connection.open()
        error_flag = False
    except Exception as e:
        print(f'Login Error!: {e}')
        error_flag = True
        connection = ''
    return connection, error_flag, config['host']


def logout(connect):
    connect.close()


# TODO: 実行結果にエラーがないか調べる機能も足したい
def send_command(connection, commands):
    try:
        output_list = list()
        if commands:
            for command in commands:
                res_command = connection.send_command(command=command)
                output_list.append(res_command.result)
        return output_list
    except Exception as e:
        print(f'Send Commnad Error!: {command} >> {e}')


def responce_command_to_text(device_name, commands, output_list):
    filename = f"output/{device_name}.log"
    with open(filename, mode='a') as f:
        for co, re in zip(commands, output_list):
            f.write("="*15 + co + "="*15 + "\n")
            f.write(f"{re}\n\n")
    print(f"* CREATE => {filename}")


def configure_replace_to_startup(connection):
    try:
        connection.send_command(command='configure replace nvram:startup-config list force')
    except Exception as e:
        print(f'Configure Replace Error!: {e}')


# スレッド処理の実行部分
def _run(config, commands):
    device = {
        "host": config['host'],
        "auth_username": config['auth_username'],
        "auth_password": config['auth_password'],
        "auth_strict_key": False,
        "platform": config['platform'],
        }

    net, error_flag, host = login(device)
    try:
        if not error_flag:
            res_command = send_command(net, commands)
            responce_command_to_text(config['device_name'],
                                     commands,
                                     res_command)
    finally:
        logout(net)
