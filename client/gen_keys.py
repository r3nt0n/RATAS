#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RATAS [GenKeys] (https://www.github.com/R3nt0n/ratas)
# R3nt0n (https://www.github.com/R3nt0n)

import argparse

from lib.keyring import Keyring


###############################################################################
# PROCESSING ARGS PASSED TO THE SCRIPT
###############################################################################
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                 description='Genera un par de claves RSA.')

parser.add_argument('-p', '--prv', action='store', metavar='file', type=str,
                    dest='prv', default='./prv.key',
                    help='Ruta dónde exportar la clave privada.')

parser.add_argument('-f', '--pub', action='store', metavar='file', type=str,
                    dest='pub', default='./pub.key',
                    help='Ruta dónde exportar la clave pública.')

args = parser.parse_args()

prvFile = args.prv
pubFile = args.pub
###############################################################################

k = Keyring()

keys = k.genRSAKeys()
prvKey = k.exportRSAKeys(keys, keyToExport='priv')
pubKey = k.exportRSAKeys(keys, keyToExport='pub', formatKey='OpenSSH')

with open(prvFile, 'wb') as f:
    f.write(prvKey)
with open(pubFile, 'wb') as f:
    f.write(pubKey)
