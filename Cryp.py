#!/usr/bin/python3

from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time


class Encryptor:
    def __init__(self, key):
        self.key = key#Atributo key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)#b"\0"<-- Es para crear bytes por ejemplo asi b'\x00\ y depdendiendo -len (longitud)=-2 retornara mas o menos b'\x00\x00\x00\..

    def encrypt(self, message, key, key_size=256):#mensaje tiene plaintext
        message = self.pad(message)#Le pasamos message como parametro a la funcion pad entonces dependiendo de la longitud del mensaje creara bits la funcion pad
        iv = Random.new().read(AES.block_size)#bytes
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):#esta funcion trabaja con la funcion encrypt
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()#plaintext guarda el valor tipo string que nosotro copiadmos por teclado
        enc = self.encrypt(plaintext, self.key)#plaintext es el parametro que recibira encrypt el cual corresponderia message y self.key es el atributo de la clase
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)#despues de encriptarlo pasamos a removerlo quedando asi solo el archivo encriptado

    def decrypt(self, ciphertext, key):#ciphertext recibe el nombre que damos por teclado por medio de la funcion decryp_file como parametro
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")#rstrip quita elementos de izquierda a derecha

    def decrypt_file(self, file_name):#file_name= nombre que tecleamos y va como parametro a la funcion de arriba
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)#Invocamos a la funcion decrypt con self.decrypt
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        for dirName, subdirList, fileList in os.walk(dir_path):
            for fname in fileList:
                if (fname != 'script.py' and fname != 'data.txt.enc'):#Para que no vaya encriptar la contraseña ni el script
                    dirs.append(dirName + "\\" + fname)
        return dirs

    def encrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.encrypt_file(file_name)

    def decrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.decrypt_file(file_name)


key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'#Atributo
enc = Encryptor(key)#Objeto de la clase Encryptor atributo key
clear = lambda: os.system('cls')#limpiamos la consoloa de windows

if os.path.isfile('data.txt.enc'):
    while True:
        password = str(input("Enter password: "))
        enc.decrypt_file("data.txt.enc")
        p = ''
        with open("data.txt", "r") as f:
            p = f.readlines()
        if p[0] == password:
            enc.encrypt_file("data.txt")
            break

    while True:
        clear()#limpiamos pantalla
        choice = int(input(
            "1. Press '1' to encrypt file.\n2. Press '2' to decrypt file.\n3. Press '3' to Encrypt all files in the directory.\n4. Press '4' to decrypt all files in the directory.\n5. Press '5' to exit.\n"))
        clear()
        if choice == 1:
            enc.encrypt_file(str(input("escribe el nombre del archivo a encriptar: ")))#nombreObj.funcion a la que deseamos acceder en este caso a encryp_file y como parametro lo que escribimos por consola
        elif choice == 2:
            enc.decrypt_file(str(input("escribe el nombre del archivo a desencriptar: ")))
        elif choice == 3:
            enc.encrypt_all_files(str())
        elif choice == 4:
            enc.decrypt_all_files()
        elif choice == 5:
            exit()
        else:
            print("Selecciona una opcion valida")

else:
    while True:
        clear()
        password = str(input("Preparando cosas. Ingrese una contraseña que se utilizará para descifrar: "))
        repassword = str(input("Confirmar password: "))
        if password == repassword:
            break
        else:
            print("Password incorrecto")
    f = open("data.txt", "w+")
    f.write(password)
    f.close()
    enc.encrypt_file("data.txt")
    print("Por favor reinicia el progama")
    time.sleep(15)
