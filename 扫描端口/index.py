# 端口扫描工具，扫描s2.wemc.cc的1000-99999端口
import socket
target = 's2.wemc.cc'
start_port = 1000
end_port = 99999

for port in range(start_port, end_port+1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f'端口号： {port} 状态：打开')
        sock.close()
    except KeyboardInterrupt:
        print('程序被中断')
        break
    except socket.gaierror:
        print('无法解析IP地址，请检查你的DNS或Hosts文件')
        break
    except socket.error:
        print('程序无法连接到指定的服务器')
        break
print('扫描完成！')
