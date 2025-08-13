

import flet as ft
from db.Querys import QUERY_SELECT_ALL_BOOKS

def buscador_libro_view(page: ft.Page, db, user=None):
        page.title = "Buscar libro"
        page.clean()

        libros = db.fetch_all(QUERY_SELECT_ALL_BOOKS)

        columns = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Título")),
            ft.DataColumn(ft.Text("Autor")),
            ft.DataColumn(ft.Text("Año")),
            ft.DataColumn(ft.Text("Género")),
        ]

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
                    ]
                )
            )

        def volver(e):
            from flet_components.interfaz_flet import main_menu
            main_menu(page, db, user)

        # Botón arriba a la derecha
        boton_volver = ft.Row(
            [
                ft.Container(
                    ft.ElevatedButton("Volver", on_click=volver),
                    alignment=ft.alignment.top_right
                )
            ],
            alignment="end"
        )

        # Contenido centrado
        contenido = ft.Column(
            [
                ft.Text("📚 Aquí están todos los libros disponibles", size=24, weight="bold"),
                ft.DataTable(columns=columns, rows=rows)
            ],
            alignment="center",
            horizontal_alignment="center"
        )

        page.add(
            ft.Column(
                [
                    boton_volver,
                    contenido
                ]
            )
        )
        page.update()