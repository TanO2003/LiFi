import RPi.GPIO as GPIO
import time 
import struct 

GPIO.setmode(GPIO.BCM)
IN1=22
IN2=27
IN3=24
GPIO.setup(IN1,GPIO.OUT)
GPIO.setup(IN2,GPIO.OUT)
GPIO.setup(IN3,GPIO.OUT)
	
def LIGHT():
	try:      
		while True:	
			GPIO.output(IN1,GPIO.HIGH)
			time.sleep(1)
			GPIO.output(IN1,GPIO.LOW)
			time.sleep(1)
	except KeyboardInterrupt:
		return
def LIGHT_OFF():
	GPIO.output(IN1,GPIO.LOW)
	GPIO.output(IN2,GPIO.LOW)
	GPIO.output(IN3,GPIO.LOW)
	
def LIGHT_ON(num):
	for i in num:
		if i=='1':
			GPIO.output(IN1,GPIO.HIGH)
			time.sleep(0.3)
		if i=='0':
			GPIO.output(IN1,GPIO.LOW)
			time.sleep(0.3)
	return

def str_2_bin(str):
	binary=''.join(format(ord(i),'08b')for i in str)
	binary.replace('00000','000001')
	return binary

def tran():
	str=input('str=')
	num = str_2_bin(str)
	LIGHT_ON(num)

while True:
	command = input('command=')
	if command == 'on':
		LIGHT()
		
	elif command == 'off':
		LIGHT_OFF()
		
	else :
		num = str_2_bin(command)
		LIGHT_ON(num)
		
