import subprocess
import time
import socket
import threading
import video_base
import pickle
import cv2 as cv
import os
import pyshine as ps
import sys

HTML="""
<html>
<head>
<title>stream uwu</title>
</head>

<body>
<center><h1> UWUOWO </h1></center>
<center><img src="stream.mjpg" width='640' height='480' autoplay playsinline></center>
</body>
</html>
"""
global flag
flag = 0
global bindState
global connState
bindState = 'unbound'
connState = 'disconnected'
global host
host = '0.0.0.0'
minTime = '1900-01-01 00:00:00'
maxTime = '3000-12-31 23:25:29'
location = 'any'
global minTimeRemote, maxTimeRemote, locationRemote
StreamProps = ps.StreamProps
StreamProps.set_Page(StreamProps,HTML)
address2 = ("0.0.0.0",9998)




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
            elif(message ==  b""):
                bindState = 'unbound'
                connState = 'disconnected'
                break
        except Exception as e:
            bindState = 'unbound'
            connState = 'disconnected'
            break
           

def conn2():
    global connState
    global bindState
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
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
    global maxTimeRemote
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
        if(len(videoRecord)== 0):
            phobos.send('stop'.encode("ascii"))
            return 0
        path = videoRecord[0][3]
        play2(os.path.abspath(path))

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
    
def getFlag():
    return flag



def play2(asdf):
    global flag
    print(asdf)
    def awaitStop():
        while(True):
            mess = phobos.recv(1024).decode('ascii')
            if(mess == 'stop'):
                capture.release()
                strm.shutdown()
                break
            else:
                remoteHandle(mess)

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
        phobos.send(str(fps).encode("ascii"))
        phobos.send(str(address2[1]).encode("ascii"))
        print('Server started at','http://'+address2[0]+':'+str(address2[1]))
        stopThd = threading.Thread(target=awaitStop)
        stopThd.start()
        strm.serve_forever()
    except Exception as e:
        capture.release()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        strm.shutdown()
    
    flag = 1
    


def conn():
    while(True):
        if(bindState != 'bound'):
            bind()
        time.sleep(0.1)




