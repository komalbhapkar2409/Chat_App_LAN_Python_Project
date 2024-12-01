import socket
import os
import hashlib
import time

# Server Code (User 2)

message = ""
Hash_server = b''

while message != "bye":
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9999))  #127.0.0.0
    server.listen(1)

    message = ""
    print("Server is listening on port 9999...")

    conn, addr = server.accept()

    #print(f"Connection established with {addr}")

    try:
        
        #file name
        file_name = conn.recv(1024).decode()
        print("Receiving file: {file_name}")
        #file size
        file_size = int(conn.recv(1024).decode())
        print(f"Expected file size: {file_size} bytes")

        # Open a file to write the received data
        with open("Received_" + os.path.basename(file_name), "wb") as file:
            received_size = 0
            while True:
                data = conn.recv(1024)
                
                if data == b"END":  # End of transmission
                    print("End of file transmission detected.")
                    break
                file.write(data)
                received_size += len(data)
                #Hash_server = hashlib.md5(data).hexdigest()
                
                print(f"Received {received_size}/{file_size} bytes", end="\r")

        #time.sleep(1)        
        Hash_From_sender_Client = conn.recv(1024)
                
        file_path = "Received_Messagefrom_U1.txt"
        File_1 = open(file_path,'r')

        message = File_1.read()
        
        Hash_server = hashlib.md5(message.encode()).hexdigest()
        
        if Hash_From_sender_Client.decode() == Hash_server:
            print("Received Message is successfully Hash Verified")
            print('Message Received from Client : ',message)
        else:
            print("Message is tampered")
        
        File_1.close()
        
        #print("\nHash of the message : ",Hash_server)
        #print("\nFile received successfully!")

        

    except Exception as e:
        print(f"An error occurred: {e}")
    except ValueError as ve:
        print(f"Error (Ex. Empty message): {ve}")
    finally:
        #conn.close()
        print(f" ")
        #server.close()
        #Socket is getting close outside of while loop

    ###########################################

    server_address_2 = ('localhost', 9998) 

    message = input("write message For Client : ")
    # Path to the file to be sent
    #file_path_send = "A:\\Work\\ttt\\Text_From_ServerU2.txt"
    file_path_send = "Text_From_ServerU2.txt"
    File_2 = open(file_path_send,'w')
    File_2.write(message)
    File_2.close()

    file_size = os.path.getsize(file_path_send)
    Server_send_to_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Server_send_to_client.connect(server_address_2)

    Server_send_to_client.send(str(file_path_send).encode())
    print(f"Sent file name: {os.path.basename(file_path_send)}")

    file_size = os.path.getsize(file_path_send)

    # Send the file size
    Server_send_to_client.send(str(file_size).encode())

    time.sleep(0.2)

    with open(file_path_send, "rb") as file:
        print("Sending file data...")
        while chunk := file.read(1024):  # Read 1 KB chunks
            Server_send_to_client.send(chunk)

    # Send the end-of-file marker
    time.sleep(0.5)
    Server_send_to_client.send(b"END")

    
    #print("File sent successfully from server!")
    Hash_Ff = hashlib.md5(bytes(message.encode())).hexdigest()

    #time.sleep(1)  
    Server_send_to_client.send(Hash_Ff.encode())

    
    #print(f"Socket is closed")

Server_send_to_client.close()
conn.close()         
server.close()