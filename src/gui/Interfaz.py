import tkinter as tk

def main_interfaz(db, user):
    root = tk.Tk()
    root.title("Interfaz Principal")

    tk.Label(root, text=f"¡Bienvenido, {user['username']}!", font=("Arial", 16)).pack(padx=20, pady=20)
    tk.Label(root, text=f"Rol: {user['rol']}").pack(pady=10)

    tk.Button(root, text="Salir", command=root.destroy).pack(pady=20)

    root.mainloop()