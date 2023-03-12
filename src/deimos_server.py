# https://youtu.be/YwWfKitB8aA
import socket

host = socket.gethostbyname(socket.gethostname())  #24:50 dla VB
port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #utworzenie obiektu socket z użyciem konstruktora socket (do użycia z internetem AF_INET, z protokołem TCP - sock_stream)
server.bind((host, port))
server.listen()
communication_socket, address = server.accept()  

def deimosConnect():
    done = False
    while not done:
        #server.accept zwraca adres nadchodzącego połączenia i inny socket którego możemy użyć do połączenia - 
        #dla każdego połączenia tworzymy nowy socket do komunikacji z klientem server socket jest tylko do akceptowania przychodzących połączeń
        incoming = communication_socket.recv(4096).decode('utf-8')
        if incoming == " ":
            communication_socket.close()
            done = True
        else:
            print(incoming)
        #communication_socket.close()
        communication_socket.send(input("Message: ").encode('utf-8'))

deimosConnect()