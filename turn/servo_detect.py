import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
Ldr = 6
GPIO.setup(Ldr, GPIO.IN)
servo = 23
GPIO.setup(servo, GPIO.OUT)
pwm_servo = GPIO.PWM(servo, 50)
pwm_servo.start(0)





def servo_detect():
    while True:
        for pos in range(181):
            servo_pulse(pos)
            sleep(0.0009)
            if GPIO.input(Ldr) == 0:
                return
        for pos in reversed(range(181)):
            servo_pulse(pos)
            sleep(0.0009)
            if GPIO.input(Ldr) == 0:
                return
                    




def servo_pulse(myangle):
	pulsewidth = (myangle*11)+500
	GPIO.output(servo,GPIO.HIGH)
	sleep(pulsewidth/1000000.0)
	GPIO.output(servo,GPIO.LOW)
	sleep(20.0/1000-pulsewidth/1000000.0)





try:
    while True:
        servo_detect()
        print("detect!")
        sleep(0.5)
except KeyboardInterrupt:
    pass
