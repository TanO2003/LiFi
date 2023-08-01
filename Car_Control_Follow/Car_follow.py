import RPi.GPIO as GPIO
from time import sleep
from Receiver import receive, receiver_init
import tracking_b as tr

from threading import Thread



global mode
mode = 'g'

def receive_main():
    try:
        while 1:
            global mode
            _mode = receive(0.005)
            if _mode == 'r' or _mode == 'g' or _mode == 'l' or _mode == 's':
                mode = _mode
            else:
                pass
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()


def tr_main():
    try:
        global mode
        while mode != 's':
            
            if tr.detect() == 'track':
                tr.track()
            elif tr.detect() == 'tri':
                tr.tri(mode)
            elif tr.detect() == 'dou':
                tr.dou(mode)
            else:
                continue
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()


if __name__ == '__main__':
    tr.init()
    receiver_init()
    while 1:
        if a := receive(0.005) == 'i':
            t1 = Thread(target=receive_main)
            t2 = Thread(target=tr_main)
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            break
        else:
            continue