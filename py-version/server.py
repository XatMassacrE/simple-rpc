
import socket
import struct
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8080))
sock.listen(1)

def handle_conn(conn, addr, handlers):
    print(addr, 'coming~')
    while True:
        len_prefix = conn.recv(4)
        if not len_prefix:
            print(addr, 'this address send nothing, close the connection')
            conn.close()
            break
        length, = struct.unpack('I', len_prefix)
        body = conn.recv(length)
        req = json.loads(body)
        msg = req['msg']
        params = req['params']
        print(msg, params)
        handler = handlers[msg]
        handler(conn, params)

def ping(conn, params):
    send_res(conn, 'pong', params)

def send_res(conn, msg, result):
    res = json.dumps({'msg': msg, 'result': result})
    len_prefix = struct.pack('I', len(res))
    conn.sendall(len_prefix)
    conn.sendall(res.encode('utf-8'))

def loop(sock, handlers):
    while True:
        conn, addr = sock.accept()
        handle_conn(conn, addr, handlers)

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,  1)
    sock.bind(('localhost', 8080))
    sock.listen(1)
    handlers = {
        'ping': ping
        }
    loop(sock, handlers)
