import flet as ft
from Utilities.funtions import buscar_libros, eliminar_favorito, get_favoritos, agregar_favorito

def favoritos_view(page: ft.Page, db, user, volver_al_menu=None):
    page.title = "Mis favoritos"
    page.clean()

    # Estado de búsqueda
    search_input = ft.TextField(label="Buscar en favoritos", expand=True)
    search_button = ft.IconButton(icon="search", tooltip="Buscar")

    # pedir favoritos del usuario
    favoritos = get_favoritos(db, user["id"]) or []

    # Filtro de búsqueda
    def cargar_favoritos(filtro=""):
        filtro = filtro.strip().lower()
        if filtro:
            filtrados = [
                libro for libro in favoritos
                if filtro in libro["titulo"].lower()
                or filtro in libro["autor"].lower()
                or filtro in libro["genero"].lower()
                or filtro in str(libro["anio"])
            ]
        else:
            filtrados = favoritos

        contenido = []

        if not filtrados:
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
            for libro in filtrados:
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(libro["id"]))),
                            ft.DataCell(ft.Text(libro["titulo"])),
                            ft.DataCell(ft.Text(libro["autor"])),
                            ft.DataCell(ft.Text(str(libro["anio"]))),
                            ft.DataCell(ft.Text(libro["genero"])),
                            ft.DataCell(
                                ft.IconButton(
                                    icon="delete",
                                    tooltip="Eliminar de favoritos",
                                    on_click=lambda e, l_id=libro["id"]: eliminar_fav(e, l_id)
                                )
                            ),
                        ]
                    )
                )

            contenido.append(
                ft.DataTable(columns=columns, rows=rows)
            )
        
        # Actualiza el contenido de la página
        main_column.controls[3:] = contenido
        page.update()

    def on_buscar(e=None):
        cargar_favoritos(search_input.value)

    def eliminar_fav(e, id_libro):
        if eliminar_favorito(db, user["id"], id_libro):
            page.snack_bar = ft.SnackBar(ft.Text("Libro eliminado de favoritos."), bgcolor="green")
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Error al eliminar favorito."), bgcolor="red")
        page.snack_bar.open = True
        # Recargar favoritos y resultados
        nonlocal favoritos
        favoritos = get_favoritos(db, user["id"]) or []
        cargar_favoritos(search_input.value)

    # Barra superior con input y lupa
    barra_busqueda = ft.Row([
        search_input,
        search_button
    ], alignment="center", vertical_alignment="center", spacing=10)

    search_input.on_submit = on_buscar
    search_button.on_click = on_buscar

    # Botón volver (siempre presente)
    btn_volver = ft.ElevatedButton(
        "Volver",
        icon="arrow_back",
        on_click=lambda e: volver_al_menu()
    )

    # Layout principal
    main_column = ft.Column([
        ft.Text("📚 Mis libros favoritos", size=28, weight="bold", color="#1976d2"),
        barra_busqueda,
        btn_volver  # Siempre se agrega el botón de volver
    ], alignment="center", horizontal_alignment="center")

    page.add(main_column)
    cargar_favoritos()
    page.update()