import threading
import connection
import os
import subprocess
import msvcrt
import time
import socket
import video_base
import pickle
import base64
import cv2 as cv
import imutils
import queue
q = queue.Queue(maxsize=300)
global state
state = "main menu"
global linuxMode
global toggle
global stream
stream = False
toggle = False
global host
host = '0.0.0.0'
bindState = 'unbound'
connState = 'disconnected'
global vidConn
vidConn = 'disconnected'
global minTime, maxTime, location, result, page
minTime = '1900-01-01 00:00:00'
maxTime = '3000-12-31 23:25:29'
location = 'any'
page = 0
global minTimeRemote, maxTimeRemote, locationRemote
minTimeRemote = 'any'
maxTimeRemote = 'any'
locationRemote = 'any'
page = 0

def isLinux():
    print("IsLinux")
    from sys import platform
    global linuxMode
    if(platform == "linux" or platform == 'linux2'):    
        linuxMode = 1   
    else:
        linuxMode = 0



def interface():
    global linuxMode
    global toggle
    global page
    global state
    isLinux()
    while (True):
        clear()
        if(toggle==True):
            print("Connection: " + bindState + " :: "+ connState + f' with  {address} Video: ' + vidConn )
        else:
            print("Connection: OFF " + bindState + " :: " + connState)
        if(state == "main menu"):
            print("1: Browse")
            print("2: Toggle Connection")
            print("3: Display IP")
            print("Command: ")
            command = input()
            handle(command)
        if(state == "browse"):
            print("1: select place")
            print("2: select min time")
            print("3: select max time")
            print('4: next page')
            print('5 previous page')
            print("4: connection toggle")
            print("5: display ip")
            command = input()
            handle(command)




def handle(command):
    global minTime
    global maxTime
    global location
    global result
    global state
    print(command)
    if(state == "main menu"):
        if(command== '1'):
            result = video_base.VideoBase.dataToTable(location, minTime, maxTime)
            for row in result:
                print (str(row))
            state='browse'
        if(command =='2'):
            print("toggle connection")
            connectionToggle()
        if(command =='3'):
            print("display ip")
    elif(state == 'browse'):
        if(command=='1'):
            location = input ("Min time = ")
            result = video_base.VideoBase.dataToTable(location, minTime, maxTime)
            print (result)
        if(command=='2'):
            maxTime = input ('Max time = ' )
            result = video_base.VideoBase.dataToTable(location, minTime, maxTime)
        if(command=='3'):
            location = input("Location = ")
            result = video_base.VideoBase.fiBlobData(location, minTime, maxTime)
        


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


def play(asdf):
        command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(video,'temp.wav')
        os.system(command)


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
        







def clear():
    if(linuxMode == 1):
        clear = lambda: os.system('clear')
        clear()
    else:
        clear = lambda: os.system('cls')
        clear()


def connectionToggle():
    global toggle
    if(toggle == False):
#        global toggle
        toggle = True
        #connThread.start()
        connection(toggle, stream)
    else:
      #  global toggle
        toggle = False
        connection(toggle, stream)


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



def connection(toggle, stream):


    if(toggle == True):
        def bind():
            global server
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #utworzenie obiektu socket z użyciem konstruktora socket (do użycia z internetem AF_INET, z protokołem TCP - sock_stream)
            global curState
            global bindState
            curState = 'binding'
            print('binding')
            if(linuxMode == 1):
                kill_process_using_port(9999) 
            try:
                server.bind((host, 9999))
                server.listen()
                bindState = "bound"
                conn()
            except:
                bindState = 'unbound'
                time.sleep(5)
                bind()

        def conn():
            print('connecting')
            global connState
            global vidConn
            curState = 'connecting'
            try:
                global video, phobos, address
                phobos, address= server.accept()
                print(f'Connected with {phobos}')
                video, address = server.accept()
                print(f'Connected with {video}')
                connState ='connected'
                vidConn = 'connected'
                t1.start()
            except:
                print('Awaiting connection... ')
                time.sleep(5)
                bind()




        def receive():
            global connState
            while(True):
                try:
                    message = phobos.recv(4096).decode('ascii')
                    if(message != ''):
                        remoteHandle(message)
                except Exception as e:
                    print(e)
                    connState = 'disconnected'
                    time.sleep(5)
                    break


        def send(message):
            global connState
            try:
                phobos.send(str(message).encode('ascii'))
            except Exception as e:
                print(e)
                connState='disconnected'
                time.sleep(1)
                

        t1 = threading.Thread(target=receive)


        bind()




    













video_base.VideoBase.baseInit()
interface()