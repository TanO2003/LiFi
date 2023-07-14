import keyboard

def get_key():
    event = keyboard.read_event()
    return event.name


if __name__ == '__main__':
    print(get_key())