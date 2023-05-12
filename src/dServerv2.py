import socket
import threading
import concurrent.futures
import queue
import time
import sys
import subprocess
import os
import cv2 as cv
import imutils
import base64
import queue

global host, port, vidPort, server, linuxMode, buffer,state
host = '0.0.0.0'
port = 9999
vidPort = 9998
buffer = 999999
q = queue.Queue(maxsize=200)


def init():
    print("Initializing")
    sendThd = threading.Thread(target=command)
    rcvThd = threading.Thread(target=receive)
    sendThd.start()
    rcvThd.start()
    clientBind()

def command():
        while True:
            try:
                msg = input()
                if(msg != ''):
                    handleLocal(msg)
            except:
                time.sleep(1)


def receive():
    while True:
        global client
        message = client.recv(4096).decode('ascii')
        if(message!=""):
            handleForeigh(message)


def handleLocal(msg):
    if(msg == "video"):
        VIDDEO(r"C:\Users\52 Blue\Documents\wbudowane\deimos\src\pepe.mp4")


def handleForeigh(msg):
    print(msg)
    
    
    


def isLinux():
    print("IsLinux")
    from sys import platform
    global linuxMode
    if(platform == "linux" or platform == 'linux2'):    
        return 1
        clientBind()
    else:
        return 0
        clientBind()


def clientBind():
    print("Binding Client")
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    global linuxMode
    linuxMode = isLinux()
    if(linuxMode == 1):
        kill_process_using_port(9999) 
    try:
        server.bind((host, port))
        server.listen()
        clientConn()
    except:
        print('You might have messed up run order. Try restarting Phobos pls :___)')
        time.sleep(5)
        clientBind()


def kill_process_using_port(port):
    print("Killing Process")
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


def clientConn():
    print("Connecting Client")
    curState = 'connecting'
    try:
        global client, address
        client, address= server.accept()
        print(f'Connected with {address}')
        curState ='connected'
    except:
        print('Awaiting connection... ')
        time.sleep(5)
        clientBind()





def VIDDEO(video):

    def postClientConn():
        print("Post connection")
        while(True):
                global vidClient, address
                vidClient, address= server.accept()
                print(f'Video connected with {address}')

    def video():
        command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(video,'temp.wav')
        os.system(command)


        def vid_info():
                global vid
                vid = cv.VideoCapture(video)
                global FPS
                FPS = vid.get(cv.CAP_PROP_FPS)
                vidClient.send(str(FPS).encode('ascii'))
                global TS
                TS = (0.5/FPS)
                global BREAK
                BREAK=False
                print('FPS:',FPS,TS)
                totalNoFrames = int(vid.get(cv.CAP_PROP_FRAME_COUNT))
                durationInSeconds = float(totalNoFrames) / float(FPS)
                d=vid.get(cv.CAP_PROP_POS_MSEC)
                print(durationInSeconds,d)

        def video_stream_gen():
            WIDTH=400
            while(vid.isOpened()):
                try:
                    _,frame = vid.read()
                    frame = imutils.resize(frame,width=WIDTH)
                    q.put(frame)
                    print(q.qsize())
                except:
                    os._exit(1)
            print('Player closed')
            global BREAK
            BREAK=True
            vid.release()

        def vid_stream():
            while(True):
                frame = q.get()
                frame = cv.putText(frame,'FPS: '+str(FPS),(10,40),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)   
        
                encoded,buffer = cv.imencode('.jpeg',frame,[cv.IMWRITE_JPEG_QUALITY,80])
                message = base64.b64encode(buffer)
                print(message)
                vidClient.sendto(message,address)

        vid_info()
        postClientConn()
        str_gen_thd = threading.Thread(target=video_stream_gen)
        str_thd = threading.Thread(target=vid_stream)
        str_gen_thd.start()
        str_thd.start()