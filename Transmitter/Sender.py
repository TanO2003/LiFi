import RPi.GPIO as GPIO
from time import sleep
import struct

def str_2_bin(str):
    ## 字符串转换为二进制
    binary = ''.join(format(ord(i), '08b') for i in str)
    binary.replace('00000','000001')
    return '10000001'+binary+'10000001'
    #return ''.join([bin(ord(c)).replace('0b', '') for c in str])




GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)

def sender(delay):
    while True:
        text = input("请输入：")
        signal = list(str_2_bin(text))
        for i in signal:
            if i == '1':
                GPIO.output(11, GPIO.LOW)
            elif i == '0':
                GPIO.output(11, GPIO.HIGH)
            sleep(delay)
                

sender(0.5)
