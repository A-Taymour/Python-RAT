# Python-RAT


This is a python remote access virus, can be compiled using PYINSTALLER, giving remote access to the target machine, screenshots, and other usages.
The virus leaves a copy called "windows32" in the AppData in case it runs on windows and for constant shell; it creates a startup in the registry 

To delete it :
1. go to : HKCU\Software\Microsoft\Windows\CurrentVersion\Run
2. Delete the registry called 'toasted'
3. Deleting the .exe is optional 


## Installation

1. Clone the repository.
2. Install dependencies using `npm install` or `pip install -r requirements.txt`.
3. Run server.py on your C2 server
4. compile and send the reverse_shell.py

use -h for help
Change IP_ADRESS to your C2 server IP
