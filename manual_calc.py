from tkinter import *
import tkinter
import sys

def calculator_display():
    global result
    calculator = Tk()
    calculator.title("Our own program")
    calculator.geometry('400x300+0+200')
    calculator.resizable(True, True)
    calculator.configure(bg='#C3C0C0')

    text_result = StringVar()
    result = Entry(calculator,justify=tkinter.CENTER,state="readonly",font=('arial',20,'bold'),width=20,borderwidth=10,textvariable=text_result)
    result.place(x=0,y=200)

    dividendo_label = Label(calculator, relief="solid",font=('arial',16,'bold'),text="Dividendo:",bg='#91A6D8',borderwidth=4)
    dividendo_label.place(x=80,y=50)
    dividendo = Entry(calculator,font=('arial',15),justify=tkinter.LEFT,width=10)
    dividendo.place(x=200,y=50)

    divisor_label = Label(calculator, relief="solid",font=('arial',16,'bold'),text="Divisor:     ",bg='#91A6D8',borderwidth=4)
    divisor_label.place(x=80,y=90)
    divisor = Entry(calculator,font=('arial',15),justify=tkinter.LEFT,width=10)
    divisor.place(x=200,y=95)

    operation_button = Button(calculator,text="Dividir",width=10,height=2,command =lambda:operation((int(dividendo.get())),(int(divisor.get()))),bg='#576FDC',borderwidth=5)
    operation_button.place(x=290,y=150)
    calculator.mainloop()
    
def operation(dividendo,divisor):
    try:
        text_result = StringVar()
        text_result.set(dividendo/divisor)
        result.config(textvariable=text_result)
    except:
        sys.exit()
    
    
calculator_display()


    