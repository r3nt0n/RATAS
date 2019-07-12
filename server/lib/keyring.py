#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RATAS [keyring_module]

from base64 import b64encode, b64decode

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes  # Para generar claves aleatorias
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


class Keyring:
    def __init__(self):
        self.sep = ':%:%:&:%:%:'
        self.session_key = False

    def genSessionKey(self):
        self.session_key = get_random_bytes(32)
        return self.session_key

    def cipherAES(self, data):
        cipherAES = AES.new(self.session_key, AES.MODE_EAX)
        cryptedData, tag = cipherAES.encrypt_and_digest(data)
        cryptedMsg = cipherAES.nonce + self.sep + tag + self.sep + cryptedData
        cryptedMsg = b64encode(cryptedMsg)
        return cryptedMsg

    def decipherAES(self, cryptedMsg):
        cryptedMsg = b64decode(cryptedMsg)
        cryptedMsg = cryptedMsg.split(self.sep)
        nonce = cryptedMsg[0]
        tag = cryptedMsg[1]
        cryptedData = cryptedMsg[2]
        decipherAES = AES.new(self.session_key, AES.MODE_EAX, nonce)
        decryptedData = decipherAES.decrypt_and_verify(cryptedData, tag)
        return decryptedData

    def genRSAKeys(self):
        keys = RSA.generate(2048)
        return keys

    def exportRSAKeys(self, keys, keyToExport='priv', formatKey='OpenSSH'):
        if keyToExport == 'priv':
            keyRSA = keys.exportKey()
        if keyToExport == 'pub':
            keyRSA = keys.publickey().exportKey(format=formatKey)
        return keyRSA

    def cipherRSA(self, data, pubKey):
        key = RSA.importKey(pubKey)
        cipherRSA = PKCS1_OAEP.new(key)
        cryptedData = cipherRSA.encrypt(data)
        cryptedData = b64encode(cryptedData)
        return cryptedData

    def decipherRSA(self, cryptedData, privKey):
        cryptedData = b64decode(cryptedData)
        key = RSA.importKey(privKey)
        decipherRSA = PKCS1_OAEP.new(key)
        decryptedData = decipherRSA.decrypt(cryptedData)
        return decryptedData

    def sign(self, privKey):
        msg = 'Hello world'
        privKey = RSA.import_key(privKey)
        msg_hash = SHA256.new(msg)
        signature = pkcs1_15.new(privKey).sign(msg_hash)
        return signature

    def verify(self, pubKey, signature):
        msg = 'Hello world'
        pubKey = RSA.import_key(pubKey)
        msg_hash = SHA256.new(msg)
        is_valid = True
        try:
            pkcs1_15.new(pubKey).verify(msg_hash, signature)
        except (ValueError, TypeError):
            is_valid = False
        return is_valid
