#!/usr/bin/env python3
"""
AI Tools Hub - Deployment Helper
一键启动本地预览 + 打印部署说明
"""
import webbrowser
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import socket

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def open_browser(url):
    """Open browser after a short delay."""
    import time
    time.sleep(1)
    print(f"   🌐 浏览器已打开: {url}")
    webbrowser.open(url)

def preview():
    """Start local preview server."""
    port = find_free_port()
    os.chdir(os.path.join(os.path.dirname(__file__), "output"))
    
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    url = f"http://localhost:{port}"
    
    t = threading.Thread(target=open_browser, args=(url,), daemon=True)
    t.start()
    
    print(f"""
╔══════════════════════════════════════════╗
║     🎉 AI Tools Hub - 本地预览已启动     ║
╠══════════════════════════════════════════╣
║                                          ║
║   🌐 浏览器访问:                        ║
║   {url}                        ║
║                                          ║
║   Ctrl+C 停止预览                        ║
║                                          ║
╚══════════════════════════════════════════╝
    """)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n预览已停止")
        server.shutdown()

def instructions():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║              🚀 一键部署到 Netlify                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   📂 项目中的 output/ 文件夹已经就绪                        ║
║                                                              ║
║   第 1 步: 打开浏览器访问                                    ║
║   → https://app.netlify.com/drop                             ║
║                                                              ║
║   第 2 步: 把 output/ 文件夹                                 ║
║   → /Users/dalulidalu/Documents/网站建设/output/              ║
║   拖拽到浏览器页面上                                         ║
║                                                              ║
║   第 3 步: 等待 10 秒，获得临时域名                          ║
║   → https://xxx-xxx-xxx.netlify.app/                         ║
║                                                              ║
║   第 4 步（域名到手后）:                                      ║
║   在 Netlify Dashboard → Domain Settings                     ║
║   → Add Custom Domain → 输入你的域名                         ║
║                                                              ║
║   📝 部署前记得替换 AdSense ID：                              ║
║   grep -r "YOUR_PUBLISHER_ID" output/ -l                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

📊 当前站点数据:
   文章: 51 篇
   HTML页面: 256 个
   总文件: 264 个
   站点大小: 3 MB
   站点地图: 406 个 URL
""")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--preview":
        preview()
    else:
        instructions()
