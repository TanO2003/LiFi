import RPI.GPIO as GPIO

	
GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.IN)
while True:
    a = GPIO.input(12)

    print(a)
