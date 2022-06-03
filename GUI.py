import socket
from tkinter import *
from tkinter import messagebox as mb
from tkinter.simpledialog import askstring
import tkinter
import pickle
import threading


gui_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
gui_socket.connect((socket.gethostname(),1234))

msg = gui_socket.recv(1024)
print(msg.decode('utf-8') + ' GUI')


def recv_msg():
    try:
        received_msg = gui_socket.recv(1024)
        return pickle.loads(received_msg) 
    except:
        return False

def send_msg(cmd,src,dst,msg):
    msg = {'cmd':cmd,
           'src':src,
           'dst':dst,
           'msg' : msg
           }
    serialized_msg = pickle.dumps(msg)
    gui_socket.send(serialized_msg)

def init_app(app: str):
    send_msg(cmd='init',
             src='gui',
             dst='apps',
             msg=app)
        
        
def close_app(app: str):
    send_msg(cmd='close',
             src='gui',
             dst='apps',
             msg=app)

def popup(int):
    if int == 1:
        mb.showinfo("Modulos",'Los modulos se han iniciado')
    elif int == 2:
        mb.showinfo("Modulos",'Los modulos se han detenido')


def display():
    send_msg(cmd='info',
             src='gui',
             dst='kernel',
             msg='OK')
      
    #app configuration
    global app
    app = Tk()
    app.title("GUI")
    app.geometry('1000x700+180+0')
    app.resizable(True, True)
    app.configure(bg='#C3C0C0')
    
    init_button = Button(app,text="Inicializar",
                         width=10,
                         height=2,
                         command = lambda : send_msg(cmd='init',src='gui',dst='kernel',msg='LOG:[INFO] 5/19/2022 - 9:00 P.M -> Register modules'),
                         bg='#576FDC',
                         borderwidth=5)
    init_button.place(x=580,y=50)
    init_label = Label(relief="solid",font=('arial',16,'bold'),text="Inicializar los modulos",bg='#91A6D8',borderwidth=4)
    init_label.place(x=340,y=55)
    
    stop_button = Button(app,text="Detener",width=10,height=2,command =lambda : send_msg(cmd='stop',src='gui',dst='kernel',msg='stop modules'),bg='#576FDC',borderwidth=5)
    stop_button.place(x=580,y=100)
    stop_label = Label(relief="solid",font=('arial',16,'bold'),text="Detener los modulos  ",bg='#91A6D8',borderwidth=4)
    stop_label.place(x=340,y=105)
    
    apps_button = Button(app,text="Aplicaciones",width=20,height=6,command = apps_display ,bg = '#576FDC',borderwidth=5)
    apps_button.place(x=300,y=350)
    apps_button = Button(app,text="Archivos",width=20,height=6,command = files_display ,bg = '#576FDC',borderwidth=5)
    apps_button.place(x=500,y=350)
    
    app.mainloop()
    
#------------------------------------------------------------------------------------------------FILES MODULE--------------------------------------------------------------------

def handle_file(operation: str):
    name = askstring("nombre","Ingrese el nombre del archivo")
    send_msg(cmd=operation,
             src='gui',
             dst='files',
             msg=name)


def files_display():
    files = Toplevel()
    files.title("Gestor de archivos")
    files.geometry('600x500+760+0')
    files.configure(bg='#C3C0C0')

    create_label = Label(files, relief="solid",font=('arial',16,'bold'),text="Crear nuevo archivo",bg='#91A6D8',borderwidth=4)
    create_label.place(x=75,y=110)
    create_button = Button(files,text="Crear",width=10,height=2,command = lambda: handle_file('create') ,bg='#576FDC',borderwidth=5)
    create_button.place(x=290,y=100)

    delete_label = Label(files, relief="solid",font=('arial',16,'bold'),text="Borrar archivo          ",bg='#91A6D8',borderwidth=4)
    delete_label.place(x=75,y=160)
    delete_button = Button(files,text="Borrar",width=10,height=2,command = lambda: handle_file('delete') ,bg='#576FDC',borderwidth=5)
    delete_button.place(x=290,y=150)

    files.mainloop
    

