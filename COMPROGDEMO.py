from tkinter import *
import tkinter.messagebox as MessageBox
import pandas as pd

def submit_fields():
    df1 = pd.read_excel(path)
    SeriesA = df1['SRCODE']
    SeriesB = df1['NAME']
    SeriesC = df1['PASSWORD']
    A = pd.Series(e_txtsource.get())
    B = pd.Series(e_txtusername.get())
    C = pd.Series(e_txtpassword.get())
    SeriesA = SeriesA.append(A)
    SeriesB = SeriesB.append(B)
    SeriesC = SeriesC.append(C)
    df2 = pd.DataFrame({"SRCODE":SeriesA, "NAME":SeriesB, "PASSWORD":SeriesC})
    df2.to_excel(path, index=False)
    e_txtsource.delete(0, END)
    e_txtusername.delete(0, END)
    e_txtpassword.delete(0, END)
     
def login():
    database = pd.read_excel(path)
    
    # get ng isang data
    print(database['SRCODE'])
   

            
master = Tk()
master.title('Welcome to Batangas State University Fund Tracker!')
master.geometry("300x350")

path = "C:/Users/jsmiayo/Desktop/Python/"

Label(master, text="SRCODE").grid(row=0)
Label(master, text="NAME").grid(row=1)
Label(master, text="PASSWORD").grid(row=2)


e_txtsource = Entry(master)
e_txtusername = Entry(master)
e_txtpassword = Entry(master)

e_txtsource.grid(row=0, column=1)
e_txtusername.grid(row=1, column=1)
e_txtpassword.grid(row=2, column=1)

Button(master, text='Quit', command=master.quit).grid(row=4, column=0, pady=4)
Button(master, text='SignUp', command=submit_fields).grid(row=4, column=1, pady=4)
Button(master, text='Login', command=login).grid(row=4, column=2, pady=4)

mainloop()