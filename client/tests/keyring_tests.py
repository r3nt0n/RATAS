#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RATAS [keyring_tests]


import unittest

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from lib.keyring import Keyring


class TestAES(unittest.TestCase):
    def setUp(self):
        self.keyring = Keyring()
        self.sessionKey = self.keyring.genSessionKey()

    def tearDown(self):
        del self.keyring, self.sessionKey

    def testEncryptDecrypt(self):
        data = 'Hello world!'
        cryptedData = self.keyring.cipherAES(data, self.sessionKey)
        decryptedData = self.keyring.decipherAES(cryptedData, self.sessionKey)
        self.assertEqual(data, decryptedData)


class TestRSA(unittest.TestCase):
    def setUp(self):
        self.keyring = Keyring()
        self.keys = self.keyring.genRSAKeys()
        self.prvKey = self.keyring.exportRSAKeys(self.keys)
        self.pubKey = self.keyring.exportRSAKeys(self.keys, keyToExport='pub')

    def tearDown(self):
        del self.keyring, self.keys, self.prvKey, self.pubKey

    def testEncryptDecrypt(self):
        data = 'Hello world!'
        cryptedData = self.keyring.cipherRSA(data, self.pubKey)
        decryptedData = self.keyring.decipherRSA(cryptedData, self.prvKey)
        self.assertEqual(data, decryptedData)


if __name__ == '__main__':
    unittest.main()
