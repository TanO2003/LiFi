import Server
import RPi.GPIO as GPIO
from time import sleep
from threading import Thread,Event
from Sender import send, sender_init
import tracking as tr

R = 22
G = 27
B = 24
Signal = 2
GPIO.setmode(GPIO.BCM)
GPIO.setup(R, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)
GPIO.setup(Signal, GPIO.OUT,initial=GPIO.HIGH)

move_num = 'init'



def car_control(ip, port, delay):
    try:
        client = Server.server_init(ip, port)
        tr.init()
        while True:
            move = Server.receive(client, delay)
            global move_num
            move_num = move
            if move == 'stop':
                tr.brake()
                GPIO.output(Signal,1)
                continue
            if not Server.start_signal.is_set():
                tr.brake()
                GPIO.output(Signal,1)
                continue

            GPIO.output(Signal,0)
            tr.tr(move)
            sleep(0.01)
            

    except KeyboardInterrupt:
        Server.over_signal.set()
        exit()




def sent_info():
    try:
        sender_init()
        global move_num
        while 1:
            if move_num == 'g' or move_num == 'l' or move_num == 'r' or move_num == 'q' or move_num == 'e':
                info = move_num
                send(info, 0.005)
            sleep(0.5)
            if Server.over_signal.is_set():
                exit()

    except Exception:
        exit()

if __name__ == '__main__':
    ip = '192.168.137.12'
    port = 6666
    delay = 0.001
    t1 = Thread(target = car_control, args=(ip, port, delay))
    t2 = Thread(target = sent_info)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

