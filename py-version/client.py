
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8080))
sock.sendall(b'How are you?')
print(sock.recv(1024))
sock.close()
