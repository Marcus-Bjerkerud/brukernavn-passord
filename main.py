import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import csv
import sys

# koble til en sql database
conn = sqlite3.connect('KundeDatabase.db')
cursor = conn.cursor()

# Lag en bruker tabell hvis den ikke eksisterer
cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, role TEXT)")

# Importer brukere fra csv fil
with open('KundeDatabase.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        username, password = row[0], hashlib.sha256(row[1].encode()).hexdigest()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user is None:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, 'user'))

# Funksjon for å slette brukere
def delete_user(username):
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    messagebox.showinfo("Success", "User deleted successfully")

# Funksjon for å logge inn på brukere
def login():
    username = entry_username.get()
    password = hashlib.sha256(entry_password.get().encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    if user is None:
        messagebox.showerror("Error", "Invalid username or password")
    else:
        messagebox.showinfo("Success", "Logged in successfully")

# Funksjon for å lage brukere
def create_user():
    username = entry_username.get()
    password = hashlib.sha256(entry_password.get().encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user is not None:
        messagebox.showerror("Error", "User already exists")
    else:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, 'user'))
        conn.commit()
        messagebox.showinfo("Success", "User created successfully")

root = tk.Tk()
root.title("User Management")

tk.Label(root, text="Username:").grid(row=0, column=0, sticky="e")
tk.Label(root, text="Password:").grid(row=1, column=0, sticky="e")
tk.Label(root, text="Delete User:").grid(row=2, column=0, sticky="e")

entry_username = tk.Entry(root)
entry_password = tk.Entry(root, show="*")
entry_delete_username = tk.Entry(root)
entry_username.grid(row=0, column=1)
entry_password.grid(row=1, column=1)
entry_delete_username.grid(row=2, column=1)

button_login = tk.Button(root, text="Login", command=login)
button_create = tk.Button(root, text="Create user", command=create_user)
button_delete = tk.Button(root, text="Delete user", command=lambda: delete_user(entry_delete_username.get()))
button_login.grid(row=3, column=0, columnspan=2)
button_create.grid(row=4, column=0, columnspan=2)
button_delete.grid(row=5, column=0, columnspan=2)

root.mainloop()

conn.close()
