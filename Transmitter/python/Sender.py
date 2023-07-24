import RPi.GPIO as GPIO
from time import sleep
import struct

def hamming_encode(data):
    # 将输入数据转换为列表形式
    data_list = [int(bit) for bit in data]
    
    # 确定校验位的值
    parity1 = (data_list[0] + data_list[1] + data_list[3]) % 2
    parity2 = (data_list[0] + data_list[2] + data_list[3]) % 2
    parity3 = (data_list[1] + data_list[2] + data_list[3]) % 2
    
    # 构建编码后的数据
    encoded_data = [parity1, parity2, data_list[0], parity3, data_list[1], data_list[2], data_list[3]]
    return '0'+''.join(str(bit) for bit in encoded_data)


def str_2_bin(str):
    ## 字符串转换为二进制
    binary = ''.join(format(ord(i), '08b') for i in str)
    binary.replace('00000','000001')
    encode = [hamming_encode(binary[i:i+4]) for i in range(0, len(binary), 4)]
    encode_str = ''.join(i for i in encode)
    bin_data = '11100100100'+encode_str+'1010101011'
    
    return bin_data





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
