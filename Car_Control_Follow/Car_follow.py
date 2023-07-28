import RPi.GPIO as GPIO
from time import sleep
from Receiver import receive, receiver_init
import tracking_b as tr



if __name__ == '__main__':
    try:
        receiver_init()
        tr.init()
        while True:
            mode = receive(0.005)
            print(mode)
            if mode == 'Error':
                print('Transmit error, trying again...')
                continue
            elif mode == 'l' or mode or 'r' or mode == 'g':
                tr.tr(mode)
            else:
                print('Receive error, trying again...')
                continue
    except KeyboardInterrupt:
        print('Interrupted')
        GPIO.cleanup()
        exit()
