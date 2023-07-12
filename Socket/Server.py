import socket
import time

print("服务端开启")
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 设置IP和端口
host = '192.168.137.104'
port = 2222
# bind绑定该端口

mySocket.bind((host, port))
mySocket.listen(10)


while True:
    # 接收客户端连接
    print("等待连接....")
    client, address = mySocket.accept()
    print("新连接")
    print("IP is %s" % address[0])
    print("port is %d\n" % address[1])
    while True:
        # 读取消息
        msg = client.recv(1024)
        # 把接收到的数据进行解码
        print(msg.decode("utf-8"))



        time.sleep(10)

        if msg == "over":
            client.close()
            mySocket.close()
            # 关闭数据库连接
            print("程序结束\n")
            exit()

