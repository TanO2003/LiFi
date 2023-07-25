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
        mySocket.connect((host, port))
        print("连接成功") ##连接到服务器
    except :                           ##连接不成功，运行最初的ip
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


def send_main(ip, port):
    mySocket = clinet_init(ip, port)
    try:
        while True:
            global _mode
            text = _mode
            send(mySocket, text, 0.01)
    except KeyboardInterrupt:
        send(mySocket, 'over', 0.01)
        pass



if __name__ == '__main__':
    ip = '192.168.137.6'
    port = 2222
    root = tk.Tk()
    root.title("控制按钮")

    create_button(root, "直行", "w")
    create_button(root, "左转", "a")
    create_button(root, "右转", "d")
    create_button(root, "停止", "space")

    t2 = Thread(target=send_main, args=(ip, port))
    t2.start()
    root.mainloop()

