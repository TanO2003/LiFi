import socket
import time

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