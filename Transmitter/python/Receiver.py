import RPi.GPIO as GPIO
from time import sleep
import re
import numpy as np
from functools import reduce
import operator as op


def Haming_decode(text):
    bits = np.array(list(text), dtype=int)
    position = reduce(op.xor, [i for i, bit in enumerate(bits) if bit])
    bits[position] = str(int(not(int(bits[position]))))
    return ''.join(str(bits[i]) for i in (3, 5, 6, 7))


def bin_2_str(bin):
    # 二进制转换为字符串
    
    messages=bin[:-10]
    position=messages.rfind('100100100')
    messages=messages[position+9:]
    try:
        messages_list=[Haming_decode(messages[i:i+8]) for i in range(0, len(messages), 8)]
        messages=''.join(messages_list)
        messages.replace('000001','00000')
        string=''
        bytes_list = re.findall('.{8}', messages)
        for byte in bytes_list:
            string += chr(int(byte, 2))
        return string
    except Exception:
        print("Error！")
        return -1


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
