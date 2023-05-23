import subprocess
import time
import socket
import threading
import video_base
import pickle
import cv2 as cv
import os
import imutils
import queue
import base64
import pyshine as ps

HTML="""
<html>
<head>
<title>PyShine Live Streaming</title>
</head>

<body>
<center><h1> PyShine Live Streaming using OpenCV </h1></center>
<center><img src="stream.mjpg" width='640' height='480' autoplay playsinline></center>
</body>
</html>
"""

global q
q = queue.Queue(maxsize=10000)
global bindState
global connState
bindState = 'unbound'
connState = 'disconnected'
global host
host = '0.0.0.0'
global minTime, maxTime, location, result, page
minTime = '1900-01-01 00:00:00'
maxTime = '3000-12-31 23:25:29'
location = 'any'
global minTimeRemote, maxTimeRemote, locationRemote
minTimeRemote = 'any'
maxTimeRemote = 'any'
locationRemote = 'any'
StreamProps = ps.StreamProps
StreamProps.set_Page(StreamProps,HTML)
address2 = (socket.gethostbyname(socket.gethostname()),9998)





def isLinux():
    print("IsLinux")
    from sys import platform
    global linuxMode
    if(platform == "linux" or platform == 'linux2'):    
        linuxMode = 1   
    else:
        linuxMode = 0

def receive():
    global connState
    global bindState
    while(True):
        try:
            message = phobos.recv(1024).decode('ascii')
            if(message != ''):
                remoteHandle(message)
        except Exception as e:
            bindState = 'unbound'
            connState = 'disconnected'
            break
           

def conn2():
    global connState
    global bindState
    global vidConn
    try:
        global video, phobos, address
        phobos, address= server.accept()
        connState ='connected'
        t1 = threading.Thread(target=receive)
        t1.start()
    except Exception as e:
        bindState = 'unbound'
        connState = str(e)
        time.sleep(3)
        bind()

def bind():
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #utworzenie obiektu socket z użyciem konstruktora socket (do użycia z internetem AF_INET, z protokołem TCP - sock_stream)
    global curState
    global bindState
    try:
        server.bind((host, 9999))
        server.listen()
        bindState = "bound"
        conn2()
    except Exception as e:
        bindState = str(e)
        time.sleep(3)
        bind()


def send(message):
            global connState
            try:
                phobos.send(str(message).encode('ascii'))
            except Exception as e:
                print(e)
                connState='disconnected'
                time.sleep(1)
                
def remoteHandle(handled):
    split = handled.split("&")
    global minTimeRemote
    global locationRemote
    if(split[0]=='request'):
        locationRemote =split[1]
        minTimeRemote = split[2]
        maxTimeRemote = split[3]
        tableRemote = video_base.VideoBase.dataToTable(locationRemote,minTimeRemote,maxTimeRemote)
        pickleTable = pickle.dumps(tableRemote)
        phobos.send(pickleTable)
    elif(split[0]=='play'):
        id = split[1]
        videoRecord = video_base.VideoBase.playQuery(id)
        path = videoRecord[0][3]
        play2(path)

def getConnState():
    try:
        return connState
    except:
        return 'disconnected'

def getBindState():
    try:
        return bindState
    except:
        return 'unbound'



def play2(asdf):
    def awaitStop():
        while(True):
            mess = phobos.recv(1024).decode('ascii')
            if(mess == 'stop'):
                capture.release()
                strm.socket.close()
                break

    try:
        StreamProps.set_Mode(StreamProps,'cv2')
        capture = cv.VideoCapture(asdf)
        capture.set(cv.CAP_PROP_BUFFERSIZE,4)
        capture.set(cv.CAP_PROP_FRAME_WIDTH,320)
        capture.set(cv.CAP_PROP_FRAME_HEIGHT,240)
        fps = capture.get(cv.CAP_PROP_FPS)
        capture.set(cv.CAP_PROP_FPS,fps)
        StreamProps.set_Capture(StreamProps,capture)
        StreamProps.set_Quality(StreamProps,90)
        strm = ps.Streamer(address2,StreamProps)
        phobos.send(str(address2[1]).encode("ascii"))
        print('Server started at','http://'+address2[0]+':'+str(address2[1]))
        stopThd = threading.Thread(target=awaitStop)
        stopThd.start()
        strm.serve_forever()
    except Exception as e:
        print(str(e))
        capture.release()
        strm.socket.close()


def conn():
    while(True):
        if(bindState != 'bound'):
            bind()
        time.sleep(0.1)




"""def isConnected():
    global bindState
    global connState
    global phobos
    while():
        time.sleep(0.1)
        try:
            phobos.send("w".encode("ascii"))
            connState = "connected"
            bindState = 'bound'
        except Exception as e:
            bindState = 'unbound'
            connState = 'disconnected'"""