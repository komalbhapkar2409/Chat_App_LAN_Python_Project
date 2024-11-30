import os
import socket
import hashlib
import time

#Client Code (User 1)
# Server details
server_address = ('localhost', 9999)  


print(server_address)
message = ""

class HashHandler:
    """Class to handle hash calculation and verification."""
    
    def __init__(self, message=""):
        self.message = message
        
    def generate_hash(self):
        """Generate MD5 hash for the given message."""
        
        return hashlib.md5(self.message.encode()).hexdigest()

    def verify_hash(self, received_hash):
        """Verify if the received hash matches the hash of the message."""
        generated_hash = self.generate_hash()
        
        if generated_hash == received_hash.decode():
            return True
        return False

while True:
    print(' ')
    message = input("write message for Server  : ")
    # Path to the file to be sent
    #file_path = "A:\\Work\\ttt\\Messagefrom_U1.txt"
    file_path = "Messagefrom_U1.txt"
    File_1 = open(file_path,'w')
    File_1.write(message)
    File_1.close()

    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Get the file size
        file_size = os.path.getsize(file_path)

        # Create a TCP client socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client.connect(server_address)
        print(f"Connected to server at {server_address}")

        # Send the file name
        client.send(os.path.basename(file_path).encode())
        #print(f"Sent file name: {os.path.basename(file_path)}")

        time.sleep(0.1)
        # Send the file size
        client.send(str(file_size).encode())
        #print(f"Sent file size: {file_size} bytes")

        time.sleep(0.2)

        # Open the file and send its contents in chunks
        with open(file_path, "rb") as file:
            print("Sending file data...")
            while chunk := file.read(1024):  # Read 1 KB chunks
                client.send(chunk)
            
        # Send the end-of-file marker
        time.sleep(0.5)
        client.send(b"END")
        #print("File sent successfully!")
        hash_handler = HashHandler(message)
        hash_from_sender_client = hash_handler.generate_hash()  # Generate hash from client message
        client.send(hash_from_sender_client.encode())
        #print("The sender hex is------ ", hashlib.md5(bytes(message.encode())).hexdigest())
        #print("The sender hex is after and ------ ",( int(Hash_From_sender_Client.encode()) & int(key.encode())))
        

    except ConnectionRefusedError:
        print("Could not connect to the server. Is it running and listening on the correct port?")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        #client.close()
        print(" ")
        #Connection closed out side of the while loop.

################################################################################

    server_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_send.bind(('localhost', 9998))
    server_send.listen(2)

    conn_send, addr_send = server_send.accept()

    file_name = conn_send.recv(1024).decode()
    #print(f"Receiving file: {file_name}")
    

    # Receive the file size
    file_size = int(conn_send.recv(1024).decode())
    #print(f"Expected file size: {file_size} bytes")


    # Open a file to write the received data
    with open("Received_" + os.path.basename(file_name), "wb") as file:
        received_size = 0
        while True:
            data = conn_send.recv(1024)
            if data == b"END":  # End of transmission
                print("End of file transmission detected.")
                break
            file.write(data)
            received_size += len(data)
            Hash_Client = hashlib.md5(data).hexdigest()
            print(f"Received {received_size}/{file_size} bytes", end="\r")

    #time.sleep(0.5)
    Hash_From_sender_Server = conn_send.recv(1024)########

    file_path = "Received_Text_From_ServerU2.txt"
    File_3 = open(file_path,'r')
    

    message = File_3.read()

    hash_handler = HashHandler(message)  # Use message from file to verify

    #print('Received message is ', message)
    #print('Received Hash is ',Hash_From_sender_Server)
    
    if hash_handler.verify_hash(Hash_From_sender_Server):
        print("Received Message is successfully Hash Verified")
        print('Message Received from Server : ',message)
    else:
        print("Message is tampered")
    #print(message)
    File_3.close()

    server_send.close()
    conn_send.close()

    if message == 'bye':
        time.sleep(1)
        print("Exiting client.")
        break


client.close()
conn_send.close()
server_send.close()
print("Connection closed.")