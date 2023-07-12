import RPi.GPIO as GPIO
from time import sleep
import re

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

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.IN)

def receiver(delay):
    # 接收
    while True:
        a = ''
        i = 0
        while i < 2:
            a += str(GPIO.input(12))
            #print(a)
            sleep(delay)
            if a[-8:] == "10000001":
                i += 1
            #print(i)
        #print(a)
        print(bin_2_str(a))

receiver(0.5)
