import socket;
import queue
import cv2 as cv
import os
import threading
import base64
import imutils

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'
port = 9999
global buffer
buffer = 999999
global q
q = queue.Queue(maxsize=200)

def VIDDEO(video):

    def bind():
        try:
            server_socket.bind((host,port))
            server_socket.listen()
        except Exception as e:
            print(e)
            bind()

    def conn():
        try:       
            global phobos, address
            phobos, address= server_socket.accept()
            video(r"C:\Users\52 Blue\Documents\wbudowane\deimos\src\pepe.mp4")
        except Exception as e:
            print(e)
            conn()
            





    def video(video):
        command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(video,'temp.wav')
        os.system(command)


        def vid_info():
                global vid
                vid = cv.VideoCapture(video)
                global FPS
                FPS = vid.get(cv.CAP_PROP_FPS)
                phobos.send(str(FPS).encode('ascii'))
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
                phobos.sendto(message,address)

        vid_info()
        str_gen_thd = threading.Thread(target=video_stream_gen)
        str_thd = threading.Thread(target=vid_stream)
        str_gen_thd.start()
        str_thd.start()



    bind()
    conn()