import flet as ft

def favoritos_view(page: ft.Page, db, user):
    page.title = "Mis favoritos"
    page.clean()

    # Simulación de favoritos (puedes dejar la lista vacía para probar el mensaje)
    favoritos = []  # Ejemplo: [{"id": 1, "titulo": "1984", "autor": "George Orwell", "anio": 1949, "genero": "Ciencia ficción"}]

    def agregar_favorito(e):
        print("Agregar libro a favoritos")  # Aquí va la lógica real

    btn_agregar = ft.ElevatedButton("Agregar a favoritos", icon="add", on_click=agregar_favorito)

    contenido = []

    if not favoritos:
        contenido.append(
            ft.Container(
                ft.Text("Todavía no hay libros agregados a favoritos.", size=20, weight="bold", color="grey"),
                alignment=ft.alignment.center,
                padding=20,
                bgcolor="#f5f5f5",
                border_radius=10,
                margin=20
            )
        )
    else:
        columns = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Título")),
            ft.DataColumn(ft.Text("Autor")),
            ft.DataColumn(ft.Text("Año")),
            ft.DataColumn(ft.Text("Género")),
            ft.DataColumn(ft.Text("Acciones")),
        ]

        rows = []
        for libro in favoritos:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(libro.get("id", "")))),
                        ft.DataCell(ft.Text(libro.get("titulo", ""))),
                        ft.DataCell(ft.Text(libro.get("autor", ""))),
                        ft.DataCell(ft.Text(str(libro.get("anio", "")))),
                        ft.DataCell(ft.Text(libro.get("genero", ""))),
                        ft.DataCell(
                            ft.IconButton("delete", tooltip="Eliminar de favoritos", on_click=lambda e, l=libro: print(f"Eliminar favorito {l['id']}"))
                        ),
                    ]
                )
            )

        contenido.append(
            ft.DataTable(columns=columns, rows=rows)
        )

    page.add(
        ft.Column([
            ft.Text("📚 Mis libros favoritos", size=28, weight="bold", color="#1976d2"),
            btn_agregar,
            *contenido
        ], alignment="center", horizontal_alignment="center")
    )
    page.update()