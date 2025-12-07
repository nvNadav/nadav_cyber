import tkinter as tk
import UserDatabase
from tkinter import messagebox


class GUI:
    def __init__(self):
        self.db = UserDatabase.UserDatabase()

        self.root = tk.Tk()
        self.root.title("Login / Signup Window")
        self.root.geometry("300x200")
        self.root.configure(bg="lightblue")

        # Username label + entry
        tk.Label(self.root, text="Username:", bg="lightblue").pack(pady=5)
        self.username_entry = tk.Entry(self.root, width=25)
        self.username_entry.pack()

        # Password label + entry
        tk.Label(self.root, text="Password:", bg="lightblue").pack(pady=5)
        self.password_entry = tk.Entry(self.root, width=25, show="*")
        self.password_entry.pack()

        # Buttons
        tk.Button(self.root, text="Login", width=10, command=self.login).pack(pady=10)
        tk.Button(self.root, text="Create Account", width=15, command=self.open_signup_window).pack()


    def open_signup_window(self):
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Create Account")
        signup_window.geometry("300x250")
        signup_window.grab_set()  # make modal (block main window)
        signup_window.configure(bg="lightblue")

        # Entries
        tk.Label(signup_window, text="Username:",bg="lightblue").pack(pady=5)
        username_entry = tk.Entry(signup_window, width=25)
        username_entry.pack()

        tk.Label(signup_window, text="Password:",bg="lightblue").pack(pady=5)
        password_entry = tk.Entry(signup_window, width=25, show="*")
        password_entry.pack()

        tk.Label(signup_window, text="Confirm Password:",bg="lightblue").pack(pady=5)
        confirm_entry = tk.Entry(signup_window, width=25, show="*")
        confirm_entry.pack()

        tk.Button(signup_window, text="Sign Up", command=self.login).pack(pady=10)

        def create_user(self):
            username = username_entry.get()
            password = password_entry.get()
            confirm = confirm_entry.get()
            
            self.db.add_user()


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not self.db.check_user(username,password):
            messagebox.showerror("Login Error", "Incorrect username or password!")
        else:
            messagebox.showinfo("Login Success", "Successfully logged in")

if __name__=="__main__":
    gui=GUI()
    gui.root.mainloop()
