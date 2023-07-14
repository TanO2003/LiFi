import CarRun
import Server
import RPi.GPIO as GPIO
#import Sender_number_only


R = 22
G = 27
B = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(R, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)
def car_control(ip, port, delay):
    try:
        CarRun.motor_init()
        client = Server.server_init(ip, port)
        while True:
            move = Server.receive(client, delay)
            move_num = 0
            if move == 'w':
                CarRun.back(0.5)
                move_num = 0
                GPIO.output(R, GPIO.HIGH)
                GPIO.output(G, GPIO.HIGH)
                GPIO.output(B, GPIO.HIGH)
            elif move == 's':
                CarRun.run(0.5)
                move_num = 1
            elif move == 'a':
                CarRun.right(0.5)
                move_num = 2
            elif move == 'd':
                CarRun.left(0.5)
                move_num = 3
            elif move == 'space':
                CarRun.brake(0.5)
                move_num = 4
                GPIO.output(R, GPIO.LOW)
                GPIO.output(G, GPIO.LOW)
                GPIO.output(B, GPIO.LOW)
            
    except KeyboardInterrupt:
        pass
    CarRun.destroy()





if __name__ == '__main__':
    ip = '192.168.137.83'
    port = 2222
    delay = 0.01
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.OUT)
    car_control(ip, port, delay)
    
