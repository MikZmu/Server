# https://youtu.be/YwWfKitB8aA
import socket
import threading
import os
import time
import subprocess
import sys
import cv2
import imutils
import queue
import pyaudio
import wave
import pickle
import base64
#import requests 






global host, port, server, linuxMode
host = '0.0.0.0'
port = 9999
global state
state = ['isLinux', 'streaming', 'connected', 'connecting', 'binding', 'quitPrompt']
global curState


#def getip():
   # ip = requests.get('https://api.ipify.org').text
    #print('My public IP address is: {}'.format(ip))


def kill_process_using_port(port):
    try:
        pid = subprocess.run(
            ['lsof', '-t', f'-i:{port}'], text=True, capture_output=True
        ).stdout.strip()
        if pid:
            if subprocess.run(['kill', '-TERM', pid]).returncode != 0:
                subprocess.run(['kill', '-KILL', pid], check=True)
            time.sleep(1)  # Give OS time to free up the PORT usage'''
    except:
        print("Maybe it is not Linux ???")

def bind():
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #utworzenie obiektu socket z użyciem konstruktora socket (do użycia z internetem AF_INET, z protokołem TCP - sock_stream)
    global curState
    curState = 'binding'
    if(linuxMode == 1):
        kill_process_using_port(9999) 
    try:
        server.bind((host, port))
        server.listen()
        conn()
    except:
        print('You might have messed up run order. Try restarting Phobos pls :___)')
        #kill_process_using_port(11111)
        time.sleep(5)
        bind()

def conn():
    global curState
    curState = 'connecting'
    try:
        global phobos, address
        phobos, address= server.accept()
        print(f'Connected with {address}')
        curState ='connected'
    except:
        print('Awaiting connection... ')
        time.sleep(5)
        conn()

def init():
    command_thread = threading.Thread(target=command)
    receive_thread = threading.Thread(target=receive)
    command_thread.start()
    receive_thread.start()
    isLinux()

def isLinux():
    global curState
    curState = 'isLinux'
    print("Enter 1 if program runs on Linux: ")
    isLin = input()
    global linuxMode

    if(isLin == '1'):
        linuxMode = 1
    else:
        linuxMode = 0
    bind()


def command():
        while True:
            try:
                msg = input()
                if(msg != ''):
                    handle(msg)
            except:
                time.sleep(1)


def receive():
    while True:
        try:
            message = phobos.recv(4096).decode('ascii')
            if(message != ''):
                print(message)
            #if(message != ''):
            #    handle(message)
        except:
            time.sleep(5)

            

def quitPrompt():
    global curState
    curState = 'quitPrompt'
    chooser = input('Enter ''stop'' to terminate')
    if(chooser =='stop'):
        print('goodbye')
        sys.exit()


def communicationBreakdown():
    global curState
    curState = 'communicationBreakdown'
    try:
        phobos.close()
    except:
        print('attempting to close connection ...')
        communicationBreakdown()


#'isLinux', 'streaming', 'connected', 'connecting', 'binding', 'quitPrompt'

def handle(handled): 
        if handled == "stop":
            if(curState == 'connecting' or curState == 'binding'):
                isLinux()
            elif(curState == 'connected' or curState =='streaming'):
                communicationBreakdown()
                isLinux()
            elif(curState == 'isLinux' or curState == 'quitPrompt'):
                quitPrompt()
                isLinux()
        elif(handled == 'browse'):
            #browse()
            print("waiting For Browse function")
        elif(curState == 'connected'):
            phobos.send(str(handled).encode('ascii'))
        if handled == 'film':
            video_stream()



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




"""q = queue.Queue(maxsize=10)
absolutePath = os.path.dirname(os.path.realpath(__file__))
relativePath = r"videos\vid1.mp4"
filename = os.path.join(absolutePath, relativePath)  
command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(filename,'temp.wav')
os.system(command)

BUFF_SIZE = 65536
vid = cv2.VideoCapture(filename)
FPS = vid.get(cv2.CAP_PROP_FPS)
global TS
TS = (0.5/FPS)
BREAK=False
totalNoFrames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
durationInSeconds = float(totalNoFrames) / float(FPS)
d=vid.get(cv2.CAP_PROP_POS_MSEC)



def video_stream():
    global TS
    fps,st,frames_to_count,cnt = (0,0,1,0)
    cv2.namedWindow('TRANSMITTING VIDEO')        
    cv2.moveWindow('TRANSMITTING VIDEO', 10,30) 
    while True:
        msg,client_addr = phobos.recvfrom(BUFF_SIZE)
        print('GOT connection from ',client_addr)
        WIDTH=400
        
        while(True):
            frame = q.get()
            encoded,buffer = cv2.imencode('.jpeg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
            message = base64.b64encode(buffer)
            phobos.sendto(message,client_addr)
            frame = cv2.putText(frame,'FPS: '+str(round(fps,1)),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            if cnt == frames_to_count:
                try:
                    fps = (frames_to_count/(time.time()-st))
                    st=time.time()
                    cnt=0
                    if fps>FPS:
                        TS+=0.001
                    elif fps<FPS:
                        TS-=0.001
                    else:
                        pass
                except:
                    pass
            cnt+=1
            
            
            
            cv2.imshow('TRANSMITTING VIDEO', frame)
            key = cv2.waitKey(int(1000*TS)) & 0xFF	
            if key == ord('q'):
                os._exit(1)
                TS=False
                break	"""