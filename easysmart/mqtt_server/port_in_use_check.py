import socket
import subprocess
import platform


def check_port_in_use(port):
    system = platform.system()
    print(f"尝试使用socket方式检查端口:{port}")
    check_dict = {}
    is_port_in_use = False

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', port))
        sock.close()
        check_dict["Socket"] = False
    except socket.error:
        # print(f"socket检查无法使用端口号{port}，可能被占用")
        check_dict["Socket"] = True
        is_port_in_use = True  # 如果出现socket错误，标记端口被占用

    print(f"尝试使用命令行方式检查端口:{port}")

    # 对于Unix-like系统（包括macOS和Linux），尝试使用lsof命令
    if system in ["Linux", "Darwin"]:
        print("system in [Linux, Darwin]")
        command = f'lsof -i :{port}'
        output = subprocess.check_output(command, shell=True, text=True)
        result = bool(output.strip())
        check_dict["Command_Line_lsof"] = result
        is_port_in_use |= result  # 如果lsof检查结果显示端口被占用，更新标志位

    # 对于Windows系统
    elif system == "Windows":
        print("system == Windows")
        command = f"netstat -ano | findstr :{port}"
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        result = bool(output.stdout.strip())
        check_dict["Command_Line_netstat"] = result
        is_port_in_use |= result  # 如果netstat检查结果显示端口被占用，更新标志位
    else:
        print("system == None")
        raise ValueError(f"Unsupported operating system: {system}")

    # 返回端口占用情况字典及是否被占用的布尔值
    return check_dict, is_port_in_use


# 示例
port_to_check = 1883
check_info, is_port_used = check_port_in_use(port_to_check)
print(check_info)
print("端口是否使用:", is_port_used)