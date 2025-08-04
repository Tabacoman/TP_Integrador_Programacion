import ttkbootstrap as tb
from tkinter import messagebox

def ventana_busqueda_libros(db, user):
    win = tb.Toplevel()
    win.title("Buscar libros")
    win.geometry("700x400")
    win.resizable(False, False)
    frame = tb.Frame(win, padding=30)
    frame.pack(fill='both', expand=True)

    tb.Label(frame, text="Buscar por título, autor o género:", font=("Segoe UI", 13, "bold")).pack(anchor='w', pady=(0,10))
    search_row = tb.Frame(frame)
    search_row.pack(fill='x', pady=5)
    entry = tb.Entry(search_row, width=40, font=("Segoe UI", 12))
    entry.pack(side='left', padx=(0,10))
    btn = tb.Button(search_row, text="🔎 Buscar", bootstyle="primary", command=lambda: buscar())
    btn.pack(side='left')

    tree = tb.Treeview(frame, columns=("Título", "Autor", "Año", "Género"), show="headings", height=10)
    for col in ("Título", "Autor", "Año", "Género"):
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill='x', pady=15)

    def buscar():
        criterio = entry.get().strip()
        if not criterio:
            messagebox.showinfo("Atención", "Ingrese un criterio de búsqueda.")
            return
        query = """SELECT titulo, autor, anio, genero FROM libros
                  WHERE titulo LIKE ? OR autor LIKE ? OR genero LIKE ?"""
        resultados = db.fetch_all(query, (f'%{criterio}%', f'%{criterio}%', f'%{criterio}%'))
        tree.delete(*tree.get_children())
        for libro in resultados:
            tree.insert('', 'end', values=(libro['titulo'], libro['autor'], libro['anio'], libro['genero']))
