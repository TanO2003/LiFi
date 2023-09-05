import socket
import time
import tkinter as tk
from threading import Thread,Event

over_signal = Event()

def clinet_init(host_address, host_port):
    #套接字接口
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #设置ip和端口
    host = host_address
    port = host_port

    try:
        mySocket.connect((host,port))
        print("连接成功") ##连接到服务器
    except :                           
        print ('连接不成功')
    
    return mySocket
        
        
def send(mySocket, text, delay):
        #发送消息
    msg = text
    #编码发送
    mySocket.send(msg.encode("utf-8"))
    
    time.sleep(delay)
    
    if msg == "over":
        mySocket.close()
        exit()

global _mode
_mode = "stop"

def on_button_click(mode):
    global _mode
    _mode = mode


def create_button(root, text, mode):
    button = tk.Button(root, text=text, command=lambda: on_button_click(mode))
    button.pack(pady=5)


def on_closing():
    # 处理关闭窗口事件的代码
    over_signal.set()
    time.sleep(0.1)
    exit()




def button():
    try:
        root = tk.Tk()
        root.title("控制按钮")
        create_button(root, "启动", "start")
        create_button(root, "直行", "g")
        create_button(root, "左转", "l")
        create_button(root, "右转", "r")
        create_button(root, "停止", "stop")
        create_button(root, "左变道", "q")
        create_button(root, "右变道", "e")
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        root.destroy()
    except Exception:
        over_signal.set()
        time.sleep(0.1)
        exit()

def send_main():
    ip = '192.168.137.12'
    port = 6666


    # 发送数据
    
    mySocket = clinet_init(ip, port)

    try:
        global _mode
        while True:
            text = _mode
            send(mySocket, text, 0.001)
            #print(_mode)
            time.sleep(0.01)
            if over_signal.is_set():
                send(mySocket, 'over', 0.001)
                exit()
    except Exception:
        exit()

if __name__ == '__main__':
    t1 = Thread(target=send_main)
    t2 = Thread(target=button)
    t1.daemon = True
    t2.daemon = True
    t2.start()
    t1.start()
    t1.join()
    t2.join()
    

