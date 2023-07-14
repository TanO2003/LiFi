import socket
import time


def server_init(host_address, host_port):
    # 套接字接口
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置IP和端口
    host = host_address
    port = host_port
    
    # bind绑定该端口
    mySocket.bind((host, port))
    mySocket.listen(10)

    return mySocket


def receive(mySocket, delay):
    while True:
        # 接收客户端连接
        client = mySocket.accept()[0]
        #print("新连接")
        #print("IP is %s" % address[0])
        #print("port is %d\n" % address[1])
        while True:
            # 读取消息, 把接收到的数据进行解码
            msg = client.recv(1024).decode("utf-8")
            
            time.sleep(delay)

            
            
            if msg == "over":
                client.close()
                mySocket.close()
                print("程序结束\n")
                exit()
            return msg
