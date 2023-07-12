import RPi.GPIO as GPIO
from time import sleep
import re

def bin_2_str(bin):
    # 二进制转换为字符串
    messages = re.findall('1010(.*?)1010',bin)

    string = ""
    print(messages)

    for message in messages:
        bytes_list = re.findall('.{4}', message)
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
            sleep(delay)
            if a[-4:] == "1010":
                i += 1
        print(bin_2_str(a))


receiver(0.5)
