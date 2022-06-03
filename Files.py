import socket
import pickle
import os
import datetime
import sys

LOGS_PATH = 'C:\\Users\\julii\\OneDrive\\Documentos\\EAFIT\\Sistemas operativos\\Trabajo final\\src\\logs\\'

def create_file(file_name: str):
    f = open(f'{LOGS_PATH}{file_name}.txt', 'w')

def delete_file(file_name: str):
    os.remove(f'{LOGS_PATH}{file_name}.txt')

def write_log(msg: str):
    files = os.listdir(LOGS_PATH)
    for file in files:
        with open(f'{LOGS_PATH}{file}','a') as f:
            f.write(f'\n{msg}')
            

def recv_msg():
    try:      
        received_msg = files_socket.recv(1024)
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
    files_socket.send(serialized_msg)

#---------------------------------------------------------------------------La ejecución del modulo empieza aquí-----------------------------------------------------

files_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
files_socket.connect((socket.gethostname(),1234))

msg = files_socket.recv(1024)
print(msg.decode('utf-8') + ' Files')

date = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
write_log(f'[REGISTER]({date}) source:files destination:kernel message:OK')

send_msg(cmd='register',
         src='files',
         dst= 'kernel',
         msg= 'Register Kernel Module')

while True:
    msg = recv_msg()
    
    if msg is not False:
        cmd = msg['cmd'].upper()
        src = msg['src']
        dst = msg['dst']
        mesage = msg['msg']
        date = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
        
        write_log(f'[{cmd}]({date}) source:{src} destination:{dst} message:{mesage}')
        
        if msg['cmd'] == 'create':
            create_file(msg['msg'])
        
        if msg['cmd'] == 'delete':
            delete_file(msg['msg'])
        
        if msg['cmd'] == 'stop':
            files_socket.close()
            sys.exit()
            
