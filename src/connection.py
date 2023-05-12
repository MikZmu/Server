import socket
import threading
import queue
import time
import subprocess
global host
global bindState
bindState = "unbound"
global connState
connState = 'disconnected'
host = "0.0.0.0"
global stream
stream = False
global toggle
toggle = False

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
                print('You might have messed up run order. Try restarting Phobos pls :___)')
                #kill_process_using_port(11111)
                time.sleep(5)
                bind()

        def conn():
            print('connecting')
            global connState
            curState = 'connecting'
            try:
                global phobos, address
                phobos, address= server.accept()
                print(f'Connected with {address}')
                connState ='connected'
                t1 = threading.Thread(target=receive)
                t1.start()
            except:
                print('Awaiting connection... ')
                time.sleep(5)
                bind()

        bind()


        if(stream):
            def postClientConn():
                print("Post connection")
                global vidClient, address
                while(stream):
                    vidClient, address= server.accept()
                    print(f'Video connected with {address}')


            def receive():
                while(True):
                    try:
                        message = phobos.recv(4096).decode('ascii')
                        if(message != ''):
                            print(message)
                        #if(message != ''):
                        #    handle(message)
                    except:
                        time.sleep(5)




            

            


            