import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

def login_interfaz(db, on_login_success):
    def intentar_login():
        username = entry_user.get().strip()
        password = entry_pass.get().strip()
        if not username or not password:
            messagebox.showwarning("Campos vacíos", "Por favor, complete ambos campos.")
            return
        user = db.fetch_one(
            "SELECT * FROM usuarios WHERE username=? AND password=?",
            (username, password)
        )
        if user:
            root.destroy()
            on_login_success(user)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def toggle_password():
        if entry_pass.cget('show') == '':
            entry_pass.config(show='*')
            btn_toggle_pass.config(text='Mostrar')
        else:
            entry_pass.config(show='')
            btn_toggle_pass.config(text='Ocultar')


    # Paleta personalizada
    COLOR_BG = "#BECCF7"
    COLOR_FRAME = "#C3BEF8"
    COLOR_BTN = "#B3ACF7"
    COLOR_BTN2 = "#D6BEF7"

    root = tb.Window(themename="superhero")
    root.title("Login Biblioteca")
    root.geometry("350x230")
    root.minsize(300, 200)
    root.resizable(True, True)
    root.configure(bg=COLOR_BG)

    frame = tb.Frame(root, padding=20, style="Custom.TFrame")
    frame.pack(fill='both', expand=True)
    style = tb.Style()
    style.configure("Custom.TFrame", background=COLOR_FRAME)
    style.configure("Custom.TButton", background=COLOR_BTN, foreground="#222", font=("Segoe UI", 11, "bold"))

    tb.Label(frame, text="Bienvenido a la Biblioteca", font=("Segoe UI", 16, "bold"), background=COLOR_FRAME, foreground="#222").grid(row=0, column=0, columnspan=3, pady=(0, 15))
    tb.Label(frame, text="Usuario:", background=COLOR_FRAME).grid(row=1, column=0, sticky="e", pady=5)
    entry_user = tb.Entry(frame)
    entry_user.grid(row=1, column=1, columnspan=2, pady=5)

    tb.Label(frame, text="Contraseña:", background=COLOR_FRAME).grid(row=2, column=0, sticky="e", pady=5)
    entry_pass = tb.Entry(frame, show="*")
    entry_pass.grid(row=2, column=1, pady=5)
    btn_toggle_pass = tb.Button(frame, text="Mostrar", width=8, command=toggle_password, style="Custom.TButton")
    btn_toggle_pass.grid(row=2, column=2, padx=(5,0))

    btn_login = tb.Button(frame, text="Iniciar sesión", width=25, command=intentar_login, style="Custom.TButton")
    btn_login.grid(row=3, column=0, columnspan=3, pady=15)

    root.bind('<Return>', lambda event: intentar_login())
    root.mainloop()