from threading import Thread, Event

signal = Event()

def send():
    signal.set()    