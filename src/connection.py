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


def isLinux():
    print("IsLinux")
    from sys import platform
    global linuxMode
    if(platform == "linux" or platform == 'linux2'):    
        linuxMode = 1   
    else:
        linuxMode = 0

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

def connection():
        
        def receive():
            global connState
            while(True):
                try:
                    message = phobos.recv(4096).decode('ascii')
                    if(message != ''):
                        remoteHandle(message)
                except Exception as e:
                    connState = 'disconnected'
                    time.sleep(3)
                    bind()
        
        def conn():
            global connState
            global vidConn
            try:
                global video, phobos, address
                phobos, address= server.accept()
                video, address = server.accept()
                connState ='connected'
                vidConn = 'connected'
                t1 = threading.Thread(target=receive)
                t1.start()
            except Exception as e:
                connState = str(e)
                vidConn = str(e)
                time.sleep(3)
                bind()

        def bind():
            global server
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #utworzenie obiektu socket z użyciem konstruktora socket (do użycia z internetem AF_INET, z protokołem TCP - sock_stream)
            global curState
            global bindState
            if(linuxMode == 1):
                kill_process_using_port(9999) 
            try:
                server.bind((host, 9999))
                server.listen()
                bindState = "bound"
                conn()
            except Exception as e:
                bindState = str(e)
                time.sleep(3)
                bind()

        while(True):
            if(bindState != 'bound'):
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
    if(split[0]=='play'):
        id = split[1]
        videoRecord = video_base.VideoBase.playQuery(id)
        path = videoRecord[0][3]
        play(path)

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
    
def getVidStete():
     try:
          return vidConn
     except:
          return 'disconnected'

def play(asdf):


        def vid_info():
                global vid
                #rawPath = r"{}".format(asdf)
                vid = cv.VideoCapture(asdf)
                global FPS
                FPS = vid.get(cv.CAP_PROP_FPS)
                video.send(str(FPS).encode('ascii'))
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
            stop = False
            while(stop == False):
                try:
                    _,frame = vid.read()
                    frame = imutils.resize(frame,width=WIDTH)
                    q.put(frame)
                    print(q.qsize())
                except:
                    break
                    time.sleep(1)
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
                video.send(message)

        vid_info()
        str_gen_thd = threading.Thread(target=video_stream_gen)
        str_thd = threading.Thread(target=vid_stream)
        str_gen_thd.start()
        str_thd.start()