import flet as ft
from gui.abm_libros_flet import abm_libros_view
from gui.buscar_libro_flet import buscador_libro_view
from gui.mis_favoritos_flet import favoritos_view


def main_menu(page: ft.Page, db, user):
    page.title = "Biblioteca - Menú Principal"

    # 🎨 Mismo fondo y tipografía que login
    page.bgcolor = "#F7F5D7"
    page.theme = ft.Theme(font_family="Arial")

    # 🎯 Estilo global para botones
    boton_style = ft.ButtonStyle(
        bgcolor="#3498DB",
        color="white",
        padding=20,
        shape=ft.RoundedRectangleBorder(radius=10),
    )

    bienvenido = ft.Text(
        f"¡Bienvenido, {user['username']}!",
        size=20,
        weight="bold",
        font_family="Arial",
        color="#2C3E50"
    )
    rol_text = ft.Text(
        f"Rol: {user['rol']}",
        size=14,
        font_family="Arial",
        color="#34495E"
    )

    botones = [
        ft.ElevatedButton(
            "🔍 Buscar libros",
            width=300,
            style=boton_style,
            on_click=lambda e: buscador_libro_view(page, db)
        ),
        ft.ElevatedButton(
            "📚 Mis favoritos",
            width=300,
            style=boton_style,
            on_click=lambda e: favoritos_view(page, db, user)
        ),
    ]

    if user.get("rol") == "admin":
        botones.append(
            ft.ElevatedButton(
                "✏️ Gestión de libros (ABM)",
                width=300,
                style=boton_style,
                on_click=lambda e: abm_libros_view(page, db)
            )
        )

    # Botón cerrar sesión
    botones.append(
        ft.ElevatedButton(
            "🚪 Cerrar sesión",
            width=300,
            style=ft.ButtonStyle(
                bgcolor="red",
                color="white",
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            on_click=lambda e: (
                page.clean(),
                login_view(page, db, on_login_success)
            )
        )
    )

    page.clean()
    page.add(
        ft.Container(
            content=ft.Column(
                [bienvenido, rol_text] + botones,
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            expand=True,
            alignment=ft.alignment.center  # 🔹 Centrado total en X e Y
        )
    )

# ⚠️ Import circular evitada usando import dentro de la función
def login_view(page, db, on_login_success):
    from flet_components.login_flet import login_view as real_login
    real_login(page, db, on_login_success)

def on_login_success(page, user):
    from db.database import Database
    db = Database("biblioteca.db")
    main_menu(page, db, user)
