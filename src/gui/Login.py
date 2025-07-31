import tkinter as tk
from tkinter import messagebox

def login_interfaz(db, on_login_success):
    def intentar_login():
        username = entry_user.get()
        password = entry_pass.get()
        user = db.fetch_one(
            "SELECT * FROM usuarios WHERE username=? AND password=?",
            (username, password)
        )
        if user:
            root.destroy()
            on_login_success(user)  # Llama a la función para la siguiente interfaz
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    root = tk.Tk()
    root.title("Login")

    tk.Label(root, text="Usuario:").grid(row=0, column=0, padx=10, pady=10)
    entry_user = tk.Entry(root)
    entry_user.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Contraseña:").grid(row=1, column=0, padx=10, pady=10)
    entry_pass = tk.Entry(root, show="*")
    entry_pass.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(root, text="Iniciar sesión", command=intentar_login).grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()