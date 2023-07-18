import numpy as np
from reedsolo import RSCodec
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

def str_2_bin(str):
    ## 字符串转换为二进制
    binary = ''.join(format(ord(i), '08b') for i in str)
    binary.replace('00000','000001')
    return '10000001'+binary+'10000001'
'''
text = 'abc'
binary = str_2_bin(text)

ecc = RSCodec(10)
print(binary)
data = ecc.encode([int(i) for i in binary])
print(bytes(data))
deco = ecc.decode(data)

print(deco)
'''
text = 'abc'

byte_string = RSCodec(10).encode(text.encode('utf-8'))
binary_string = ''.join([bin(b)[2:].zfill(8) for b in byte_string])
print(binary_string)


binary_list = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
byte_string = bytes([int(b, 2) for b in binary_list])
print(byte_string)
print(RSCodec(10).decode(byte_string)[0].decode('utf-8'))

