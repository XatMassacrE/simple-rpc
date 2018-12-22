
import socket
import struct
import json
import os
import select
import asyncore
from io import StringIO

class RPCHandler():
    def __init__(self, sock, addr):
        self.addr = addr
        self.handlers = {
                'ping': self.ping
                }
        self.rbuf = StringIO()

    def close(self):
        print('close this connection: ', self.addr)
        self.close()

    def read(self):
        while True:
            content = self.recv(1024)
            if content:
                self.rbuf.write(content)
            if len(content) < 1024:
                break
        self.handle_rpc()

    def handle_rpc(self):
        while True:
            self.rbuf.seek(0)
            len_prefix = self.rbuf.read(4)
            if len(len_prefix) < 4:
                break

            length, = struct.unpack('I', len_prefix)
            body = self.rbuf(length)
            if len(body) < length:
                break
            req = json.loads(body)
            msg = req['msg']
            params = req['params']
            print(msg, params)
            handler = self.handlers[msg]
            handler(params)
            left = self.rbuf.getvalue()[length + 4:]
            self.rbuf = StringIO()
            self.rbuf.write(left)
        self.rbuf.seek(0, 2)

    def ping(self, params):
        self.send_res('pong', params)

    def send_res(self, msg, result):
        res = json.dumps({'msg': msg, 'result': result})
        len_prefix = struct.pack('I', len(res))
        self.send(len_prefix)
        self.send(res.encode('utf-8'))

class RPCServer():

    def __init__(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(False)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(1)
        self.server = server
        self.inputs = [self.server]
        self.outputs = []
        self.queues = {}

    def start(self):
        while self.inputs:
            print('waiting...')
            # print('inputs', self.inputs)
            # print('outputs', self.outputs)
            # print('queues', self.queues)
            rs, ws, exs = select.select(self.inputs, self.outputs, self.inputs)
            # print('readable, writeable, exceptions', rs, ws, exs)
            if not (rs or ws or exs):
                print('select has nothings')
                break
            for s in rs:
                if s is self.server:
                    sock, addr = s.accept()
                    print('have connection ', addr)
                    rpc = RPCHandler(sock, addr)
                    rpc.handle_rpc()
                    self.inputs.append(sock)
                    self.queues[sock] = []
                else:
                    try:
                        # data = s.recv(1024)
                        length_prefix = s.recv(4)
                        length, = struct.unpack("I", length_prefix)
                        data = s.recv(length)
                    except:
                        print('closing conn', addr)
                        if s in self.outputs:
                            self.outputs.remove(s)
                        self.inputs.remove(s)
                        s.close()
                        del self.queues[s]
                    else:
                        if data:
                            print('receive data ', data, s.getpeername())
                            self.queues[s].append(data)
                            if s not in self.outputs:
                                self.outputs.append(s)
            for s in ws:
                try:
                    next_msg = self.queues[s][0]
                    del self.queues[s][0]
                except:
                    print(s.getpeername(), ' queue empty')
                    self.outputs.remove(s)
                else:
                    req = json.loads(next_msg)
                    msg = req['msg']
                    params = req['params']
                    res = json.dumps({'msg': 'pong', 'params': params})
                    print('sending ', res, ' to ', s.getpeername())
                    os.popen('sleep 5').read()
                    length_prefix = struct.pack("I", len(res))
                    s.send(length_prefix)
                    s.send(res.encode('utf-8'))

            for e in exs:
                print('exception happens ', s.getpeername())
                self.inputs.remove(s)
                if s in self.outputs:
                    self.outputs.remove(s)
                s.close()
                del self.queues[s]


if __name__ == '__main__':
    s = RPCServer('localhost', 8080)
    s.start()

    #asyncore.loop()
