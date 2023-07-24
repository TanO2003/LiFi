import RPi.GPIO as GPIO
from time import sleep
import re

def bin_2_str(bin):
    # 二进制转换为字符串
    messages=bin[:-10]
    #print(messages)
    position=messages.rfind('10101010')
    messages=messages[position+8:]
    print(messages)
    #messages=re.findall('10101010(.*?)10101010',bin)
    messages.replace('000001','00000')
    string=''
    bytes_list = re.findall('.{8}', messages)
    for byte in bytes_list:
        string += chr(int(byte, 2))
    return string
    #return ''.join([chr(i) for i in [int(b, 2) for b in bin.split('')]])

GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.IN)

def receiver(delay):
    # 接收
    while True:
        a = ''
        while 1:
            a += str(GPIO.input(6))
            sleep(delay)
            if a[-10:] == "1010101011":
                break
            #print(i)
        #print(a)
        print(bin_2_str(a))

receiver(0.005)
