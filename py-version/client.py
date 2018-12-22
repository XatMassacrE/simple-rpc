
import json
import time
import struct
import socket

def send_str(sock, s):
    sock.sendall(s.encode('utf-8'))

def rpc(sock, msg, params):
    req = json.dumps({'msg': msg, 'params': params})
    len_prefix = struct.pack('I', len(req))
    sock.sendall(len_prefix)
    send_str(sock, req)

    res_len_prefix = sock.recv(4)
    res_len_body, = struct.unpack('I', res_len_prefix)
    body = sock.recv(res_len_body)
    res = json.loads(body)
    return res['msg'], res['params']

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8080))
 
    for i in range(10):
        out, result = rpc(sock, 'ping', f'conn {i}')
        print(out, result)
        time.sleep(1)
    sock.close()
