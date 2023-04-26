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
import concurrent.futures
#import requests 






global host, port, server, linuxMode, buffer
host = '0.0.0.0'
port = 9999
global state
state = ['isLinux', 'streaming', 'connected', 'connecting', 'binding', 'quitPrompt']
global curState
buffer = 65536
q = queue.Queue(maxsize=30)







#def getip():
   # ip = requests.get('https://api.ipify.org').text
    #print('My public IP address is: {}'.format(ip))





def kill_process_using_port(port):
    print("kill process")
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
    print('binding')
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
    print('connecting')
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
            videoTransmission(r"C:\Users\52 Blue\Documents\wbudowane\deimos\src\pepe.mp4")


def videoTransmission(video):
    command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(video,'temp.wav')
    os.system(command)

    """def vidBind():
        global server_socket
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host_name = socket.gethostname()
        host_ip = '0.0.0.0'
        vidPort = 9998
        try:
            server_socket.bind((host_ip, vidPort))
            server_socket.listen()
            vidConn()
        except Exception as e:
            print(str(e))
            #kill_process_using_port(11111)
            time.sleep(5)
            vidBind()

    def vidConn():
        try:
            global phobosVid, addressVid
            phobosVid, addressVid= server_socket.accept()
            print(f'Connected with {addressVid}')
        except:
            print('Awaiting connection... ')
            time.sleep(5)
            vidConn()"""




    def vidInfo():
        global vid
        vid = cv2.VideoCapture(video)
        global FPS
        FPS = vid.get(cv2.CAP_PROP_FPS)
        global TS
        TS = (0.5/FPS)
        global BREAK
        BREAK=False
        print('FPS:',FPS,TS)
        totalNoFrames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
        durationInSeconds = float(totalNoFrames) / float(FPS)
        d=vid.get(cv2.CAP_PROP_POS_MSEC)
        print(durationInSeconds,d)



    
    def video_stream_gen():
        WIDTH=400
        while(vid.isOpened()):
            try:
                _,frame = vid.read()
                frame = imutils.resize(frame,width=WIDTH)
                q.put(frame)
            except:
                os._exit(1)
        print('Player closed')
        global BREAK
        BREAK=True
        vid.release()

    def video_stream():
        global TS
        fps,st,frames_to_count,cnt = (0,0,1,0)
        """cv2.namedWindow('TRANSMITTING VIDEO')        
        cv2.moveWindow('TRANSMITTING VIDEO', 10,30) """
        while True:
            WIDTH=400
            
            while(True):
                frame = q.get()
                encoded,buffer = cv2.imencode('.jpeg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
                message = base64.b64encode(buffer)
                phobos.sendto(message,address)
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
                    break
    vidInfo()
    #vidBind()
    gen_thread = threading.Thread(target=video_stream_gen)
    stream_thread = threading.Thread(target=video_stream)
    gen_thread.start()
    stream_thread.start()
    



    

