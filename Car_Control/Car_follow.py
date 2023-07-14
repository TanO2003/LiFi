import RPi.GPIO as GPIO
from time import sleep
import re
import CarRun




#光敏电阻引脚定义
LdrSensorLeft = 7
LdrSensorRight = 6
Ldr = LdrSensorRight
GPIO.setmode(GPIO.BCM)
GPIO.setup(Ldr, GPIO.IN)

def bin_2_str(bin):
    # 二进制转换为字符串
    messages = re.findall('1010(.*?)1010',bin)

    string = ""
    print(messages)

    for message in messages:
        bytes_list = re.findall('.{4}', message)
        for byte in bytes_list:
            string += chr(int(byte, 2))

    
    return string
    #return ''.join([chr(i) for i in [int(b, 2) for b in bin.split('')]])


def receiver(delay):
    # 接收
    while True:
        a = ''
        i = 0
        while i < 2:
            a += str(GPIO.input(Ldr))
            sleep(delay)
            if a[-4:] == "1010":
                i += 1
        return bin_2_str(a)





try:
    CarRun.motor_init()
    while True:
        '''
        move = receiver(0.1)
        if move == '0':
            sleep(0.5)
            CarRun.run(0.5)
        elif move == '1':
            sleep(0.5)
            CarRun.back(0.5)
        elif move == '2':
            sleep(0.5)
            CarRun.left(0.5)
        elif move == '3':
            sleep(0.5)
            CarRun.right(0.5)
        elif move == '4':
            sleep(0.5)
            CarRun.brake(0.5)
        '''

        if GPIO.input(Ldr) == 0:
            CarRun.run(0.5)
        else:
            CarRun.brake(0.5)
except KeyboardInterrupt:
    pass
CarRun.destroy()
GPIO.cleanup()
