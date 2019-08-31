import socket
import _thread
from PIL import Image
import webbrowser, os
import sys
def parse_Command(sentence):
    words = sentence.split(" ")
    print(words)
    check1 = 1
    check2 = 1
    if not len(words) == 4 :
        check1 = 0
    if not words[3] == "8080":
        print(words[3])
        check2 = 0
    check = check1 & check2
    return words,check
    
def on_new_client(conn,addr):
    
    sentence = conn.recv(1024).decode()
    print(sentence)
    sentence,check = parse_Command(sentence)
    if check == 0:
        conn.sendall(b"invalid command")
        conn.close()
        return
    command = sentence[0]
    if command == "GET":
        file_Name = sentence[1]
        message = ""
        print(file_Name)
        try:
            message = open(file_Name,"rb").read()
            conn.sendall(b"HTTP/1.0 200 OK\r\n")
        except IOError:
            message = "HTTP/1.0 404 Not Found\r\n"
            message = message.encode()
        conn.sendall(message)
        conn.close()
    
    
    
    elif  command == "POST":
        conn.sendall(b"HTTP/1.0 200 OK\r\n")
        file_P = sentence[1]
        file_name,file_type = file_P.split(".")
        #divide chunks
        data = b""
        while True:
            d = conn.recv(256)
            data+=d
            if len(d)<256:
                break
        
        
        
        #data = data.decode()
        #end recieving here
        if file_type == "txt":
            f = open(file_P,"wb")
            f.write(data)
            f.close()
                
        if (file_type == "jpg") or ( file_type == "jpeg"):
            img = Image.open(io.BytesIO(data))
            img.show()
            img.save(file_P,"JPEG")

        if file_type == "html":
            f = open(file_P,"wb")
            f.write(data)
            f.close()
            webbrowser.open('file://' + os.path.realpath(file_P))
        conn.close()
        
    else:
        print("fuck")
        conn.sendall(b"invalid command")
        conn.close()
 
if len(sys.argv)==1:
    Host = input("Enter hostname(IP address): ")
    serverPort =int(input("Enter port number: "))
else:
    Host = str(sys.argv[1])
    serverPort = int(sys.argv[2])
#Host = '192.168.0.1'
#serverPort = 8080

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind((Host,serverPort))
x = 0
op = 'y'
while not x==5:
    
    serverSocket.listen(1)
    conn, addr = serverSocket.accept()
    _thread.start_new_thread(on_new_client,(conn,addr))
    x = x + 1    
    op = input("continue? y/n? ")
    if op =='n':
        break