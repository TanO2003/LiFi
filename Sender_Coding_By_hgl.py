import RPi.GPIO as GPIO
from time import sleep
import struct

def str_2_bin(str):
    ## 字符串转换为二进制
    binary = ''.join(format(ord(i), '08b') for i in str)
    binary.replace('11111','111110')
    return '01111110'+binary+'01111110'
    #return ''.join([bin(ord(c)).replace('0b', '') for c in str])

text = input("请输入：")
signal = list(str_2_bin(text))


GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)

while True:
    for i in signal:
        if i == '1':
            GPIO.output(11, GPIO.LOW)
            sleep(0.5)
        elif i == '0':
            GPIO.output(11, GPIO.HIGH)
            sleep(0.5)
    sleep(3)