import RPi.GPIO as GPIO
from time import sleep
from daqhats_utils import select_hat_device, enum_mask_to_string
from daqhats import mcc118, OptionFlags, HatIDs, HatError
import re

def bin_2_str(bin):
    # 二进制转换为字符串
    messages=re.findall('10000001(.*?)10000001',bin)
    for message in messages:
        message.replace('000001','00000')
    string=''
    for message in messages:
        bytes_list = re.findall('.{8}', message)
        for byte in bytes_list:
            string += chr(int(byte, 2))
    return string
    #return ''.join([chr(i) for i in [int(b, 2) for b in bin.split('')]])

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.IN)
'''
def receiver(delay):
    # 接收
    while True:
        a = ''
        i = 0
        while i < 2:
            a += str(GPIO.input(12))
            #print(a)
            sleep(delay)
            if a[-8:] == "10000001":
                i += 1
            #print(i)
        #print(a)
        print(bin_2_str(a))

receiver(0.5)
'''

delay = 0.5

options = OptionFlags.DEFAULT
low_chan = 0
high_chan = 3
mcc_118_num_channels = mcc118.info().NUM_AI_CHANNELS
sample_interval = 0.5  # Seconds
light_index = 0

value = hat.a_in_read(1, options)
light_index = 100 - round(value * 1000 / 50)

while True:
        a = ''
        i = 0
        while i < 2:
            value = hat.a_in_read(1, options)
            light_index = 100 - round(value * 1000 / 50)
            if light_index > 50:
                a += '1'
            else:
                a += '0'

            #a += str(GPIO.input(12))
            #print(a)
            sleep()
            if a[-8:] == "10000001":
                i += 1
            #print(i)
        #print(a)
        print(bin_2_str(a))
