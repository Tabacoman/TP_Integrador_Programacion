from Utilities.funtions import eliminar_favorito, get_favoritos
from models.Libro import Libro
import flet as ft

def favoritos_view(page: ft.Page, db, user, volver_al_menu):
    page.title = "Mis favoritos"
    page.clean()

    search_input = ft.TextField(label="Buscar en favoritos", expand=True)
    search_button = ft.IconButton(icon="search", tooltip="Buscar")

    def eliminar_fav(e, libro: Libro):
        try:
            if eliminar_favorito(db, user, libro):
                page.open(ft.SnackBar(ft.Text(f"Libro '{libro.titulo}' eliminado de favoritos."), bgcolor="green"))
            else:
                page.open(ft.SnackBar(ft.Text("Error al eliminar favorito."), bgcolor="red"))
        except Exception as err:
            page.open(ft.SnackBar(ft.Text(f"Error al eliminar favorito: {err}"), bgcolor="red"))

        # recargar la lista con el texto actual del buscador
        cargar_favoritos(search_input.value)
        page.update()

    def cargar_favoritos(filtro: str = ""):
        filtro = (filtro or "").strip().lower()
        todos_favoritos = get_favoritos(db, user) or []

        if filtro:
            favoritos_filtrados = [
                libro for libro in todos_favoritos
                if (libro.titulo and filtro in libro.titulo.lower())
                or (libro.autor and filtro in libro.autor.lower())
                or (libro.genero and filtro in libro.genero.lower())
                or (libro.anio and filtro in str(libro.anio))
            ]
        else:
            favoritos_filtrados = todos_favoritos

        contenido = []

        if not favoritos_filtrados:
            # cartel cuando no hay favoritos
            contenido.append(
                ft.Container(
                    ft.Text("Todavía no hay libros agregados a favoritos.",
                            size=20,
                            weight="bold",
                            color="grey"),
                    alignment=ft.alignment.center,
                    padding=20,
                    bgcolor="#f5f5f5",
                    border_radius=10,
                    margin=20
                )
            )
        else:
            for libro in favoritos_filtrados:
                contenido.append(
                    ft.Container(
                        ft.Row([
                            ft.Column([
                                ft.Text(f"Título: {libro.titulo}", size=18, weight="bold"),
                                ft.Text(f"Autor: {libro.autor}"),
                                ft.Text(f"Año: {libro.anio}"),
                                ft.Text(f"Género: {libro.genero}"),
                            ], expand=True),
                            ft.IconButton(
                                icon="delete",
                                tooltip="Eliminar de favoritos",
                                on_click=lambda e, l=libro: eliminar_fav(e, l),
                                icon_color="#e53e3e"
                            )
                        ], alignment="spaceBetween"),
                        padding=10,
                        margin=ft.margin.symmetric(vertical=8, horizontal=0),
                        bgcolor="#f4f4f4",
                        border_radius=12,
                        shadow=ft.BoxShadow(blur_radius=4, color="#00000022", offset=ft.Offset(0, 2))
                    )
                )

        # siempre creamos un Column, con libros o con el cartel
        libros_scroll = ft.Column(
            contenido,
            expand=True,
            scroll="auto",
            alignment="center",
            horizontal_alignment="center",
            spacing=10
        )

        # reemplazamos el contenido desde la posición 2
        main_column.controls[2:] = [libros_scroll, btn_volver]
        page.update()

    def on_buscar(e=None):
        cargar_favoritos(search_input.value)

    barra_busqueda = ft.Row(
        [search_input, search_button],
        alignment="center",
        vertical_alignment="center",
        spacing=10
    )

    search_input.on_submit = on_buscar
    search_button.on_click = on_buscar

    main_column = ft.Column([
        ft.Text(" Mis libros favoritos",
                size=28,
                weight="bold",
                color="#2d3e50",
                font_family="Georgia",
                text_align="center"),
        barra_busqueda,
    ], alignment="center", horizontal_alignment="center", expand=True, spacing=20)

    # 🔹 ahora definimos btn_volver después de main_column
    btn_volver = ft.ElevatedButton(
        "Volver",
        icon="arrow_back",
        on_click=lambda e: volver_al_menu()
    )

    main_content = ft.Container(
        content=main_column,
        bgcolor="#faf9e3",
        border_radius=30,
        padding=40,
        expand=True,
        alignment=ft.alignment.center,
        height=600
    )

    page.add(
        ft.Column([main_content],
                  expand=True,
                  alignment="center",
                  horizontal_alignment="center")
    )

    # primera carga
    cargar_favoritos()
    page.update()
