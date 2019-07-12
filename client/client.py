#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RATAS [Client]

import os
import sys
import ConfigParser
import argparse

from lib.connection import Connection
from lib.keyring import Keyring
from lib.shell_cli import Shell
from lib.color import color

CFG_FILE = "./client.cfg"

def read_conf():
    cfg = ConfigParser.ConfigParser()
    cfg.read([CFG_FILE])
    host = cfg.get('GENERAL', 'host')
    port = cfg.get('GENERAL', 'port')
    reverse = cfg.get('GENERAL', 'reverse_conn')
    pub_key = cfg.get('PKI', 'pub_key')
    prv_key = cfg.get('PKI', 'prv_key')
    known_hosts = cfg.get('PKI', 'known_hosts')
    return host, int(port), reverse, pub_key, prv_key, known_hosts

def read_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Remote Shell Client.')
    parser.add_argument('-a', '--address', action='store', metavar='port', type=str,
                        dest='addr', default=False,
                        help='La dirección a utilizar en la conexión.')
    parser.add_argument('-p', '--port', action='store', metavar='port', type=int,
                        dest='port', default=False,
                        help='El puerto a utilizar en la conexión.')

    args = parser.parse_args()
    addr = args.addr
    port = args.port
    return addr, port


def main():
    HOST, PORT, REVERSE, PUB_KEY_FILE, PRV_KEY_FILE, KN_HOSTS_FILE = read_conf()

    # Si se pasa dirección y/o puerto como argumento, sobreescribirlo
    addr, port = read_args()
    if addr: HOST = addr
    if port: PORT = port

    # Si existe el known_hosts, leerlo y convertirlo en una lista
    if os.path.isfile(KN_HOSTS_FILE):
        with open(KN_HOSTS_FILE, "rb") as f:
            known_hosts = f.read()
        known_hosts = known_hosts.split("\n")
    else:
        known_hosts = False

    # Creación del socket
    conn = Connection(HOST, PORT)

    try:
        if REVERSE == '1':
            conn.listen(timeout=10)
        else:
            conn.connect()

        keyring = Keyring()

        # Lee los ficheros de claves pub/priv
        with open(PRV_KEY_FILE, 'rb') as f:
            prv_key = f.read()
        with open(PUB_KEY_FILE, 'rb') as f:
            pub_key = f.read()

        # Envía su clave pública al servidor
        conn.send(pub_key)

        # Recibe la clave pública del servidor
        srv_pub_key = conn.receive()
        if srv_pub_key == ':ERR:':
            print '{}[!]{} ERROR: El servidor no reconoce tu clave pública.'.format(color.RED,color.END)
            sys.exit(1)

        # Comparación de clave pública recibida con las contenidas en el known_hosts
        if (not known_hosts) or (srv_pub_key not in known_hosts):
            add_srv_to_known_hosts = raw_input("{}[!]{} WARNING: La clave pública de este servidor no se encuentra almacenada:\n{} \nSi lo desea, puede añadirla [y/n] >>> ".format(color.YELLOW, color.END, srv_pub_key))
            if add_srv_to_known_hosts.lower() == "y":
                with open(KN_HOSTS_FILE, "ab") as f:
                    f.write(srv_pub_key + "\n")

        # Envía firma de autenticación
        signature = keyring.sign(prv_key)
        conn.send(signature)

        srv_signature = conn.receive()
        # Si recibe error de autenticación, informa y cierra el programa
        if srv_signature == ':ERR:':
            print '{}[!]{} ERROR: La autenticación ha fallado'.format(color.RED,color.END)
            sys.exit(1)


        # Si logra autenticarse, comprueba la firma del servidor
        print '{}[+]{} Cliente autenticado correctamente'.format(color.GREEN, color.END)
        sign_valid = keyring.verify(srv_pub_key, srv_signature)
        if sign_valid:
            conn.send(':OK:')
            print '{}[+]{} Servidor autenticado correctamente'.format(color.GREEN, color.END)
        else:
            conn.send(':ERR:')
            print '{}[!]{} ERROR: La autenticación ha fallado'.format(color.RED, color.END)
            sys.exit(1)

        # Marca de sincronización
        sync = conn.receive()

        # Intercambio de clave de sesión mediante PKI
        session_key = keyring.genSessionKey()
        session_key_crypted = keyring.cipherRSA(session_key, srv_pub_key)
        conn.send(session_key_crypted)
        print '{}[+]{} Intercambiando clave de sesión...'.format(color.BLUE, color.END)
        # Una vez establecida e intercambiada la clave de sesión, asociamos el keyring a la conexión
        keyring.session_key = session_key
        conn.keyring = keyring

        shell = Shell(conn)
        shell.start()

    except conn.timeout:
        print '\n{}[!]{} El servidor está desconectado.\n'.format(color.RED,color.END)


if __name__ == '__main__':
    main()
