import RPi.GPIO as GPIO
from time import sleep
import re
import CarRun
from Receiver import receive, receiver_init







try:
    CarRun.motor_init()
    receiver_init()
    while True:
        move = receive(0.005)
        print(move)
        if move == 'w':
            sleep(0.5)
            CarRun.run(0.5,20)
        elif move == 's':
            sleep(0.5)
            CarRun.back(0.5,20)
        elif move == 'a':
            sleep(0.5)
            CarRun.left(0.5,60)
        elif move == 'd':
            sleep(0.5)
            CarRun.right(0.5,60)
        elif move == '0':
            sleep(0.5)
            CarRun.brake(0.5,60)
except KeyboardInterrupt:
    pass
CarRun.destroy()
GPIO.cleanup()
