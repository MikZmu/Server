# https://youtu.be/YwWfKitB8aA
import socket

host = socket.gethostbyname(socket.gethostname())  #24:50 dla VB
port = 2137

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #utworzenie obiektu socket z użyciem konstruktora socket (do użycia z internetem AF_INET, z protokołem TCP - sock_stream)
server.bind((host, port))

server.listen(10)

while True:
    communication_socket, address = server.accept()  
    #server.accept zwraca adres nadchodzącego połączenia i inny socket którego możemy użyć do połączenia - 
    #dla każdego połączenia tworzymy nowy socket do komunikacji z klientem server socket jest tylko do akceptowania przychodzących połączeń
    print(f"Connected with {address}" )
    message = communication_socket.recv(4096).decode() #recv(rozmiar bufora w bitach)  wiadomość jest otrzymana w formacie bitowym -> musi zostać zdekodowana
    print(f"Message is: {message}")
    communication_socket.send("Gotcha... Anything else ?".encode('utf-8')) #utf-8 -> 8-bit Unicode Transformation Format
    communication_socket.close()
    print(f"Connection with {address} ended")