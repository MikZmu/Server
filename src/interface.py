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
state = "browse"
global bindState
global connState
bindState = 'a'
connState = 'b'
global startTime
startTime = '1900-01-01 00:00:00'
global endTime
endTime = '3000-12-31 23:25:29'
global location
location = 'atrium'

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
        if(state == "browse"):
            print("Bind Sate " + bindState + " :: "+ connState)
            print('1 : connection setup **** 2 : connect **** 3 : menu **** 4 : show state')
            print(f"Start Time: {startTime} **** End Time: {endTime}  **** Location: {location}")
            print("StartTime to set start time **** EndTime to set end time **** Location to set location **** Play to play video")
            result = video_base.VideoBase.dataToTable(location, startTime, endTime)
            try:
                for row in result:
                    print("ID: "+str(row[0])+" Location: "+ row[1]+ " Time: " + row[2])
            except Exception as e:
                print(f"There was a problem with displaying data. Exception {e}")
            print("Command: ")
        update.clear()

def command():
    while(True):
        command = input()
        if(command != ""):
            handle(command)
            update.set()


def handle(command):
    global startTime
    global endTime
    global location
    if(state == 'browse'):
        if(command == 'StartTime'):
                print("YYYY-MM-DD HH:MM:SS : ")
                startYear = input('year ')
                startMonth = input('month ')
                startDay = input('day ')
                startHour = input('hour ')
                startMinute = input('minute ')
                startSecond = input('second ')
                startTime = startYear+'-'+startMonth+'-'+startDay+" "+startHour+":"+startMinute+":"+startSecond
        if(command == 'EndTime'):
                print("YYYY-MM-DD HH:MM:SS : ")
                endYear = input('year ')
                endMonth = input('month ')
                endDay = input('day ')
                endHour = input('hour ')
                endMinute = input('minute ')
                endSecond = input('second ')
                endTime = endYear+'-'+endMonth+'-'+endDay+" "+endHour+":"+endMinute+":"+endSecond
        if(command == 'location'):
                location = input("location: ")
        

def clear():
    if(linuxMode == 1):
        clear = lambda: os.system('clear')
        clear()
    else:
        clear = lambda: os.system('cls')
        clear()



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
initFlag =video_base.VideoBase.baseInit2()
connection.isLinux()
commThd = threading.Thread(target=command)
commThd.start()
#isConnThd = threading.Thread(target=connection.checkSend)
#isConnThd.start()
connThd = threading.Thread(target=connection.conn)
connThd.start()
stat = threading.Thread(target=status)
stat.start()
update = threading.Event()
inter = threading.Thread(target=interface)
inter.start()

