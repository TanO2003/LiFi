import socket
import time
from threading import Event

start_signal = Event()
over_signal = Event()

def server_init(host_address, host_port):
    # 套接字接口
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置IP和端口
    host = host_address
    port = host_port
    
    # bind绑定该端口
    mySocket.bind((host, port))
    mySocket.listen(10)

    return mySocket.accept()[0]


def receive(client, delay):


    while True:
        # 读取消息, 把接收到的数据进行解码
        msg = client.recv(1024).decode("utf-8")
        
        time.sleep(delay)


        if msg == 'start':
            start_signal.set()
            return 'g'
        
        if msg == 'stop':
            start_signal.clear()
            return msg

        if msg == "over":
            client.close()
            over_signal.set()
            #mySocket.close()
            print("程序结束\n")
            exit()
        return msg