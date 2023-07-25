import CarRun_Former as CarRun
import Server
import RPi.GPIO as GPIO
from time import sleep
from threading import Thread
from Sender import send, sender_init


R = 22
G = 27
B = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(R, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)
move_num = 'init'


def car_control(ip, port, delay):
    try:
        CarRun.motor_init()
        client = Server.server_init(ip, port)
        while True:
            move = Server.receive(client, delay)
            global move_num
            if move == 'w':
                CarRun.run(0.5,20)
                move_num = 'w'
            elif move == 's':
                CarRun.back(0.5,20)
                move_num = 's'
            elif move == 'a':
                CarRun.left(0.5,30)
                CarRun.run(0.5,20)
                move_num = 'a'
            elif move == 'd':
                CarRun.right(0.5,30)
                CarRun.run(0.5,20)
                move_num = 'd'
            elif move == 'space':
                CarRun.brake(0.5,20)
                move_num = '0'
            
    except KeyboardInterrupt:
        pass
    CarRun.destroy()


def sent_info():
    try:
        sender_init()
        info = move_num
        if info != 'init':
            for i in range(5):
                send(info, 0.005)
                sleep(0.5)
        info = 'init'
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    ip = '192.168.137.6'
    port = 2222
    delay = 0.001
    t1 = Thread(target = car_control, args=(ip, port, delay))
    t2 = Thread(target = sent_info)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


