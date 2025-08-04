import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

def ventana_favoritos(db, user):
    win = tb.Toplevel()
    win.title("Mis Favoritos")
    win.geometry("700x400")
    win.resizable(True, True)

    frame = tb.Frame(win, padding=20)
    frame.pack(fill='both', expand=True)

    tb.Label(frame, text="Libros favoritos:", font=("Arial", 12)).pack(anchor='w')

    tree = tb.Treeview(frame, columns=("Título", "Autor", "Año", "Género"), show="headings")
    for col in ("Título", "Autor", "Año", "Género"):
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill='both', expand=True, pady=10)

    def cargar_favoritos():
        query = '''SELECT libros.titulo, libros.autor, libros.anio, libros.genero, favoritos.id as fav_id\n                   FROM favoritos\n                   JOIN libros ON favoritos.id_libro = libros.id\n                   WHERE favoritos.id_usuario = ?'''
        resultados = db.fetch_all(query, (user['id'],))
        tree.delete(*tree.get_children())
        for libro in resultados:
            tree.insert('', 'end', iid=libro['fav_id'], values=(libro['titulo'], libro['autor'], libro['anio'], libro['genero']))

    def eliminar_favorito():
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showinfo("Atención", "Seleccione un libro para eliminar de favoritos.")
            return
        fav_id = seleccionado[0]
        db.execute_query("DELETE FROM favoritos WHERE id = ?", (fav_id,))
        cargar_favoritos()
        messagebox.showinfo("Eliminado", "Libro eliminado de favoritos.")

    btn = tb.Button(frame, text="Eliminar de favoritos", command=eliminar_favorito, bootstyle=DANGER)
    btn.pack(anchor='w', pady=5)

    cargar_favoritos()
