from tkinter import Tk, ttk, StringVar, N, E, S, W, messagebox
from pandas import read_excel, DataFrame

class User:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password

class Excel:
    
    def __init__(self, filepath='database.xlsx'):
        self.db = read_excel(filepath)
        self.filepath = filepath
        self.USERNAME_COL = 'NAME'
        self.PASSWORD_COL = 'PASSWORD'

    def get_user(self, username):
        user = self.db.loc[self.db[self.USERNAME_COL] == username]

        if user.empty:
            return None
        
        return User(username, user.iat[0, 1])

    def register_user(self, username, password):
        self.db = self.db.append(
            DataFrame([[username, password]], columns=[self.USERNAME_COL, self.PASSWORD_COL]),
            ignore_index=True
        )
        self.db.to_excel(self.filepath)


class Application:

    def __init__(self, root, db):

        self.db = db
        self.root = root
        self.root.title('Login Widget')

        self.mainframe = ttk.Frame(self.root, padding='3 3 12 12')
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
       
        self.username = StringVar()
        ttk.Label(self.mainframe, text='Username').grid(column=1, row=1, sticky=(W))
        username_field = ttk.Entry(self.mainframe, width=20, textvariable=self.username)
        username_field.grid(column=2, row=1, sticky=(W, E))

        self.password = StringVar()
        ttk.Label(self.mainframe, text='Password').grid(column=1, row=2, sticky=(W))
        password_field = ttk.Entry(self.mainframe, width=20, textvariable=self.password, show='*')
        password_field.grid(column=2, row=2, sticky=(W, E))

        
        ttk.Button(self.mainframe, text='Sign Up', command=self.register).grid(column=1, row=3, sticky=(W))
        ttk.Button(self.mainframe, text='Login', command=self.login).grid(column=2, row=3, sticky=(E))


        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        username_field.focus()
        self.root.bind('<Return>', self.login)
        self.root.bind('<Escape>', exit)
        
    def register(self, *args):
        username = self.username.get()
        password = self.password.get()
        user = self.db.get_user(username)

        if user is not None:
            messagebox.showerror(title='Sign Up Error', message='User already exists.')
            return

        self.db.register_user(username, password)
        messagebox.showinfo(title='Sign Up Successful', message='User has been registered successfully.')

    def login(self, *args):
        username = self.username.get()
        user = self.db.get_user(username)

        if user is None:
            messagebox.showerror(title='Login Error', message='User not found. Please sign up first.')
            return

        if user.get_password() != self.password.get():
            messagebox.showerror(title='Login Error', message='Incorrect password. Please try again.')
            return

        messagebox.showinfo(title='Login Successful', message='You successfully logged in')

def main():
    root = Tk()
    db = Excel()
    Application(root, db)
    root.mainloop()

if __name__ == '__main__':
    main()
