import RPi.GPIO as GPIO
from time import sleep
from Receiver import receive, receiver_init
import tracking_b as tr

from threading import Thread, Event


global mode
mode = 'g'

stop_event = Event()
start_signal = Event()

def receive_main():
    try:
        while not stop_event.is_set():
            global mode
            _mode = receive(0.005)
            if _mode == 's':
                start_signal.set()
            if _mode == 'b':
                start_signal.clear()
            elif _mode == 'r' or _mode == 'g' or _mode == 'l':
                mode = _mode
            else:
                pass
            sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()


def tr_main():
    try:
        while not stop_event.is_set():
            global mode
            if not start_signal.is_set():
                tr.brake()
                continue

            if tr.detect() == 'track':
                tr.track()
            elif tr.detect() == 'tri':
                tr.tri(mode)
            elif tr.detect() == 'dou':
                tr.dou(mode)
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()


if __name__ == '__main__':
    tr.init()
    receiver_init()
    t1 = Thread(target=receive_main)
    t2 = Thread(target=tr_main)
    t1.start()
    t2.start()
    while True:
        a=input()
        if a=='exit':
            break
    stop_event.set()
    t1.join()
    t2.join()
    exit()