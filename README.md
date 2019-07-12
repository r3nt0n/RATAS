![[Version 1.2](https://github.com/R3nt0n)](http://img.shields.io/badge/version-v1.2-orange.svg)
![[Python 2.7](https://github.com/R3nt0n)](http://img.shields.io/badge/python-2.7-blue.svg)
![[GPL-3.0 License](https://github.com/R3nt0n)](https://img.shields.io/badge/license-GPL%203.0-brightgreen.svg)



# RATAS
RATAS (**R**emote **A**ccess **T**ool **A**wesome and **S**ecure) is a tool to get access to other computers. 
It was **written in 2016** for **academic purposes**, presented as a final project of the Higher Degree in Information Systems Management in the Network. The idea was to create something that replicate the ssh functions.  
  
  
<p align="center"><img src="https://github.com/R3nt0n/ratas/blob/master/remote-shell.png" /></p>


+ Asymetric encryptation
+ Reverse connection
+ Compatible with ssh

The app is divided into two slices: client and server. From the **client** you can **administer** the computer that has installed the **server**.

You can use **any normal command** that you be able to introduce in the server shell, and **also special built-in commands** like READ, START, GETFILE, SENDFILE... 

The communication between two processes will be encrypted using **asymetric criptography** (using RSA-2048 public and private keys to establish the communication and AES-256 onwards). Also have the option to configure **known hosts** (compatible with the known hosts ssh protocol).

It also include a built-in tool to **generate random private and public keys** (`gen_keys.py`).

If you want, you can configure it to use **reverse connection** in the configuration files.
 

## Requirements
+ Python 2.7
+ requests (*optional*, only if you want to use lyricpass)
+ beautifulsoup4 (*optional*, only if you want to use lyricpass)


## Legal disclaimer
This tool is created for the sole purpose of security awareness and education, it should not be used against systems that you do not have permission to test/attack. The author is not responsible for misuse or for any damage that you may cause. You agree that you use this software at your own risk.
