import flet as ft
from gui.abm_libros_flet import abm_libros_view
from gui.buscar_libro_flet import buscador_libro_view
from gui.mis_favoritos_flet import favoritos_view
from gui.login_flet import login_view
from Utilities.funtions import get_libros
from models.Errors import *


def main_menu(page: ft.Page, db, user, on_login_success):
    page.title = "Biblioteca Moderna"
    page.clean()

    # Función para volver al menú principal
    def volver_al_menu():
        main_menu(page, db, user, on_login_success)

    # Encabezado superior
    header = ft.Container(
        bgcolor="#568ec7",
        padding=ft.padding.symmetric(vertical=20, horizontal=40),
        content=ft.Row([
            ft.Text("Biblioteca Moderna", size=28, weight="bold", color="white", font_family="Arial"),
            ft.Row([
                ft.TextButton("Inicio", style=ft.ButtonStyle(color="white", overlay_color="#2B169F"), on_click=lambda e: volver_al_menu()),
                ft.TextButton("Buscar", style=ft.ButtonStyle(color="white", overlay_color="#2B169F"), on_click=lambda e: buscador_libro_view(page, db, user, volver_al_menu)),
                ft.TextButton("Favoritos", style=ft.ButtonStyle(color="white", overlay_color="#2B169F"), on_click=lambda e: favoritos_view(page, db, user, volver_al_menu)),
                *(
                    [ft.TextButton("ABM Libros", style=ft.ButtonStyle(color="white", overlay_color="#2B169F"), on_click=lambda e: abm_libros_view(page, db, volver_al_menu))]
                    if user.rol == "admin" else []
                ),
                ft.TextButton("Cerrar sesión", style=ft.ButtonStyle(color="white", overlay_color="#e53e3e"), on_click=lambda e: (page.clean(), login_view(page, db, on_login_success))),
            ], spacing=20)
        ], alignment="spaceBetween"),
        border_radius=ft.border_radius.only(top_left=0, top_right=0, bottom_left=20, bottom_right=20),
        shadow=ft.BoxShadow(blur_radius=10, color="#00000033", offset=ft.Offset(0, 4))
    )

    bienvenida = ft.Text(f"¡Bienvenido, {user.username}!", size=26, weight="bold", color="#2d267f", font_family="Arial")
    rol_text = ft.Text(f"Rol: {user.rol}", size=18, color="#4f46e5", font_family="Arial")

    botones = [
        ft.ElevatedButton(
            "🔍 Buscar libros",
            width=250,
            style=ft.ButtonStyle(
                bgcolor="#4f46e5",
                color="white",
                shape=ft.RoundedRectangleBorder(radius=12),
                overlay_color="#6366f1"
            ),
            on_click=lambda e: buscador_libro_view(page, db, user, volver_al_menu)
        ),
        ft.ElevatedButton(
            "📚 Mis favoritos",
            width=250,
            style=ft.ButtonStyle(
                bgcolor="#22d3ee",
                color="#2d267f",
                shape=ft.RoundedRectangleBorder(radius=12),
                overlay_color="#67e8f9"
            ),
            on_click=lambda e: favoritos_view(page, db, user, volver_al_menu)
        ),
    ]

    if user.rol == "admin":
        botones.append(
            ft.ElevatedButton(
                "✏️ Gestión de libros (ABM)",
                width=250,
                style=ft.ButtonStyle(
                    bgcolor="#f59e42",
                    color="white",
                    shape=ft.RoundedRectangleBorder(radius=12),
                    overlay_color="#fbbf24"
                ),
                on_click=lambda e: abm_libros_view(page, db, volver_al_menu)
            )
        )

    botones.append(
        ft.ElevatedButton(
            "🚪 Cerrar sesión",
            width=250,
            style=ft.ButtonStyle(
                bgcolor="#e53e3e",
                color="white",
                shape=ft.RoundedRectangleBorder(radius=12),
                overlay_color="#f87171"
            ),
            on_click=lambda e: (page.clean(), login_view(page, db, on_login_success))
        )
    )

    left_col = ft.Column(
        [
            bienvenida,
            rol_text,
            ft.Container(height=20),
            *botones
        ],
        alignment="center",
        horizontal_alignment="center",
        spacing=20
    )

    # --- Tema minimalista para la landing principal ---
    left_col = ft.Container(
        expand=True,
        bgcolor="#faf9e3",
        border_radius=ft.border_radius.only(top_left=40, bottom_left=40),
        margin=ft.margin.only(right=20),
    )

    # Obtén todos los libros y selecciona los 5 más recientes
    libros = get_libros(db)
    ultimos_libros = sorted(libros, key=lambda l: l.id if l.id is not None else 0, reverse=True)[:5]

    libros_columna = ft.Column(
        [
            ft.Text("Últimos libros agregados", size=28, weight="bold", color="#2d3e50", font_family="Georgia", text_align="center"),
            *[
                ft.Container(
                    ft.Column([
                        ft.Text(libro.titulo, size=22, weight="bold", color="#2d3e50", font_family="Georgia"),
                        ft.Text(f"Autor: {libro.autor}", size=18, color="#568ec7", font_family="Georgia"),
                        ft.Text(f"Año: {libro.anio}", size=16, color="#2d3e50", font_family="Georgia"),
                        ft.Text(f"Género: {libro.genero}", size=16, color="#2d3e50", font_family="Georgia"),
                    ], spacing=2),
                    bgcolor="#f4f4f4",
                    border_radius=16,
                    padding=20,
                    margin=ft.margin.symmetric(vertical=12, horizontal=0),
                    shadow=ft.BoxShadow(blur_radius=8, color="#568ec799", offset=ft.Offset(0, 4)),
                    width=500
                )
                for libro in ultimos_libros
            ]
        ],
        alignment="center",
        horizontal_alignment="center",  # Centrado horizontal
        spacing=10,
        expand=True,
        scroll="auto"
    )

    main_content = ft.Container(
        content=libros_columna,
        bgcolor="#faf9e3",
        border_radius=30,
        padding=40,
        expand=True,
        alignment=ft.alignment.center  # Centra el contenido en el container
    )

    page.add(
        ft.Column([
            header,
            main_content
        ], expand=True, alignment="center", horizontal_alignment="center")
    )
    page.update()


