import socket
import time
import keyboard
import tkinter as tk
from threading import Thread

def get_key():
    event = keyboard.read_event()
    return event.name



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
_mode = "g"

def on_button_click(mode):
    global _mode
    _mode = mode


def create_button(root, text, mode):
    button = tk.Button(root, text=text, command=lambda: on_button_click(mode))
    button.pack(pady=5)


def button():
    root = tk.Tk()
    root.title("控制按钮")
    create_button(root, "启动", "i")
    create_button(root, "直行", "g")
    create_button(root, "左转", "l")
    create_button(root, "右转", "r")
    create_button(root, "停止", "s")
    root.mainloop()

def send_main():
    ip = '192.168.137.15'
    port = 2222


    # 发送数据
    
    mySocket = clinet_init(ip, port)

    try:
        global _mode
        while True:
            text = _mode
            if text == 'i':
                send(mySocket, text, 0.01)
                _mode = 'g'
            send(mySocket, text, 0.01)
            print(_mode)
            time.sleep(0.5)
    except KeyboardInterrupt:
        send(mySocket, 'over', 0.01)
        pass

if __name__ == '__main__':
    t1 = Thread(target=send_main)
    t2 = Thread(target=button)

    t2.start()
    t1.start()
    t1.join()
    t2.join()
    

