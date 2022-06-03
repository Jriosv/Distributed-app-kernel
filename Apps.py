import socket
import pickle
import subprocess
import threading
import os
import psutil
import sys

def recv_msg():
    try:
        received_msg = app_socket.recv(1024)
        return pickle.loads(received_msg) 
    except:   
        return False

def send_msg(cmd,src,dst,msg):
    msg = {'cmd':cmd,
           'src': src,
           'dst': dst,
           'msg' : msg
           }
    serialized_msg = pickle.dumps(msg)
    app_socket.send(serialized_msg)

def init_app(app_number: int):
    if app_number == 1:
        global app1
        app1 = subprocess.Popen('notepad')
    elif app_number == 2:
        global app2
        app2 = subprocess.Popen('snippingtool') 
    elif app_number == 3:
        try:
            command = 'C:/Users/julii/AppData/Local/Programs/Python/Python38/python.exe "c:/Users/julii/OneDrive/Documentos/EAFIT/Sistemas operativos/Trabajo final/src/manual_calc.py"'
            proc = subprocess.check_output(command, stderr=subprocess.STDOUT)
            # do something with output
        except subprocess.CalledProcessError:
            print('failed')

def close_app(app_number: str):
    if app_number == 1:
        app1.kill()
    elif app_number == 2:
        app2.kill()
    elif app_number == 3:
        pass
      
#---------------------------------------------------------------------------La ejecución del modulo empieza aquí-----------------------------------------------------

app_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
app_socket.connect((socket.gethostname(),1234))

msg = app_socket.recv(1024)
print(msg.decode('utf-8') + ' Apps')


send_msg(cmd='register',
         src='apps',
         dst= 'kernel',
         msg= 'OK')

def get_info_by_id(pid_id: str):
    process_pid = psutil.Process(pid_id)
    # Gives You PID ID, name and started date# psutil.Process(pid=1216, name='ATKOSD2.exe', started='21:38:05')# Name of the process
    process_name = process_pid.name()
    status = process_pid.status()
    mesage = f'{process_name} {status}'
    return mesage


while True:
    msg = recv_msg()
    
    if msg is not False:
        if msg['cmd'] == 'close':
            if msg['msg'] == 'app1':
                close_app(1)
        
            if msg['msg'] == 'app2':
                close_app(2)

            if msg['msg'] == 'app3':
                close_app(3)

        if msg['cmd'] == 'init':
            if msg['msg'] == 'app1':
                init_app(1)

            if msg['msg'] == 'app2':
                init_app(2)

            if msg['msg'] == 'app3':
                init_app(3)
        
        if msg['cmd'] == 'info':
            print('llegó la info')
            send_msg(cmd='answer',
                     src='apps',
                     dst='gui',
                     msg= get_info_by_id(msg['msg']))
        
        if msg['cmd'] == 'stop':
            app_socket.close()
            sys.exit()
 
    
            
    

