from tkinter import Tk, ttk, StringVar, N, E, S, W, messagebox
from pandas import read_excel, DataFrame

class User:
    """
    A class to represent user data from a row in excel DataFrame
    """    
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password

class Excel:
    """
    A class to abstract interactions to the excel file as database.
    File: database.xlsx
    Column Name for usernames: NAME
    Column Name for passwords: PASSWORD
    """
    def __init__(self, filepath='database.xlsx'):
        self.db = read_excel(filepath)
        self.filepath = filepath
        self.USERNAME_COL = 'NAME'
        self.PASSWORD_COL = 'PASSWORD'

    def get_user(self, username):
        # Get the row with USERNAME column that matches the given username
        # This will be None if the username does not exist in the USERNAME column
        user = self.db.loc[self.db[self.USERNAME_COL] == username]

        if user.empty:
            return None

        # DataFrame.iat[0, 1] was used to retrieve the actual password value from the DataFrame row
        return User(username, user.iat[0, 1])

    """
    This creates a DataFrame with single row containing the username and password
    then appends that DataFrame to the current db.
    Write the updated db to the excel file.
    """
    def register_user(self, username, password):
        row = { self.USERNAME_COL: username, self.PASSWORD_COL: password }
        # ignore_index=True allows the use of a dict instead of DataFrame
        self.db = self.db.append(row, ignore_index=True)
        # index=False removes the unnecessary Unnamed column that pandas adds by default.
        self.db.to_excel(self.filepath, index=False)


class Application:
    """
    A class to represent the application widget
    @param root Tk
    @param db Excel
    """
    def __init__(self, root, db):

        self.db = db
        self.root = root
        self.root.title('Login Widget')

        # UI configuration steps
        self.mainframe = ttk.Frame(self.root, padding='3 3 12 12')
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
       
        # username field
        self.username = StringVar()
        ttk.Label(self.mainframe, text='Username').grid(column=1, row=1, sticky=(W))
        username_field = ttk.Entry(self.mainframe, width=20, textvariable=self.username)
        username_field.grid(column=2, row=1, sticky=(W, E))

        # password field
        self.password = StringVar()
        ttk.Label(self.mainframe, text='Password').grid(column=1, row=2, sticky=(W))
        password_field = ttk.Entry(self.mainframe, width=20, textvariable=self.password, show='*')
        password_field.grid(column=2, row=2, sticky=(W, E))

        # action buttons
        ttk.Button(self.mainframe, text='Sign Up', command=self.register).grid(column=1, row=3, sticky=(W))
        ttk.Button(self.mainframe, text='Login', command=self.login).grid(column=2, row=3, sticky=(E))

        # add padding to child widgets
        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        # focus the username field on widget load
        username_field.focus()

        # bind some useful keyboard events
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
