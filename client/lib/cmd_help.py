#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RATAS [commandHelp] (https://www.github.com/R3nt0n/ratas)
# R3nt0n (https://www.github.com/R3nt0n)


##########################################################################
# MANUAL DE COMANDOS
# Entra comando y devuelve la entrada del manual relacionada
##########################################################################
def manual(command):

    if command == 'help':
        output = '''
                           *** COMANDOS ESPECIALES ***
    -------------------------------------------------------------------------
        HELP:           Muestra la lista de comandos especiales
        CLEAR:          Limpiar pantalla
        PWD:            Muestra el directorio en el que te encuentras
        FTP:            Conectar a un servidor FTP
        GETFILE:        Descargar un fichero del servidor en esta máquina
        SENDFILE:       Enviar un fichero de esta máquina al servidor
        START:          Ejecutar un archivo en el equipo servidor
        READ:           Muestra el contenido de un fichero en la consola
        SHUTDOWN:       Apagar el servidor
        REBOOT:         Reiniciar el servidor
        EXIT:           Salir de la consola de comandos
    -------------------------------------------------------------------------\n
    *Para más info sobre un comando especial (descripción, modificadores...):
     help [comando]\n'''

##########################################################################

    elif command.startswith('help ftp'):  # AYUDA DE FTP
        output = '''
Este comando sirve para realizar una conexion a un servidor FTP.\n
Tras ejecutar el comando, se pedira la IP del host, el usuario y la contraseña.\n
La sintaxis es [ftp] ENTER [ip-host] ENTER [user] ENTER [password]\n'''

##########################################################################

    elif command.startswith('help start'):  # AYUDA DE START
        output = '''
Este comando sirve para ejecutar un archivo en el equipo del servidor.\n
La sintaxis es: [start] [nombre-del-archivo]\n
Ejemplo: start client.py\n'''

##########################################################################

    elif command.startswith('help:&:read'):  # AYUDA DE READ
        output = '''
Este comando sirve para mostrar por la consola el contenido de un fichero alojado en el equipo servidor.\n
La sintaxis es: [read] [nombre-del-archivo]\n
Ejemplo: read texto.txt\n'''

##########################################################################

    elif command.startswith('help:&:clear'):  # AYUDA DE CLEAR
        output = '''
Este comando sirve para limpiar la pantalla.\n'''

##########################################################################

    elif command.startswith('help:&:getfile'):
        output = '''
Este comando sirve para descargar ficheros que estén alojados en el servidor.
\nLa sintaxis es: getfile [rutaOrigen] [rutaDestino]\n
- La ruta de origen hace referencia a la ruta donde se encuentra alojado el fichero en el servidor.
- La ruta de destino hace referencia a la ruta donde se almacenará el fichero en
  la máquina cliente.
- Las rutas pueden ser absolutas o relativas.
\nEjemplo: getfile D:/Documents/fichero.exe D:/Downloads/ficheroDescargado.exe'''

##########################################################################

    elif command.startswith('help:&:sendfile'):
        output = '''
Este comando sirve para enviar ficheros que estén alojados en el cliente hacia
la máquina del servidor.\n
La sintaxis es: sendfile [rutaOrigen] [rutaDestino]\n
- La ruta de origen hace referencia a la ruta donde se encuentra alojado el
  fichero en esta máquina.
- La ruta de destino hace referencia a la ruta donde se almacenará el fichero en
  la máquina servidor.
- Las rutas pueden ser absolutas o relativas.\n
Ejemplo: getfile D:/Documents/fichero.exe D:/Downloads/ficheroDescargado.exe'''

##########################################################################

    elif command.startswith('help:&:shutdown'):  # AYUDA DE SHUTDOWN
            output = '''
Este comando sirve para apagar el servidor de forma inmediata, forzando el cierre de aplicaciones.
\nLa sintaxis es: [shutdown]\n'''

##########################################################################

    elif command.startswith('help:&:reboot'):  # AYUDA DE REBOOT
        output = '''
Este comando sirve para reiniciar el servidor de forma inmediata, forzando el cierre de aplicaciones.
\nLa sintaxis es: [reboot]\n'''

