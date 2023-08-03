import RPi.GPIO as GPIO
import time




IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

TSLP1 = 3
TSLP2 = 5
TSRP1 = 4
TSRP2 = 18

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

chan_signal = True


def init():
	global pwm_ENA
	global pwm_ENB
	GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
	GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
	GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
	GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
	GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
	GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
	GPIO.setup(TSLP1,GPIO.IN)
	GPIO.setup(TSLP2,GPIO.IN)
	GPIO.setup(TSRP1,GPIO.IN)
	GPIO.setup(TSRP2,GPIO.IN)
	pwm_ENA = GPIO.PWM(ENA,2000)
	pwm_ENB = GPIO.PWM(ENB,2000)
	pwm_ENA.start(0)
	pwm_ENB.start(0)
	
def run(leftspeed, rightspeed):
	GPIO.output(IN1,GPIO.LOW)
	GPIO.output(IN2,GPIO.HIGH)
	GPIO.output(IN3,GPIO.LOW)
	GPIO.output(IN4,GPIO.HIGH)
	pwm_ENA.ChangeDutyCycle(rightspeed)
	pwm_ENB.ChangeDutyCycle(leftspeed)
	
def back(leftspeed, rightspeed):
	GPIO.output(IN1,GPIO.HIGH)
	GPIO.output(IN2,GPIO.LOW)
	GPIO.output(IN3,GPIO.HIGH)
	GPIO.output(IN4,GPIO.LOW)
	pwm_ENA.ChangeDutyCycle(rightspeed)
	pwm_ENB.ChangeDutyCycle(leftspeed)

	
def brake():
	GPIO.output(IN1,GPIO.LOW)
	GPIO.output(IN2,GPIO.LOW)
	GPIO.output(IN3,GPIO.LOW)
	GPIO.output(IN4,GPIO.LOW)

def track(TSLV1,TSLV2,TSRV1,TSRV2):
	if TSLV1==0 and TSLV2==1 and TSRV1==1 and TSRV2==1:
		run(1,32)
		#time.sleep(0.01)
	elif TSLV1==1 and TSLV2==0 and TSRV1==0 and TSRV2==1:
		run(3,15)
		#time.sleep(0.01)
	elif TSLV1==1 and TSLV2==0 and TSRV1==1 and TSRV2==1:
		run(1,32)
		#time.sleep(0.01)
	elif TSLV1==1 and TSLV2==1 and TSRV1==0 and TSRV2==1:
		run(24,1)
		#time.sleep(0.01)
	elif TSLV1==1 and TSLV2==1 and TSRV1==1 and TSRV2==0:
		run(24,1)
		#time.sleep(0.01)
''' 
def track():
	if TSLV1==0 and TSLV2==0 and TSRV1==0 and TSRV2==0:
		back(0,20)
'''
def tri(order):
	if order == 'r':
		run(20,1)
		time.sleep(1.2)
	elif order == 'l':
		run(1,16)
		time.sleep(1.2)
	elif order == 'g':
		run(4,4)
		return
	#time.sleep(0.5)
	while True:
		TSLV1_tri = GPIO.input(TSLP1)
		TSLV2_tri = GPIO.input(TSLP2)
		TSRV1_tri = GPIO.input(TSRP1)
		TSRV2_tri = GPIO.input(TSRP2)
		if TSLV1_tri==1 and TSLV2_tri==0 and TSRV1_tri==0 and TSRV2_tri==1:
			return
	
def chan(mode):
	if mode =='q':
		run(1,18)
		time.sleep(1)
	if mode =='e':
		run(25,1)
		time.sleep(1)
	global chan_signal
	chan_signal = False
	while 1:
		run(4,16)
		time.sleep(0.6)
		TSLV1_chan = GPIO.input(TSLP1)
		TSLV2_chan = GPIO.input(TSLP2)
		TSRV1_chan = GPIO.input(TSRP1)
		TSRV2_chan = GPIO.input(TSRP2)
		if not(TSLV1_chan and TSLV1_chan and TSRV1_chan and TSRV2_chan):
			return
			




def tr(mode):
	order= mode
	global chan_signal
	TSLV1 = GPIO.input(TSLP1)
	TSLV2 = GPIO.input(TSLP2)
	TSRV1 = GPIO.input(TSRP1)
	TSRV2 = GPIO.input(TSRP2)
	if mode == 'stop':
		brake()
		return
	if mode =='q' or mode == 'e':
		if chan_signal:
			chan(mode)
		else:
			mode == 'g'
	if mode == 'g' or mode == 'l' or mode == 'r':
		chan_signal = True
	if not ((TSLV1==0 and TSLV2==0 and TSRV1==0 and TSRV2==0)or(TSLV1==1 and TSLV2==0 and TSRV1==0 and TSRV2==0)or(TSLV1==0 and TSLV2==0 and TSRV1==0 and TSRV2==1)):
		track(TSLV1,TSLV2,TSRV1,TSRV2)
	elif TSLV1==0 and TSLV2==0 and TSRV1==0 and TSRV2==0:
		tri(order)
	elif TSLV1==1 and TSLV2==0 and TSRV1==0 and TSRV2==0:
		tri(order)
	elif TSLV1==0 and TSLV2==0 and TSRV1==0 and TSRV2==1:
		tri(order)
	

