import RPi.GPIO as GPIO
from time import sleep




class Servo:
    def __init__(self):
        self.Ldr = 6
        self.servo = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.Ldr, GPIO.IN)
        GPIO.setup(self.servo, GPIO.OUT)
        pwm_servo = GPIO.PWM(self.servo, 50)
        pwm_servo.start(0)


    def servo_pulse(self, myangle):
        pulsewidth = (myangle*11)+500
        GPIO.output(self.servo,GPIO.HIGH)
        sleep(pulsewidth/1000000.0)
        GPIO.output(self.servo,GPIO.LOW)
        sleep(20.0/1000-pulsewidth/1000000.0)





    def servo_detect(self):
        while True:
            for pos in range(45, 135):
                self.servo_pulse(pos)
                sleep(0.005)
                if GPIO.input(self.Ldr) == 0:
                        return
            for pos in reversed(range(45, 135)):
                self.servo_pulse(pos)
                sleep(0.005)
                if GPIO.input(self.Ldr) == 0:
                        return
    




