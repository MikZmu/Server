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
global page
page = 0
global result

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
    global result
    while (True):
        update.wait()
        clear()
        if(state == "browse"):
            if(initFlag == 1):
                 print('There was an error during adding files. Please check file name formatting')
            print("Bind Sate " + bindState + " :: "+ connState + '::: ip: ' + socket.gethostbyname(socket.gethostname()))
            print(f"Start Time: {startTime} **** End Time: {endTime}  **** Location: {location}")
            print("StartTime to set start time **** EndTime to set end time **** Location to set location **** Play to play video")
            print('next for next page ::: prev for previous page ::: reset to update database')
            print("StartTime: " + startTime + " EndTime: " + endTime + " location: " + location)
            result = video_base.VideoBase.dataToTable(location, startTime, endTime)
            try:
                for x in range(page * 10, ((page +1)  * 10)):
                    print("ID: "+str(result[x][0])+" Location: "+ result[x][1]+ " Time: " + result[x][2])
            except Exception as e:
                print(f"There was a problem with displaying data. Exception {e}")
            print("Page: " + str(page+1) + " out of " + str(int(len(result)/10+1)))
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
    global result
    global page
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
        elif(command == 'EndTime'):
                print("YYYY-MM-DD HH:MM:SS : ")
                endYear = input('year ')
                endMonth = input('month ')
                endDay = input('day ')
                endHour = input('hour ')
                endMinute = input('minute ')
                endSecond = input('second ')
                endTime = endYear+'-'+endMonth+'-'+endDay+" "+endHour+":"+endMinute+":"+endSecond
        elif(command == 'location'):
                location = input("location: ")
        elif(command == 'next'):
             if(page < len(result)):
                  page += 1
        elif(command == 'prev'):
             if(page > 0):
                  page -= 1
        elif(command == 'reset'):
             video_base.VideoBase.baseInit2()

        

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
        clearFlag = connection.getFlag()
        time.sleep(0.1)
        if(newconnState != connState or newbindState != bindState or clearFlag == 1):
            bindState = newbindState
            connState = newconnState
            connection.flag = 0
            update.set()

isLinux()
initFlag =video_base.VideoBase.baseInit2()
connection.isLinux()
commThd = threading.Thread(target=command)
commThd.start()
connThd = threading.Thread(target=connection.conn)
connThd.start()
stat = threading.Thread(target=status)
stat.start()
update = threading.Event()
inter = threading.Thread(target=interface)
inter.start()

