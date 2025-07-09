from mcrcon import MCRcon  
  
def check_minecraft_server(host, port, password):  
    # 确保 port 是一个整数  
    port = int(port)  # 如果 port 已经是整数，这行代码是安全的，但如果它是字符串，则会将其转换为整数  
    try:  
        with MCRcon(host, port, password) as rcon:  
            # 发送命令并获取结果  
            response = rcon.command("/list")  
            print(response)  
            # 解析响应以获取玩家数量（这里只是简单示例）  
            # 注意：这里的解析可能需要更复杂的逻辑  
            players_lines = response.strip().split('\n')  
            players_count = len(players_lines) - 2  # 假设每行一个玩家，但具体取决于响应格式  
            if players_count > 0:  
                print(f"当前在线玩家数量: {players_count}")  
            else:  
                print("没有在线玩家")  
    except Exception as e:  
        print(f"无法连接到服务器或执行命令: {e}")  
  
# 替换为你的服务器信息和密码  
host = 's2.wemc.cc:14259'  
port = 25575  # 确保这是整数，而不是字符串 '25575'  
password = 'zzx20110216'  
  
check_minecraft_server(host, port, password)
