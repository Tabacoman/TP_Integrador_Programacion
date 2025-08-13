import flet as ft
from Utilities.funtions import get_libros

def abm_libros_view(page: ft.Page, db):
    page.title = "Gestión de Libros (ABM)"
    page.clean()

    # Obtener los libros
    libros = get_libros(db)

    # Botón para agregar libro
    btn_agregar = ft.ElevatedButton("Agregar libro", icon="add", on_click=lambda e: print("Agregar libro"))

    # Definir columnas de la tabla
    columns = [
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Título")),
        ft.DataColumn(ft.Text("Autor")),
        ft.DataColumn(ft.Text("Año")),
        ft.DataColumn(ft.Text("Género")),
        ft.DataColumn(ft.Text("Acciones")),
    ]

    # Definir filas con botones de editar y eliminar
    rows = []
    for libro in libros:
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(libro.get("id", "")))),
                    ft.DataCell(ft.Text(libro.get("titulo", ""))),
                    ft.DataCell(ft.Text(libro.get("autor", ""))),
                    ft.DataCell(ft.Text(str(libro.get("anio", "")))),
                    ft.DataCell(ft.Text(libro.get("genero", ""))),
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton("edit", tooltip="Editar", on_click=lambda e, l=libro: print(f"Editar {l['id']}")),
                            ft.IconButton("delete", tooltip="Eliminar", on_click=lambda e, l=libro: print(f"Eliminar {l['id']}"))
                        ])
                    ),
                ]
            )
        )

    page.add(
        ft.Column([
            ft.Text("📚 Gestión de Libros", size=24, weight="bold"),
            btn_agregar,
            ft.DataTable(columns=columns, rows=rows)
        ], alignment="center", horizontal_alignment="center")
    )
    page.update()