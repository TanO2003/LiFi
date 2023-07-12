import RPi.GPIO as GPIO
from time import sleep
import struct

def str_2_bin(str):
    ## 字符串转换为二进制
    #binary = ''.join(format(ord(i), '08b') for i in str)
    binary = ""
    for i in str:
        _bin = bin(int(i))[2:]
        if len(_bin) != 4:
            _bin = '0'*(4-len(_bin)%4)+_bin
        binary += _bin
    return '1010'+binary+'1010'
    #return ''.join([bin(ord(c)).replace('0b', '') for c in str])




GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)

def sender(delay):
    while True:
        text = str(input("请输入："))
        signal = list(str_2_bin(text))
        #print(signal)
        for i in signal:
            if i == '1':
                GPIO.output(11, GPIO.LOW)
            elif i == '0':
                GPIO.output(11, GPIO.HIGH)
            sleep(delay)
                

sender(0.5)
