import re
def str_2_bin(str):
    ## 字符串转换为二进制
    binary = ''.join(format(ord(i), '08b') for i in str)
    binary.replace('11111','111110')
    return '01111110'+binary+'01111110'
def bin_2_str(bin):
    # 二进制转换为字符串
    messages=re.findall('01111110(.*?)01111110',bin)
    for message in messages:
        message.replace('111110','11111')
    string=''
    for message in messages:
        bytes_list = re.findall('.{8}', message)
        for byte in bytes_list:
            string += chr(int(byte, 2))
    return string
    #return ''.join([chr(i) for i in [int(b, 2) for b in bin.split('')]])
str='hello world'
str1='nihao'
#a='00000'+str_2_bin(str)
a=str_2_bin(str)
a=a+'00000'
a+=str_2_bin(str1)
a='000000'+a+'00000'
print(a)
b=bin_2_str(a)
print(b)