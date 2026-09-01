import socket

target = "google.com"
port = 22

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.settimeout(2)

result = sock.connect_ex((target, port))

print("Result:",result)

sock.close()
