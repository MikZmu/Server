import sys
import connection
import threading
import os
import subprocess
import time
import socket
import video_base
import pickle
import base64
import imutils
import queue
q = queue.Queue(maxsize=300)
global state
state = "main menu"
global bindState
global connState
bindState = 'a'
connState = 'b'

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
    while (True):
        update.wait()
        clear()
        print("Bind Sate " + bindState + " :: "+ connState)
        if(state == "main menu"):
            print("1: Browse :: 2: Toggle Connection :: 3: Display IP")
            print("Command: ")
        elif(state == "browse"):
            print("1: select place :: 2: select min time :: 3: select max time :: 4: next page :: 5: previous page :: 6: connection toggle :: 7: display ip")
        update.clear()

def command():
    command = input()
    if(command!=""):
        update.set()
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

def status():
    global connState
    global bindState
    while(True):
        newconnState = connection.getConnState()
        newbindState = connection.getBindState()
        time.sleep(0.1)
        if(newconnState != connState or newbindState != bindState):
            bindState = newbindState
            connState = newconnState
            update.set()

isLinux()
video_base.VideoBase.baseInit()
connection.isLinux()
commThd = threading.Thread(target=command)
commThd.start()
isConnThd = threading.Thread(target=connection.checkSend)
isConnThd.start()
connThd = threading.Thread(target=connection.conn)
connThd.start()
stat = threading.Thread(target=status)
stat.start()
update = threading.Event()
inter = threading.Thread(target=interface)
inter.start()

