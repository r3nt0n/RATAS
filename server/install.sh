#!/usr/bin/env bash

apt update -y
apt install -y python-pip

pip install requests
pip install pycryptodome