import RPi.GPIO as GPIO
from time import sleep
import struct
from reedsolo import RSCodec


def str_2_bin(str):
    ## 字符串转换为二进制
    byte_string = RSCodec(10).encode(str.encode('utf-8'))
    binary_string = ''.join([bin(b)[2:].zfill(8) for b in byte_string])
    #binary = ''.join(format(ord(i), '08b') for i in str)
    #binary.replace('00000','000001')
    return '1111111110101010'+binary_string+'1010101011111111'
    #return ''.join([bin(ord(c)).replace('0b', '') for c in str])




GPIO.setmode(GPIO.BCM)

GPIO.setup(22, GPIO.OUT)

def sender(delay):
    while True:
        text = input("请输入：")
        signal = list(str_2_bin(text))
        for i in signal:
            if i == '1':
                GPIO.output(22, GPIO.LOW)
            elif i == '0':
                GPIO.output(22, GPIO.HIGH)
            sleep(delay)
                

sender(0.01)
