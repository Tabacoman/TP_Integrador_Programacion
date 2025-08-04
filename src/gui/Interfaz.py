import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from gui.BusquedaLibros import ventana_busqueda_libros
from gui.Favoritos import ventana_favoritos
from gui.ABMLibros import ventana_abm_libros

def main_interfaz(db, user):
    root = tb.Window(themename="flatly")
    root.title("Biblioteca - Menú Principal")
    root.geometry("400x420")
    root.resizable(False, False)
    frame = tb.Frame(root, padding=30)
    frame.pack(expand=True)
    tb.Label(frame, text=f"¡Bienvenido, {user['username']}!", font=("Segoe UI", 16, "bold")).pack(pady=(0,10))
    tb.Label(frame, text=f"Rol: {user['rol']}", font=("Segoe UI", 11)).pack(pady=(0,20))

    def salir():
        if messagebox.askokcancel("Salir", "¿Seguro que deseas salir?"):
            root.destroy()

    tb.Button(frame, text="🔍 Buscar libros", width=30, bootstyle=PRIMARY, command=lambda: ventana_busqueda_libros(db, user)).pack(pady=8)
    tb.Button(frame, text="📚 Mis favoritos", width=30, bootstyle=SUCCESS, command=lambda: ventana_favoritos(db, user)).pack(pady=8)
    if user.get('rol') == 'admin':
        tb.Button(frame, text="🛠️  Gestión de libros (ABM)", width=30, bootstyle=WARNING, command=lambda: ventana_abm_libros(db, user)).pack(pady=8)
    tb.Button(frame, text="🚪 Salir", width=30, bootstyle=DANGER, command=salir).pack(pady=(30,0))
    root.mainloop()

def ventana_abm_libros(db, user):
    win = tb.Toplevel()
    win.title("Gestión de Libros (ABM)")
    win.geometry("800x500")
    win.resizable(False, False)
    frame = tb.Frame(win, padding=20)
    frame.pack(fill='both', expand=True)
    tb.Label(frame, text="Libros en la biblioteca:", font=("Segoe UI", 13, "bold")).pack(anchor='w')
    tree = tb.Treeview(frame, columns=("ID", "Título", "Autor", "Año", "Género"), show="headings", height=10)
    for col in ("ID", "Título", "Autor", "Año", "Género"):
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill='x', pady=10)

    # Entradas
    form = tb.Frame(frame)
    form.pack(pady=10)
    labels = ["Título:", "Autor:", "Año:", "Género:"]
    entrys = []
    for l in labels:
        tb.Label(form, text=l).pack(anchor='w')
        e = tb.Entry(form, width=40)
        e.pack(anchor='w', pady=2)
        entrys.append(e)

    def cargar_libros():
        resultados = db.fetch_all("SELECT * FROM libros")
        tree.delete(*tree.get_children())
        for libro in resultados:
            tree.insert('', 'end', iid=libro['id'], values=(libro['id'], libro['titulo'], libro['autor'], libro['anio'], libro['genero']))

    def agregar_libro():
        datos = [e.get().strip() for e in entrys]
        if not all(datos):
            messagebox.showwarning("Campos vacíos", "Complete todos los campos.")
            return
        try:
            int(datos[2])
        except ValueError:
            messagebox.showwarning("Año inválido", "El año debe ser un número.")
            return
        db.execute_query("INSERT INTO libros (titulo, autor, anio, genero) VALUES (?, ?, ?, ?)", tuple(datos))
        cargar_libros()
        for e in entrys: e.delete(0, 'end')
        messagebox.showinfo("Éxito", "Libro agregado.")

    def eliminar_libro():
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showinfo("Atención", "Seleccione un libro para eliminar.")
            return
        libro_id = seleccionado[0]
        db.execute_query("DELETE FROM libros WHERE id = ?", (libro_id,))
        cargar_libros()
        messagebox.showinfo("Eliminado", "Libro eliminado.")

    def modificar_libro():
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showinfo("Atención", "Seleccione un libro para modificar.")
            return
        libro_id = seleccionado[0]
        datos = [e.get().strip() for e in entrys]
        if not all(datos):
            messagebox.showwarning("Campos vacíos", "Complete todos los campos.")
            return
        try:
            int(datos[2])
        except ValueError:
            messagebox.showwarning("Año inválido", "El año debe ser un número.")
            return
        db.execute_query("UPDATE libros SET titulo=?, autor=?, anio=?, genero=? WHERE id=?", (*datos, libro_id))
        cargar_libros()
        messagebox.showinfo("Modificado", "Libro modificado.")

    btns = tb.Frame(frame)
    btns.pack(pady=10)
    tb.Button(btns, text="➕ Agregar", command=agregar_libro, bootstyle=SUCCESS).pack(side='left', padx=5)
    tb.Button(btns, text="✏️ Modificar", command=modificar_libro, bootstyle=WARNING).pack(side='left', padx=5)
    tb.Button(btns, text="🗑️ Eliminar", command=eliminar_libro, bootstyle=DANGER).pack(side='left', padx=5)
    cargar_libros()

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
            btn_toggle_pass.config(text='Mostrar 👁️')
        else:
            entry_pass.config(show='')
            btn_toggle_pass.config(text='Ocultar 👁️')

    root = tb.Window(themename="flatly")
    root.title("Login Biblioteca")
    root.geometry("350x300")
    root.resizable(False, False)
    frame = tb.Frame(root, padding=30)
    frame.pack(expand=True)

    tb.Label(frame, text="Bienvenido a la Biblioteca", font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))
    tb.Label(frame, text="Usuario:").pack(anchor='w')
    entry_user = tb.Entry(frame)
    entry_user.pack(fill='x', pady=5)
    tb.Label(frame, text="Contraseña:").pack(anchor='w')
    entry_pass = tb.Entry(frame, show="*")
    entry_pass.pack(fill='x', pady=5)
    btn_toggle_pass = tb.Button(frame, text="Mostrar 👁️", command=toggle_password, bootstyle=SECONDARY)
    btn_toggle_pass.pack(pady=5)
    btn_login = tb.Button(frame, text="Iniciar sesión ✅", width=20, command=intentar_login, bootstyle=SUCCESS)
    btn_login.pack(pady=15)
    root.bind('<Return>', lambda event: intentar_login())
    root.mainloop()