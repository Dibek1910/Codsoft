import string
import random
from tkinter import *
from tkinter import messagebox
import sqlite3

class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.username_var = StringVar()
        self.password_len_var = IntVar()
        self.generated_password_var = StringVar()

        self.create_db_table()

        master.title('Password Generator')
        master.geometry('660x500')
        master.config(bg='#FF8000')
        master.resizable(False, False)

        self.create_widgets()

    def create_db_table(self):
        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS users(Username TEXT NOT NULL, GeneratedPassword TEXT NOT NULL);")
            db.commit()

    def create_widgets(self):
        Label(text=":PASSWORD GENERATOR:", anchor=N, fg='darkblue', bg='#FF8000', font='arial 20 bold underline').grid(row=0, column=1)

        for _ in range(3):  # Adding blank labels
            Label(text="").grid(row=_, column=0, columnspan=2)

        Label(text="Enter User Name: ", font='times 15 bold', bg='#FF8000', fg='darkblue').grid(row=4, column=0)
        Entry(textvariable=self.username_var, font='times 15', bd=6, relief='ridge').grid(row=4, column=1)

        Label(text="Enter Password Length: ", font='times 15 bold', bg='#FF8000', fg='darkblue').grid(row=6, column=0)
        Entry(textvariable=self.password_len_var, font='times 15', bd=6, relief='ridge').grid(row=6, column=1)

        generated_password_label = Label(text="Generated Password: ", font='times 15 bold', bg='#FF8000', fg='darkblue')
        generated_password_label.grid(row=8, column=0)

        Entry(textvariable=self.generated_password_var, font='times 15', bd=6, relief='ridge', fg='#DC143C').grid(row=8, column=1)

        for _ in range(3):  # Adding more blank labels
            Label(text="").grid(row=_, column=0)

        Button(text="GENERATE PASSWORD", bd=3, relief='solid', padx=1, pady=1, font='Verdana 15 bold', fg='#68228B', bg='#BCEE68', command=self.generate_password).grid(row=11, column=1)
        Button(text="ACCEPT", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#458B00', bg='#FFFAF0', command=self.accept_fields).grid(row=13, column=1)
        Button(text="RESET", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#458B00', bg='#FFFAF0', command=self.reset_fields).grid(row=15, column=1)

    def generate_password(self):
        upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower = "abcdefghijklmnopqrstuvwxyz"
        chars = "@#%&()\"?!"
        numbers = "1234567890"

        name = self.username_var.get()
        length = self.password_len_var.get()

        if name == "":
            messagebox.showerror("Error", "Name cannot be empty")
            return

        if not name.isalpha():
            messagebox.showerror("Error", "Name must be a string")
            self.username_var.set('')
            return

        if length < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            self.password_len_var.set(0)
            return

        u = random.randint(1, length - 3)
        l = random.randint(1, length - 2 - u)
        c = random.randint(1, length - 1 - u - l)
        n = length - u - l - c

        password = random.sample(upper, u) + random.sample(lower, l) + random.sample(chars, c) + random.sample(numbers, n)
        random.shuffle(password)
        gen_passwd = "".join(password)
        self.generated_password_var.set(gen_passwd)

    def accept_fields(self):
        username = self.username_var.get()
        generated_password = self.generated_password_var.get()

        if not username:
            messagebox.showerror("Error", "Username cannot be empty")
            return

        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            find_user = ("SELECT * FROM users WHERE Username = ?")
            cursor.execute(find_user, [(username)])

            if cursor.fetchall():
                messagebox.showerror("Error", "This username already exists! Please use another username.")
            else:
                insert_query = "INSERT INTO users(Username, GeneratedPassword) VALUES (?, ?)"
                cursor.execute(insert_query, (username, generated_password))
                db.commit()
                messagebox.showinfo("Success", "Password generated successfully")

    def reset_fields(self):
        self.username_var.set('')
        self.password_len_var.set(0)
        self.generated_password_var.set('')


if __name__ == '__main__':
    root = Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
