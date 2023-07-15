import RPi.GPIO as GPIO
from time import sleep
import re
import CarRun
import Server



#光敏电阻引脚定义
LdrSensorLeft = 7
LdrSensorRight = 6
Ldr = LdrSensorRight
GPIO.setmode(GPIO.BCM)
GPIO.setup(Ldr, GPIO.IN)
ip = '169.254.87.109'
port = 2000
delay = 0.01
        
try:
    CarRun.motor_init()
    client = Server.server_init(ip, port)
    while True:
        move = Server.receive(client, delay)
        #print(move)
        global move_num
        if move == 'run':
            CarRun.run(0.5)
        elif move == 'back':
            CarRun.back(0.5)
        elif move == 'left':
            CarRun.run(0.4)
            CarRun.left(0.5)
        elif move == 'right':
            CarRun.run(0.4)
            CarRun.right(0.5)
        elif move == 'stop':
            CarRun.brake(0.5)
            
except KeyboardInterrupt:
    pass
CarRun.destroy()