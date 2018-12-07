
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8080))
sock.listen(1)

def start():
    while True:
        conn, addr = sock.accept()
        print(conn.recv(1024))
        conn.sendall(b'Fine, thank you, and you?')
        conn.close()

if __name__ == '__main__':
    start()
