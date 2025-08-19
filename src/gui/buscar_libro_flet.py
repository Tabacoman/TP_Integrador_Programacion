import flet as ft
from Utilities.funtions import buscar_libros, agregar_favorito, get_favoritos

def buscador_libro_view(page: ft.Page, db, user=None, volver_al_menu=None):
    page.title = "Buscar libro"
    page.clean()

    # Estado de búsqueda
    search_input = ft.TextField(label="Buscar por título, autor o género", expand=True)
    search_button = ft.IconButton(icon="SEARCH", tooltip="Buscar")
    resultados = []

    # Obtener ids de favoritos del usuario
    favoritos = get_favoritos(db, user["id"]) if user else []
    favoritos_ids = {libro["id"] for libro in favoritos} if favoritos else set()

    def cargar_resultados(filtro=""):
        # Buscar libros según filtro
        filtro = filtro.strip()
        if filtro:
            libros = buscar_libros(db, titulo=filtro) + buscar_libros(db, autor=filtro) + buscar_libros(db, genero=filtro)
            # Eliminar duplicados por id
            vistos = set()
            libros_filtrados = []
            for l in libros:
                if l["id"] not in vistos:
                    libros_filtrados.append(l)
                    vistos.add(l["id"])
        else:
            libros_filtrados = buscar_libros(db)
        resultados.controls.clear()
        if not libros_filtrados:
            resultados.controls.append(
                ft.Container(
                    ft.Text("No se encontraron libros.", size=18, color="grey"),
                    alignment=ft.alignment.center,
                    padding=20
                )
            )
        else:
            for libro in libros_filtrados:
                en_favoritos = libro["id"] in favoritos_ids
                resultados.controls.append(
                    ft.Container(
                        ft.Row([
                            ft.Column([
                                ft.Text(f"Título: {libro['titulo']}", size=18, weight="bold"),
                                ft.Text(f"Autor: {libro['autor']}"),
                                ft.Text(f"Año: {libro['anio']}"),
                                ft.Text(f"Género: {libro['genero']}"),
                            ], expand=True),
                            ft.IconButton(
                                icon="star" if en_favoritos else "star_border",
                                tooltip="Agregar a favoritos" if not en_favoritos else "Ya en favoritos",
                                disabled=en_favoritos,
                                icon_color="#FFD700" if en_favoritos else "#888888",
                                on_click=(lambda e, l_id=libro["id"]: on_agregar_favorito(l_id)) if not en_favoritos else None
                            )
                        ], alignment="spaceBetween"),
                        padding=10,
                        margin=ft.margin.symmetric(vertical=4, horizontal=0),
                        bgcolor="#f5f5f5",
                        border_radius=8,
                        shadow=ft.BoxShadow(blur_radius=2, color="#00000022", offset=ft.Offset(0, 2))
                    )
                )
        page.update()

    def on_buscar(e=None):
        cargar_resultados(search_input.value)

    def on_agregar_favorito(id_libro):
        if agregar_favorito(db, user["id"], id_libro):
            page.snack_bar = ft.SnackBar(ft.Text("Libro agregado a favoritos."), bgcolor="green")
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Error al agregar a favoritos o ya está en favoritos."), bgcolor="red")
        page.snack_bar.open = True
        # Actualizar favoritos y recargar resultados
        nonlocal favoritos_ids
        nuevos_favoritos = get_favoritos(db, user["id"]) or []
        favoritos_ids = {libro["id"] for libro in nuevos_favoritos}
        cargar_resultados(search_input.value)

    # Barra superior con input y lupa
    barra_busqueda = ft.Row([
        search_input,
        search_button
    ], alignment="center", vertical_alignment="center", spacing=10)

    search_input.on_submit = on_buscar
    search_button.on_click = on_buscar

    # Botón volver
    btn_volver = ft.ElevatedButton(
        "Volver",
        icon="arrow_back",
        on_click=lambda e: volver_al_menu()
    )

    # Contenedor de resultados
    resultados = ft.Column([], expand=True, scroll="auto")

    # Layout principal
    elementos = [
        ft.Text("📚 Buscar libros", size=24, weight="bold"),
        barra_busqueda,
        resultados,
        btn_volver  
    ]

    page.add(
        ft.Column(elementos, alignment="center", horizontal_alignment="center", expand=True)
    )

    # Cargar todos los libros al inicio
    cargar_resultados()
    page.update()