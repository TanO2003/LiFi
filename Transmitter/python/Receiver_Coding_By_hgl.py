import RPi.GPIO as GPIO
from time import sleep
import re

def bin_2_str(bin):
    # 二进制转换为字符串
    messages=re.findall('01111110(.*?)01111110',bin)
    for message in messages:
        message.replace('111110','11111')
    string=''
    for message in messages:
        bytes_list = re.findall('.{8}', message)
        for byte in bytes_list:
            string += chr(int(byte, 2))
    return string
    #return ''.join([chr(i) for i in [int(b, 2) for b in bin.split('')]])

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.IN)

while True:
    for i in range(7):
        a += str(GPIO.input(12))
        sleep(0.5)

    print(bin_2_str(a))


