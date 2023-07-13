# Path: Car_Control\Car-Control.py
import CarRun
import Server

def car_control(ip, port, delay):
    try:
        mySocket = Server.server_init(ip, port)
        while True:
            move = Server.receive(mySocket, delay)
            if move == 'w':
                CarRun.run(1)
            elif move == 's':
                CarRun.back(1)
            elif move == 'a':
                CarRun.left(1)
            elif move == 'd':
                CarRun.right(1)
    except KeyboardInterrupt:
        pass
    CarRun.destroy()

if __name__ == '__main__':
    ip = ''
    port = 2222
    delay = 0.05
    car_control(ip, port, delay)