import socket
from PIL import Image
import io
import webbrowser, os
import sys
if len(sys.argv)==1:
    HOST = input("Enter hostname(IP address): ")
    PORT =int(input("Enter port number: "))
else:
    HOST = str(sys.argv[1])
    PORT = int(sys.argv[2])

#%%reads all requests from file
with open("inputfile.txt","r") as fp:
    request = fp.readline()
#%%        
    op = 'y'
    #takes user i/p for control and debugging purposes
    while request:
        
        #creating client socket
        clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #3 way handshaking with server
        clientSocket.connect((HOST,PORT))
        #formulate the complete request message with ip and port
        requestMSG = request.rstrip() + ' ' + HOST + ' ' + str(PORT)
        #split request to words to know type of request(GET or POST)
        requestType, requestedFile = request.rstrip().split(" ") 
        fileType = requestedFile.split(".")[1]
        
    #%% GET REQUEST
        if requestType == "GET":
            #send request as bytes to server
            clientSocket.sendall(requestMSG.encode())
            print(requestMSG)
            #wait to/ receive acknowledgement
            reply = clientSocket.recv(17)#size of acknowledgement message
            print('ACK: ',reply.decode())
    
            #in case of positive acknowledgement
            if reply.decode().split(" ")[1] == "200":
                #receive data 1kbyte at a time
                data = b"" 
                while True:
                    d= clientSocket.recv(1024)
                    data += d
                    print(len(d))
                    if len(d) < 1024:
                        break
                
    #%%         Receiving Text files   
                if fileType == "txt":
                    print(data.decode())
                    f = open(requestedFile,"wb")
                    f.write(data)
                    f.close()
                    
    #%%         Receiving HTML files
                if fileType == "html":
                    f = open(requestedFile,"wb")
                    f.write(data)
                    f.close()  
                    webbrowser.open('file://' + os.path.realpath(requestedFile))
                    
    #%%         Receiving Images
                if (fileType == "jpg") or ( fileType == "jpeg"):
                    img = Image.open(io.BytesIO(data))
                    img.show()
                    img.save(requestedFile,"JPEG")
                    
    #%%        POST REQUESTS
        elif requestType == "POST":
             #send request as bytes to server
            clientSocket.sendall(requestMSG.encode())
            print(requestMSG)
            #wait to/ receive acknowledgement
            reply = clientSocket.recv(17)#size of acknowledgement message
            print('ACK: ',reply.decode())
            #wait to/ receive data 
            try:
                file = open(requestedFile,"rb").read()
                clientSocket.sendall(file)
            except IOError:
                clientSocket.sendall(b"HTTP/1.0 404 NOT FOUNd\r\n")
            print("SENT ")
                
     #%%       
        clientSocket.close()
        print("Client Socket closed")
    #%%
        request = fp.readline()
        op = input('more operations ? y/n? ')
        if op == 'n':
            break

