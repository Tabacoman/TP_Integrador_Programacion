import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

def ventana_abm_libros(db, user):
    win = tb.Toplevel()
    win.title("Gestión de Libros (ABM)")
    win.geometry("800x450")
    win.resizable(True, True)

    frame = tb.Frame(win, padding=20)
    frame.pack(fill='both', expand=True)

    tb.Label(frame, text="Libros en la biblioteca:", font=("Arial", 12)).pack(anchor='w')

    tree = tb.Treeview(frame, columns=("ID", "Título", "Autor", "Año", "Género"), show="headings")
    for col in ("ID", "Título", "Autor", "Año", "Género"):
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill='both', expand=True, pady=10)

    # Entradas para ABM
    entrys = {}
    for idx, campo in enumerate(["Título", "Autor", "Año", "Género"]):
        tb.Label(frame, text=campo+":").pack(anchor='w')
        entrys[campo] = tb.Entry(frame, width=40)
        entrys[campo].pack(anchor='w', pady=2)

    def cargar_libros():
        resultados = db.fetch_all("SELECT * FROM libros")
        tree.delete(*tree.get_children())
        for libro in resultados:
            tree.insert('', 'end', iid=libro['id'], values=(libro['id'], libro['titulo'], libro['autor'], libro['anio'], libro['genero']))

    def agregar_libro():
        datos = [entrys[c].get().strip() for c in ["Título", "Autor", "Año", "Género"]]
        if not all(datos):
            messagebox.showwarning("Campos vacíos", "Complete todos los campos.")
            return
        try:
            anio = int(datos[2])
        except ValueError:
            messagebox.showwarning("Año inválido", "El año debe ser un número.")
            return
        db.execute_query("INSERT INTO libros (titulo, autor, anio, genero) VALUES (?, ?, ?, ?)", tuple(datos))
        cargar_libros()
        for e in entrys.values(): e.delete(0, 'end')
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
        datos = [entrys[c].get().strip() for c in ["Título", "Autor", "Año", "Género"]]
        if not all(datos):
            messagebox.showwarning("Campos vacíos", "Complete todos los campos.")
            return
        try:
            anio = int(datos[2])
        except ValueError:
            messagebox.showwarning("Año inválido", "El año debe ser un número.")
            return
        db.execute_query("UPDATE libros SET titulo=?, autor=?, anio=?, genero=? WHERE id=?", (*datos, libro_id))
        cargar_libros()
        messagebox.showinfo("Modificado", "Libro modificado.")

    btns = tb.Frame(frame)
    btns.pack(anchor='w', pady=10)
    tb.Button(btns, text="Agregar", command=agregar_libro, bootstyle=SUCCESS).pack(side='left', padx=5)
    tb.Button(btns, text="Modificar", command=modificar_libro, bootstyle=WARNING).pack(side='left', padx=5)
    tb.Button(btns, text="Eliminar", command=eliminar_libro, bootstyle=DANGER).pack(side='left', padx=5)

    cargar_libros()
