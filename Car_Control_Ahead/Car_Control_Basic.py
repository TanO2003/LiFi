import Server
import RPi.GPIO as GPIO
from time import sleep
from threading import Thread
from Sender import send, sender_init
import tracking as tr

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
        client = Server.server_init(ip, port)
        tr.init()
        while True:
            move = Server.receive(client, delay)
            global move_num
            move_num = move
            tr.tr(move)
            sleep(0.5)
            
    except KeyboardInterrupt:
        pass



def sent_info():
    try:
        sender_init()
        while 1:
            global move_num
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


