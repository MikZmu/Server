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
global bindState
global connState
global vidConn
bindState = 'unbound'
connState = 'disconnected'
vidConn = 'disconnected'

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
        print("Bind Sate " + bindState + " :: "+ connState + f'  Video: ' + vidConn )
        if(state == "main menu"):
            print("1: Browse :: 2: Toggle Connection :: 3: Display IP")
            print("Command: ")
            command = input()
            handle(command)
        if(state == "browse"):
            print("1: select place :: 2: select min time :: 3: select max time :: 4: next page :: 5: previous page :: 6: connection toggle :: 7: display ip")
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
        elif(command =='2'):
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
        



        







def clear():
    if(linuxMode == 1):
        clear = lambda: os.system('clear')
        clear()
    else:
        clear = lambda: os.system('cls')
        clear()

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

def getState():
    while(True):
        global connState
        connState = connection.getConnState()
        global bindState
        bindState = connection.getBindState()
        global vidConn
        vidConn = connection.getVidState()
        time.sleep(5)


video_base.VideoBase.baseInit()
connection.isLinux()
connThd = threading.Thread(target=connection.connection)
connThd.start()
interface()