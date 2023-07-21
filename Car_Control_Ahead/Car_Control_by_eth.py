import CarRun_Former as CarRun
import Server
import RPi.GPIO as GPIO
from time import sleep
from threading import Thread
import Client



R = 22
G = 27
B = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(R, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)
move_num = ''


def car_control(ip, port, delay):
    try:
        CarRun.motor_init()
        client = Server.server_init(ip, port)
        while True:
            move = Server.receive(client, delay)
            global move_num
            if move == 'w':
                CarRun.run(0.5,20)
                move_num = 'run'
            elif move == 's':
                CarRun.back(0.5,20)
                move_num = 'back'
            elif move == 'a':
                CarRun.left(0.5,30)
                CarRun.run(0.5,20)
                move_num = 'left'
            elif move == 'd':
                CarRun.right(0.5,30)
                CarRun.run(0.5,20)
                move_num = 'right'
            elif move == 'space':
                CarRun.brake(0.5,20)
                move_num = 'stop'
            
    except KeyboardInterrupt:
        pass
    CarRun.destroy()


def sent_info(ip, port, delay):
    try:
        mySocket = Client.clinet_init(ip, port)
        i = 0
        while True:
            #info = CarRun.get_info()
            global move_num
            info = move_num
            Client.send(mySocket, info, delay)
            sleep(0.5)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    ip = '192.168.137.6'
    port = 2222
    delay = 0.01
    ip_2 = '169.254.35.79'
    port_2 = 2000
    delay_2 = 0.05
    #car_control(ip, port, delay)
    t1 = Thread(target = car_control, args=(ip, port, delay))
    t2 = Thread(target = sent_info, args=(ip_2, port_2, delay_2))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