##########################################################################

    elif command.startswith('help:&:exit'):  # AYUDA DE EXIT
        output = 'Este comando sirve para cerrar la consola.\n'

    else:
        output = 'No existe una entrada en el manual para ese comando.\n'

##########################################################################

    return output
##########################################################################


##########################################################################
# MANUAL DE COMANDOS FTP
# Entra command, devuelve output
##########################################################################
def manualFTP(comftp):

    if comftp == 'help':
        output = '''
                             *** COMANDOS FTP ***
    ---------------------------------------------------------------------
    HELP:           Muestra la lista de comandos que se pueden utilizar
    CLEAR:          Limpiar pantalla
    PWD:            Muestra la ruta del directorio actual
    CD:             Cambia de directorio
    LS:             Muestra el contenido del directorio actual
    MKDIR:          Crear un directorio o árbol de directorios
    RMDIR:          Eliminar un directorio
    UP:             Subir un fichero al servidor FTP
    DOWN:           Descargar un fichero del servidor FTP
    BYE:            Cerrar la conexión FTP y regresar a la consola remota
    ---------------------------------------------------------------------\n
   **Para obtener ayuda sobre algún comando:    help comando**\n
   **NOTA: Para ejecutar comandos locales, anteponer ! al comando.
           Ejemplo: !pwd\n\n'''

    elif comftp.startswith('shortHelp'):
        output = '''
Para conocer los comandos FTP disponibles escribe help.
Para ejecutar comandos locales, anteponer ! al comando.'''

    elif comftp.startswith('help:&:clear'):  # AYUDA DE CLEAR
        output = '''
Este comando sirve para limpiar la pantalla.\n'''

##########################################################################

    elif comftp.startswith('help pwd'):  # AYUDA DE PWD
        output = '''
Este comando sirve para mostrar la ruta del directorio en el que te encuentras.\n'''

##########################################################################

    elif comftp.startswith('help !pwd'):  # AYUDA DE LPWD
        output = '''
Este comando sirve para mostrar la ruta del directorio local en el que te encuentras.\n'''

##########################################################################

    elif comftp.startswith('help cd'):  # AYUDA DE CD
        output = '''
Este comando sirve para cambiar de directorio.\n
La sintaxis es: [cd] [ruta]\n
Ejemplo: cd pages\n'''

##########################################################################

    elif comftp.startswith('help !cd'):  # AYUDA DE LCD
        output = '''
Este comando sirve para cambiar el directorio local.\n
La sintaxis es: [lcd] [ruta]\n
Ejemplo: lcd pages\n'''

##########################################################################

    elif comftp.startswith('help ls'):  # AYUDA DE LS
        output = '''
Este comando sirve para listar el contenido del directorio actual.'''

##########################################################################

    elif comftp.startswith('help !ls'):  # AYUDA DE LLS
        output = '''
Este comando sirve para listar el contenido del directorio actual en el equipo local.'''

##########################################################################

    elif comftp.startswith('help:&:mkdir'):  # AYUDA DE MKDIR
        output = '''
Este comando sirve para crear directorios.\n
La sintaxis es: [mkdir] [ruta]\n
Ejemplo: mkdir carpeta'''

##########################################################################

    elif comftp.startswith('help rmdir'):  # AYUDA DE RMDIR
        output = '''
Este comando sirve para eliminar directorios.\n
La sintaxis es: [rmdir] [ruta]\n
Ejemplo: rmdir carpeta\n'''

##########################################################################

    elif comftp.startswith('help up'):  # AYUDA DE UP
        output = '''
Este comando sirve para subir un fichero al host FTP desde el equipo servidor.\n
La sintaxis es: [up] [ruta]\n
Ejemplo: up imagen.png'''

##########################################################################

    elif comftp.startswith('help down'):  # AYUDA DE DOWN
        output = '''
Este comando sirve para descargar un fichero desde el host FTP al equipo servidor.\n
La sintaxis es: [down] [ruta]\n
Ejemplo: down imagen.png'''

##########################################################################

    else:
        output = 'No existe una entrada en el manual para ese comando.\n'

    return output
##########################################################################
