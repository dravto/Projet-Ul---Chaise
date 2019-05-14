#!/usr/bin/env /usr/bin/python
from gpiozero import AngularServo
import time
import socket

#pin

moteur = 18
up = False

#setup bleutooth

server_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
address = "B8:27:EB:8B:31:A9"
port = 1
server_socket.bind((address,port))
server_socket.listen(1)
print("On standby...")

client_socket,address = server_socket.accept()
print("Accepted connection from ", address)

#moteur

servo = AngularServo(moteur)

while True:
    
    data = client_socket.recv(1024)

    if data == b'0' and up == True:
        print("Down")
        servo.angle = -30
        time.sleep(3)
        up = False
        
    elif data == b'1' and up == False:
        print("Up")
        servo.angle = 15
        time.sleep(6)
        up = True
        
    elif data == b's':
        print("Start")
        servo.min()
        time.sleep(5)
        
    elif data == b'q':
        print("Quit")
        servo.max()
        time.sleep(6)
        servo.angle = 0
        break
        
    servo.angle = 0 


#onExit

client_socket.close()
server_socket.close()

from subprocess import call
call("shutdown -h now", shell=True)
