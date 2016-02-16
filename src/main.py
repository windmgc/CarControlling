__author__ = 'windmgc'
# coding: UTF-8

'''This is the source code file for controlling your PWM cars.
The socket address here is 192.168.8.1:2001, just an example.
Class Carcontrol defines five controlling function definitions,
including going forward, going backward, going left, going right and buzzing.
In the main function, create your socket connection first, then create the car object and design control flow.
'''

import socket
import time


def socketConnect():
    socket_host = '::ffff:192.168.8.1'
    socket_port = 2001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((socket_host, socket_port))
        return s
    except:
        print "Error occurred when socket connection."


class CarControl(object):

    def __init__(self):
        self.car_type = "PWM CAR"

    def carForward(self, socketconn, time_to_sleep):
        cmd = "direction:run!"
        socketconn.sendall(cmd)
        data = socketconn.recv(1024)
        time.sleep(time_to_sleep)
        cmd = "direction:stop!"
        socketconn.sendall(cmd)
        data = socketconn.recv(1024)

    def carBackward(self, socketconn, time_to_sleep):
        cmd = "direction:back!"
        socketconn.sendall(cmd)
        data = socketconn.recv(1024)
        time.sleep(time_to_sleep)
        cmd = "direction:stop!"
        socketconn.sendall(cmd)
        data = socketconn.recv(1024)

    def carLeft(self, socketconn, time_to_sleep):
        cmd = "direction:left!"
        socketconn.sendall(cmd)
        data = socketconn.recv(1024)
        time.sleep(time_to_sleep)
        cmd = "direction:stop!"
        socketconn.sendall(cmd)
        data = socketconn.recv(1024)

    def carRight(self, socketconn, time_to_sleep):
        cmd = "direction:right!"
        socketconn.sendall(cmd)
        data = socketconn.recv(1024)
        time.sleep(time_to_sleep)
        cmd = "direction:stop!"
        socketconn.sendall(cmd)
        data = socketconn.recv(1024)

    def carBuzzer(self, socketconn, time_to_sleep):
        time.sleep(time_to_sleep)
        cmd = "buzzer:on!"
        socketconn.sendall(cmd)
        data = socketconn.recv(1024)
        time.sleep(time_to_sleep)
        cmd = "buzzer:off!"
        socketconn.sendall(cmd)
        data = socketconn.recv(1024)


def main():
    socketconn = socketConnect()
    car_object = CarControl()

    #You can design control flow of the car here
    car_object.carForward(socketconn, 1)
    car_object.carBackward(socketconn, 1)
    car_object.carLeft(socketconn, 1)
    car_object.carRight(socketconn, 1)
    car_object.carBuzzer(socketconn, 1)


if __name__ == "__main__":
    main()


