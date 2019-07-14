#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RATAS [connection_module] (https://www.github.com/R3nt0n/ratas)
# R3nt0n (https://www.github.com/R3nt0n)

import socket
from requests import get


class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.timeout = socket.timeout  # Default timeout exception
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.conn = None
        self.keyring = None

    def getPrivateIP(self):
        tempSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            tempSocket.connect(('10.255.255.255', 0))
            ip = tempSocket.getsockname()[0]
        except:
            ip = '127.0.0.1'
        finally:
            tempSocket.close()
        return ip

    def getPublicIP(self):
        try:
            ip = get('https://api.ipify.org', timeout=2).text
        except:
            ip = self.getPrivateIP()
        return ip

    def listen(self, timeout=None):
        self.sock.settimeout(timeout)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        conn, addr = self.sock.accept()
        self.sock.settimeout(None)
        self.conn = conn

    def connect(self):
        self.sock.connect((self.host, self.port))
        self.conn = self.sock

    def send(self, msg):
        if self.keyring and self.keyring.session_key:
            msg = self.keyring.cipherAES(msg)
        self.conn.send(msg + ':END:')

    def receive(self):
        output = ''
        while True:
            output += self.conn.recv(1024)
            if output.endswith(':END:'):
                break
        output = output[:-5]
        if self.keyring and self.keyring.session_key:
            output = self.keyring.decipherAES(output)
        return output

    def close(self):
        if self.conn:
            self.conn.close()


if __name__ == '__main__':

    # ESPERAR UNA CONEXIÓN ETERNAMENTE
    server = Connection('', 5555)
    server.listen()

    # ESPERAR UNA CONEXIÓN DURANTE 4 SEGUNDOS
    server = Connection('', 5555)
    try:
        server.listen(4)
    except socket.timeout:
        print 'Nadie ha intentado conectarse'

    # CREAR UNA CONEXIÓN
    client = Connection('localhost', 5555)
    try:
        client.connect()
    except socket.error:
        print 'El servidor está desconectado'
