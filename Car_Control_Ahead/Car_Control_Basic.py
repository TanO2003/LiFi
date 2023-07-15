import CarRun_Former as CarRun
import Server
import RPi.GPIO as GPIO
from time import sleep
from threading import Thread
#import Sender_number_only


R = 22
G = 27
B = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(R, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)
move_num = 0


def car_control(ip, port, delay):
    try:
        CarRun.motor_init()
        client = Server.server_init(ip, port)
        while True:
            move = Server.receive(client, delay)
            global move_num
            if move == 'w':
                
                move_num = 0
                GPIO.output(R, GPIO.HIGH)
                GPIO.output(G, GPIO.HIGH)
                GPIO.output(B, GPIO.HIGH)
                sleep(0.3)
                CarRun.run(0.5)
            elif move == 's':
                CarRun.back(0.5)
                move_num = 1
            elif move == 'a':
                CarRun.left(0.5)
                move_num = 2
            elif move == 'd':
                CarRun.right(0.5)
                move_num = 3
            elif move == 'space':
                
                move_num = 4
                GPIO.output(R, GPIO.LOW)
                GPIO.output(G, GPIO.LOW)
                GPIO.output(B, GPIO.LOW)
                sleep(0.3)
                CarRun.brake(0.5)
            
    except KeyboardInterrupt:
        pass
    CarRun.destroy()


def sent_info():
    try:
        while True:
            info = CarRun.get_info() 
            sleep(1)
            return info
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    ip = '192.168.137.30'
    port = 2222
    delay = 0.01
    car_control(ip, port, delay)

