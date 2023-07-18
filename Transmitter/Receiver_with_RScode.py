import RPi.GPIO as GPIO
from time import sleep
import re
from reedsolo import RSCodec

def bin_2_str(bin):
    # 二进制转换为字符串
    binary_string=re.findall('1111111110101010(.*?)1010101011111111',bin)
    
    '''
    for message in messages:
        message.replace('000001','00000')
    
    string=''
    for message in messages:
        bytes_list = re.findall('.{8}', message)
        for byte in bytes_list:
            string += chr(int(byte, 2))
    return string
    #return ''.join([chr(i) for i in [int(b, 2) for b in bin.split('')]])
    '''
    binary_string = ''.join(binary_string)
    binary_list = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    byte_string = bytes([int(b, 2) for b in binary_list])
    return RSCodec(10).decode(byte_string)[0].decode('utf-8')


GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.IN)

def receiver(delay):
    # 接收
    while True:
        a = ''
        i = 0
        while i < 2:
            a += str(GPIO.input(6))
            #print(a)
            sleep(delay)
            if a[-16:] == "1010101011111111":
                i += 1
            #print(i)
        #print(a)
        print(bin_2_str(a))

receiver(0.01)
