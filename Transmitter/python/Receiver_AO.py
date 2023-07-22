from time import sleep
import re
from Voltage_to_Digital import V2D

def bin_2_str(bin):
    # 二进制转换为字符串
    messages=re.findall('10000001(.*?)10000001',bin)
    for message in messages:
        message.replace('000001','00000')
    string=''
    for message in messages:
        bytes_list = re.findall('.{8}', message)
        for byte in bytes_list:
            string += chr(int(byte, 2))
    return string
    #return ''.join([chr(i) for i in [int(b, 2) for b in bin.split('')]])





def receiver(delay):
    # 接收
    while True:
        print(bin_2_str(V2D(1,1,delay)))

receiver(0.5)
