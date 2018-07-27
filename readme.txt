Download and copy the source code in any destination you like.

To make it easy, Copy it to Documents

Open Terminal(Mac/Linux) or CMD(Windows)


Type in the following commands:
    cd Documents
    cd excelv
    
    (You need to install the necessary modules to run the application which you can do by calling the 
    following command)

    pip3 install -r requirements.txt
    or
    pip install -r requirements.txt


Then you are ready to run the website
    In the same directory run:

    python3 manage.py runserver
    or
    python manage.py runserver

    Then to check it in the browser simply type the following address on the urlbar
    127.0.0.1:8000

IF YOU WANT TO RUN THE WEBSITE ACROSS MULTIPLE DEVICES:

1. you need to know your local IP address first which you can find out by running 'ipconfig' or 'ifconfig'
   on terminal or cmd.

2. After you know your network ipaddress, go to excelv folder inside excelv where you can see a file
   called 'settings.py'

    You can see this line. You have to modify the line.
    ALLOWED_HOSTS = []

    modified:
    ALLOWED_HOSTS = ['YOUR.NETWORK.IPADDRESS']

    eg:
    ALLOWED_HOSTS = ['192.168.1.100']

    Then simply run
    python3 manage.py runserver 192.168.1.100:8000

    this way you can you the website in different devices across same network

THE ADMINISTRATOR ACCOUNT FOR YOU TO LOGIN is 

username: dan
password: DanLin123


If you have any errors during these process, feel free to email me.