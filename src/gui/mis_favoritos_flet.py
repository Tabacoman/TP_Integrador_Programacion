from Utilities.funtions import eliminar_favorito, get_favoritos
from models.Libro import Libro
import flet as ft

def favoritos_view(page: ft.Page, db, user, volver_al_menu):
    page.title = "Mis favoritos"
    page.clean()

    search_input = ft.TextField(label="Buscar en favoritos", expand=True)
    search_button = ft.IconButton(icon="search", tooltip="Buscar")

    resultados = ft.Column([], expand=True, scroll="auto")

    favoritos = get_favoritos(db, user) if user else []
    favoritos_ids = {libro.id for libro in favoritos} if favoritos else set()

    def cargar_favoritos(filtro=""):
        filtro = filtro.strip().lower()
        if filtro:
            favoritos= [
                libro for libro in favoritos
                if filtro in libro.titulo.lower()
                or filtro in libro.autor.lower()
                or filtro in libro.genero.lower()
                or filtro in str(libro.anio)
            ]
        else:
            favoritos = get_favoritos(db, user) or []

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
            for libro in favoritos:
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
                                on_click=lambda e, l=libro: eliminar_fav(db, user, l),
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

        libros_scroll = ft.Column(
            contenido,
            expand=True,
            scroll="auto",
            alignment="center",
            horizontal_alignment="center",
            spacing=10
        )
        # Ahora pon el botón volver después del scroll
        main_column.controls[3:] = [libros_scroll, btn_volver]
        page.update()

    def on_buscar(e=None):
        cargar_favoritos(search_input.value)

    def eliminar_fav(db, user, libro: Libro):
        if eliminar_favorito(db, user, libro):
            page.snack_bar = ft.SnackBar(ft.Text("Libro eliminado de favoritos."), bgcolor="green")
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Error al eliminar favorito."), bgcolor="red")
        page.snack_bar.open = True
        favoritos = get_favoritos(db, user) or []
        cargar_favoritos()
        page.update()

    barra_busqueda = ft.Row([
        search_input,
        search_button
    ], alignment="center", vertical_alignment="center", spacing=10)

    search_input.on_submit = on_buscar
    search_button.on_click = on_buscar

    btn_volver = ft.ElevatedButton(
        "Volver",
        icon="arrow_back",
        on_click=lambda e: volver_al_menu()
    )

    main_column = ft.Column([
        ft.Text("📚 Mis libros favoritos", size=28, weight="bold", color="#2d3e50", font_family="Georgia", text_align="center"),
        barra_busqueda,
    ], alignment="center", horizontal_alignment="center", expand=True, spacing=20)

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
        ft.Column([main_content], expand=True, alignment="center", horizontal_alignment="center")
    )
    cargar_favoritos()
    page.update()
