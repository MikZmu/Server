# https://youtu.be/YwWfKitB8aA
import socket
import threading
import os
import time
import subprocess
import requests

def getip():
    ip = requests.get('https://api.ipify.org').text
    print('My public IP address is: {}'.format(ip))


def kill_process_using_port(port):
    pid = subprocess.run(
        ['lsof', '-t', f'-i:{port}'], text=True, capture_output=True
    ).stdout.strip()
    if pid:
        if subprocess.run(['kill', '-TERM', pid]).returncode != 0:
            subprocess.run(['kill', '-KILL', pid], check=True)
        time.sleep(1)  # Give OS time to free up the PORT usage

def bind():
    try:
        kill_process_using_port(11111) 
        server.bind(("", port))
        server.listen(50)
    except:
        print('You messed up my order ! Restart PHOBOS !!!!!!!!!!!!!')
        kill_process_using_port(11111)
        time.sleep(3)
        bind()

def conn():
    try:
        global phobos, address
        phobos, address= server.accept()
    except:
            print('Awaiting connection... ')
            time.sleep(3)
            conn()

def init():
    global host, port, server
    host = socket.gethostbyname(socket.gethostname())  #24:50 dla VB
    #host = '0.0.0.0'  #24:50 dla VB
    port = 11111
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #utworzenie obiektu socket z użyciem konstruktora socket (do użycia z internetem AF_INET, z protokołem TCP - sock_stream)
    getip()
    bind()
    conn()
    print(f'Connected with {address}')  
    recv_thread = threading.Thread(target=handle)
    send_thread = threading.Thread(target=sendMessage)
    recv_thread.start()
    send_thread.start()      

    

def sendMessage():
    while True:
        msg = input()
        phobos.send(msg.encode('ascii'))

def command(keyword):
        try:
            msg = input()
            phobos.send(msg.encode('ascii'))
        except:
            print('broken pipe ?')


def handle(): 
    while True:
        try:
            message = phobos.recv(1024).decode('ascii')
            if(message != ""):
                if message == "quit":
                    print('now i rest')
                    command("quit")
                    phobos.close()
                elif(message == 'sendFile'):
                    #deimosChat()
                    print("msg")
                elif(message == 2):
                    print("file")
                    #deimosFile()
                elif(message == 3):
                    print("vid")
                    #deimosVid()
                else:
                    print(message)
        except:
            print('im waiting god damn it !')
            time.sleep(5)



"""def deimosFile():
    fileName  = input('provide file name plis: ')
    file = open(fileName , 'rb') #rb - reading bytes mode // otwiera plik w trybie czytania bitów
    fileSize = os.path.getsize(fileName)
    extension = fileName.split('.')[1]
    communication_socket.send(fileName.encode())
    communication_socket.send(str(fileSize).encode())
    data = file.read() # zwraca plik
    communication_socket.sendall(data)
    communication_socket.send(b'<END>')#wysyła tag końcowy, tak aby druga maszyna wiedziała jaki jest koniec pliku w bitach :_)
    file.close()
    communication_socket.close()


def remoteControl():
    while True:
        communication_socket, address = server.accept()
        menuThread = threading.Thread(target = menu) 
        menuThread.start
        sendThread = threading.Thread(target = sending)
        recvThread = threading.Thread(target = recv)

def recv():
    while True:
        try:
            chooser = communication_socket.recv('1024')
            
            menu(incoming)
        except:
            sleep()

def menu(chooser):
    if chooser == "quit":
        communication_socket.close()
        done = True
    else:
        if(chooser == 1):
            deimosChat()
        if(chooser == 2):
            deimosFile()
        if(chooser == 3):
            deimosVid()







def menu2():
    print('Type 1 to chat, 2 - To send .txt, 3 - To send video quit to quit' )
    sending = input('Make your choice!: ')
    incoming = communication_socket.recv(4096).decode('utf-8')
    if sending == "quit":
        communication_socket.close()
        done = True
    else:
        communication_socket.send(sending.encode())
        if(sending == 1):
            deimosChat()
        if(sending == 2):
            deimosFile()
        if(sending == 3):
            deimosVid()

    if incoming == "quit":
        communication_socket.close()
        done = True
    else:
        if(incoming == 1):
            deimosChat()
        if(incoming == 2):
            deimosFile()
        if(incoming == 3):
            deimosVid()"""