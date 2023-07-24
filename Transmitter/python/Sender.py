import RPi.GPIO as GPIO
from time import sleep
import struct

def str_2_bin(str):
    ## 字符串转换为二进制
    binary = ''.join(format(ord(i), '08b') for i in str)
    binary.replace('00000','000001')
    print(binary)
    return '1110101010'+binary+'1010101011'
    #return ''.join([bin(ord(c)).replace('0b', '') for c in str])




GPIO.setmode(GPIO.BCM)
IN1 = 22
IN2 = 27
IN3 = 24
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)

def sender(delay):
    while True:
        text = input("请输入：")
        signal = list(str_2_bin(text))
        #signal = list('10000001'+text+'10000001')
        for i in signal:
            if i == '1':
                GPIO.output(IN3, GPIO.LOW)
                GPIO.output(IN2, GPIO.LOW)
                GPIO.output(IN1, GPIO.LOW)
            elif i == '0':
                GPIO.output(IN3, GPIO.HIGH)
                GPIO.output(IN2, GPIO.HIGH)
                GPIO.output(IN1, GPIO.HIGH)
            sleep(delay)
                

sender(0.005)
