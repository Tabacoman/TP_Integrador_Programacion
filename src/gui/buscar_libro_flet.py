import flet as ft
from Utilities.funtions import buscar_libros, agregar_favorito, get_favoritos, get_libros
from models.Libro import Libro
from models.User import User

def buscador_libro_view(page: ft.Page, db, user: User, volver_al_menu):
    page.title = "Buscar libro"
    page.clean()

    search_input = ft.TextField(label="Buscar por título, autor o género", expand=True)
    search_button = ft.IconButton(icon="SEARCH", tooltip="Buscar")
    resultados = ft.Column([], expand=True, scroll="auto")

    favoritos = get_favoritos(db, user) if user else []
    favoritos_ids = {libro.id for libro in favoritos} if favoritos else set()

    def cargar_resultados(filtro=""):
        filtro = filtro.strip().lower()
        if filtro:
            libros = (
                buscar_libros(db, Libro(titulo=filtro)) +
                buscar_libros(db, Libro(autor=filtro)) +
                buscar_libros(db, Libro(genero=filtro))
            )
            vistos = set()
            libros_filtrados = []
            for l in libros:
                if l.id not in vistos:
                    libros_filtrados.append(l)
                    vistos.add(l.id)
        else:
            libros_filtrados = get_libros(db)

        resultados.controls.clear()
        if not libros_filtrados:
            resultados.controls.append(
                ft.Container(
                    ft.Text("No se encontraron libros.", size=18, color="grey"),
                    alignment=ft.alignment.center,
                    padding=20,
                    bgcolor="#f5f5f5",
                    border_radius=10,
                    margin=20
                )
            )
        else:
            for libro in libros_filtrados:
                en_favoritos = libro.id in favoritos_ids
                resultados.controls.append(
                    ft.Container(
                        ft.Row([
                            ft.Column([
                                ft.Text(f"Título: {libro.titulo}", size=18, weight="bold"),
                                ft.Text(f"Autor: {libro.autor}"),
                                ft.Text(f"Año: {libro.anio}"),
                                ft.Text(f"Género: {libro.genero}"),
                            ], expand=True),
                            ft.IconButton(
                                icon="star" if en_favoritos else "star_border",
                                tooltip="Agregar a favoritos" if not en_favoritos else "Ya en favoritos",
                                disabled=en_favoritos,
                                icon_color="#FFD700" if en_favoritos else "#888888",
                                on_click=(lambda e, l=libro: on_agregar_favorito(l)) if not en_favoritos else None
                            )
                        ], alignment="spaceBetween"),
                        padding=10,
                        margin=ft.margin.symmetric(vertical=8, horizontal=0),
                        bgcolor="#f4f4f4",
                        border_radius=12,
                        shadow=ft.BoxShadow(blur_radius=4, color="#00000022", offset=ft.Offset(0, 2))
                    )
                )
        page.update()

    def on_buscar(e=None):
        cargar_resultados(search_input.value)

    def on_agregar_favorito(libro: Libro):
        nonlocal favoritos_ids
        try:
            if agregar_favorito(db, user, libro):
                page.open(ft.SnackBar(ft.Text(f"✅ Libro '{libro.titulo}' agregado a favoritos."), bgcolor="green"))
            else:
                page.open(ft.SnackBar(ft.Text("⚠️ Error al agregar o ya estaba en favoritos."), bgcolor="red"))
        except Exception as err:
            page.open(ft.SnackBar(ft.Text(f"❌ Error: {err}"), bgcolor="red"))

        # refrescar favoritos
        nuevos_favoritos = get_favoritos(db, user) or []
        favoritos_ids = {l.id for l in nuevos_favoritos}

        # recargar resultados (sin duplicar)
        resultados.controls.clear()
        cargar_resultados(search_input.value)

        page.update()

    barra_busqueda = ft.Row(
        [search_input, search_button],
        alignment="center", vertical_alignment="center", spacing=10
    )

    search_input.on_submit = on_buscar
    search_button.on_click = on_buscar

    btn_volver = ft.ElevatedButton(
        "Volver",
        icon="arrow_back",
        on_click=lambda e: volver_al_menu()
    )

    # --- Tema igual que main_menu ---
    main_content = ft.Container(
        content=ft.Column([
            ft.Text("Buscar libros", size=28, weight="bold", color="#2d3e50", font_family="Georgia", text_align="center"),
            barra_busqueda,
            resultados,
            btn_volver
        ], alignment="center", horizontal_alignment="center", expand=True, spacing=20),
        bgcolor="#faf9e3",
        border_radius=30,
        padding=40,
        expand=True,
        alignment=ft.alignment.center
    )

    page.add(
        ft.Column([main_content], expand=True, alignment="center", horizontal_alignment="center")
    )

    cargar_resultados()
    page.update()
