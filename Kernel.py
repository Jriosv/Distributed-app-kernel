from asyncio import subprocess
import socket
import threading
import os
import time
import select
import pickle
import subprocess


class Kernel:
    def __init__(self):
        #defines Kernel (server) IP and address
        self.IP_ADRESS = socket.gethostname()
        self.PORT = 1234
        
        #create the server socket
        self.kernel_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.kernel_socket.bind((self.IP_ADRESS, self.PORT))
        self.kernel_socket.listen(5)
        
        #list that contains the sockets we are going to select
        self.sockets_list = [self.kernel_socket]
        self.registered_sockets = {'kernel': self.kernel_socket}
        
        #Start kernel
        self.kernel_thread = threading.Thread(target= self.start_execution)
        self.kernel_thread.start()
        time.sleep(3)
        
        #Start gui
        self.gui_thread = threading.Thread(target= self.start_GUI_module)
        self.gui_thread.start()
    
    def recv_msg(self, client_socket):
        try:
            received_msg = client_socket.recv(1024)
            return pickle.loads(received_msg) 
        except:
            return False
    
    def send_msg(self,cmd,src,dst,msg,client_socket):
        msg = {'cmd':cmd,
           'src': src,
           'dst': dst,
           'msg' : msg
           }
        serialized_msg = pickle.dumps(msg)
        client_socket.send(serialized_msg)
    
    def register_socket(self, module_name,client_socket):
        if module_name in self.registered_sockets.keys():
            return False
        else:
            self.registered_sockets[module_name] = client_socket
            print(f'Socket registered: {module_name}')
        
            
    def start_execution(self):
        print(f'Server connected listening in {self.IP_ADRESS}:{self.PORT}')
        while True:
            read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
            
            for notified_socket in read_sockets:
                
                if notified_socket == self.kernel_socket:
                    
                    clientsocket, address = self.kernel_socket.accept()
                    print(f'Connection from {address} has been established!')
                    
                    self.sockets_list.append(clientsocket)
                    
                    clientsocket.send(bytes("Welcome to the server!","utf-8"))   
                
                else:
                    
                    msg = self.recv_msg(notified_socket)
                    
                    if msg is False:
                        print(f'Closed connection from {notified_socket}')
                        self.sockets_list.remove(notified_socket)
                        continue
                    
                    if 'files' in self.registered_sockets.keys():
                        destination = self.registered_sockets['files']
                        self.send_msg(cmd=msg['cmd'],
                                      src=msg['src'],
                                      dst=msg['dst'],
                                      msg=msg['msg'],
                                      client_socket=destination)      
                    
                    if msg['cmd'] == 'register':
                        self.register_socket(module_name= msg['src'],
                                             client_socket= notified_socket)
                    
                    if msg['cmd'] == 'init':
                        if msg['dst'] == 'apps':
                            destination = self.registered_sockets['apps']
                            if 'app' in msg['msg']:
                                self.send_msg(cmd=msg['cmd'],
                                         src=msg['src'],
                                         dst=msg['dst'],
                                         msg=msg['msg'],
                                         client_socket=destination)
                        else:
                            self.initialize_modules()
                            destination = self.registered_sockets['gui']
                            self.send_msg(cmd='init',
                                     src='kernel',
                                     dst='gui',
                                     msg='init modules',
                                     client_socket=destination)
                        
                    
                    if msg['cmd'] == 'info':
                        if msg['dst'] == 'apps':
                            destination = self.registered_sockets['apps']
                            self.send_msg(cmd=msg['cmd'],
                                     src=msg['src'],
                                     dst=msg['dst'],
                                     msg=msg['msg'],
                                     client_socket=destination)
                                
                        if msg['dst'] == 'files':
                            destination = self.registered_sockets['files']
                    
                    if msg['cmd'] == 'close':
                        if msg['dst'] == 'apps':
                            destination = self.registered_sockets['apps']
                            if 'app' in msg['msg']:
                                self.send_msg(cmd=msg['cmd'],
                                         src=msg['src'],
                                         dst=msg['dst'],
                                         msg=msg['msg'],
                                         client_socket=destination)
                    
                    if msg['cmd'] == 'answer':
                        if msg['dst'] == 'gui':
                            destination = self.registered_sockets['gui']
                            self.send_msg(cmd=msg['cmd'],
                                          src=msg['src'],
                                          dst=msg['dst'],
                                          msg=msg['msg'],
                                          client_socket=destination)
                    

                        
                                                                     
    def start_app_module(self):
        os.system('python Apps.py')
    
    def start_GUI_module(self):
        os.system('python GUI.py')
    
    def start_files_module(self):
        os.system('python Files.py')
      
    def initialize_modules(self):
        app_thread = threading.Thread(target=self.start_app_module)
        files_thread = threading.Thread(target=self.start_files_module)
        app_thread.start()
        time.sleep(3)
        files_thread.start()
        time.sleep(3)

        



    
    