# 用python启动一个http本地服务器
import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
    
# http://127.0.0.1:8000/
# http://localhost:8000/
# http://192.168.1.100:8000/
# http://192.168.1.100:8000/index.html