#------------------------------------------------------------------------------------------------------------------APPS MODULE-------------------------------------
    
def switch():
    global is_on1
    if is_on1:
        state1_button.config(image = off) 
        close_app('app1')
        is_on1 = False
    else:
        init_app('app1')
        state1_button.config(image = on)
        is_on1 = True
        
def switch2():
    global is_on2
    if is_on2:
        state2_button.config(image = off)
        close_app('app2')
        is_on2 = False
    else:
        init_app('app2')
        state2_button.config(image = on)
        is_on2 = True

def switch3():
    global is_on3
    if is_on3:
        state3_button.config(image = off)
        close_app('app3')
        is_on3 = False
    else:
        init_app('app3')
        state3_button.config(image = on)
        is_on3 = True

def get_pid(pid_number: str):
    send_msg(cmd='info',
             src='gui',
             dst='apps',
             msg=pid_number)
    
def apps_display():
    global is_on1
    global is_on2
    global is_on3
    is_on1 = False
    is_on2 = False
    is_on3 = False
    
    global on
    global off
    global state1_button
    global state2_button
    global state3_button
    
    global status_text

    apps = Toplevel()
    apps.title("Aplicaciones")
    apps.geometry('600x500+0+0')
    apps.configure(bg='#C3C0C0')
    on = PhotoImage(file = "on.png")
    off = PhotoImage(file = "off.png")


    state1_button = Button(apps, image = off, bd = 0,command = switch)
    state1_button.place(x=410,y=100)
    application1_label = Label(apps, relief="solid",font=('arial',16,'bold'),text="Iniciar/suspender aplicación 1",bg='#91A6D8',borderwidth=4)
    application1_label.place(x=100,y=105)

    application2_label = Label(apps, relief="solid",font=('arial',16,'bold'),text="Iniciar/suspender aplicación 2",bg='#91A6D8',borderwidth=4)
    application2_label.place(x=100,y=155)
    state2_button = Button(apps, image = off, bd = 0,command = switch2)
    state2_button.place(x=410,y=150)

    application3_label = Label(apps, relief="solid",font=('arial',16,'bold'),text="Iniciar/suspender aplicación 3",bg='#91A6D8',borderwidth=4)
    application3_label.place(x=100,y=205)
    state3_button = Button(apps, image = off, bd = 0,command = switch3)
    state3_button.place(x=410,y=200)
    
    status_entry = Entry(apps,font=('arial',15),justify=tkinter.LEFT,width=20)
    status_entry.place(x=100,y=300)
    status_button = Button(apps,text="Estado",width=10,height=2,command = lambda: get_pid(int(status_entry.get())) ,bg='#576FDC',borderwidth=5)
    status_button.place(x=350,y=300)

    status_text = StringVar()
    status = Entry(apps,justify=tkinter.CENTER,state="readonly",font=('arial',20,'bold'),width=20,borderwidth=10,textvariable=status_text)
    status.place(x=100,y=350)
    
    apps.mainloop
    
#--------------------------------------------------------------------------------------------------------MAIN EXECUTION-------------------------------------------------------------------------
        
send_msg(cmd='register',
         src='gui',
         dst= 'kernel',
         msg= 'Register GUI Module')

main_gui = threading.Thread(target=display)
app_gui = threading.Thread(target=apps_display)
files_gui = threading.Thread(target=files_display)
main_gui.start()

while True: 
    msg = recv_msg()
    
    if msg is not False:
        if msg['cmd'] == 'init':
            app_gui.start()
            files_gui.start()
        
        if msg['cmd'] == 'answer':
            status_text.set(msg['msg'])
        
        if msg['cmd'] == 'stop':
            app_gui.kill()
            files_gui.kill()
            

 