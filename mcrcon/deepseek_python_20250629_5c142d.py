from mcrcon import MCRcon
import socket

def test_rcon_connection(host, port, password, timeout=5):
    """测试RCON连接是否成功"""
    try:
        with MCRcon(host, password, port, timeout=timeout) as mcr:
            # 发送空命令测试连接
            response = mcr.command("")
            return True, "RCON连接成功！"
    except socket.timeout:
        return False, f"连接超时：无法在{timeout}秒内连接到{host}:{port}"
    except ConnectionRefusedError:
        return False, f"连接被拒绝：请检查RCON服务是否运行在{host}:{port}"
    except Exception as e:
        return False, f"连接错误：{str(e)}"

def interactive_rcon_session(host, port, password):
    """交互式RCON会话"""
    try:
        with MCRcon(host, password, port, timeout=10) as mcr:
            print("已连接到RCON，输入命令（输入'exit'退出）：")
            while True:
                cmd = input(">>> ")
                if cmd.lower() == 'exit':
                    break
                try:
                    response = mcr.command(cmd)
                    print(f"服务器响应: {response}")
                except Exception as e:
                    print(f"命令执行错误: {str(e)}")
    except Exception as e:
        print(f"会话错误: {str(e)}")

if __name__ == "__main__":
    # 配置信息
    HOST = "play.simpfun.cn"
    PORT = 25575  # 如果使用Docker映射端口，请修改为实际映射端口
    PASSWORD = "zzx20110216"
    
    # 先测试连接
    print("正在测试RCON连接...")
    success, message = test_rcon_connection(HOST, PORT, PASSWORD)
    print(message)
    
    # 如果连接成功，进入交互模式
    if success:
        interactive_rcon_session(HOST, PORT, PASSWORD)
    else:
        print("请检查：")
        print("1. 服务器是否运行并开启了RCON")
        print("2. 端口和密码是否正确")
        print("3. 防火墙/安全组是否放行了该端口")
        print("4. 如果是Docker运行，是否正确映射了端口")