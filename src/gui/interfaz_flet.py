import flet as ft
from gui.abm_libros_flet import abm_libros_view
from gui.buscar_libro_flet import buscador_libro_view
from gui.mis_favoritos_flet import favoritos_view
from gui.login_flet import login_view


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

    # Libro recomendado (puedes cambiar los datos o traerlos de la base de datos)
    libro_destacado = {
        "titulo": "Harry Potter y el misterio del príncipe",
        "autor": "J.K. Rowling",
        "resena": "La serie de libros 'Harry Potter', escrita por J.K. Rowling, trata sobre las aventuras de un joven mago llamado Harry Potter y sus amigos Hermione Granger y Ron Weasley mientras estudian en el Colegio Hogwarts de Magia y Hechicería. La trama central gira en torno a la lucha de Harry contra el mago tenebroso Lord Voldemort, quien asesinó a sus padres y busca conquistar el mundo mágico.",
        "imagen": "src\\gui\\harry potter.jpg"
    }

    # --- Tema minimalista para la landing principal ---
    left_col = ft.Container(
        expand=True,
        bgcolor="#faf9e3",
        border_radius=ft.border_radius.only(top_left=40, bottom_left=40),
        margin=ft.margin.only(right=20),
        height=500,
        content=ft.Column([
            ft.Container(
                ft.Image(src=libro_destacado["imagen"], width=200, height=300, fit=ft.ImageFit.CONTAIN),
                alignment=ft.alignment.center,
                margin=20
            )
        ], alignment="center", horizontal_alignment="center")
    )

    right_col = ft.Column(
        [
            ft.Text("📖 Libro recomendado", size=28, weight="bold", color="#2d3e50", font_family="Georgia", text_align="center"),
            ft.Text(libro_destacado["titulo"], size=26, weight="bold", color="#2d3e50", font_family="Georgia", text_align="center"),
            ft.Text(f"Autor: {libro_destacado['autor']}", size=20, color="#568ec7", font_family="Georgia", text_align="center"),
            ft.Container(
                ft.Text(libro_destacado["resena"], size=16, color="#2d3e50", font_family="Georgia", text_align="center"),
                margin=ft.margin.symmetric(horizontal=40, vertical=20)
            )
        ],
        alignment="center",
        horizontal_alignment="center",
        spacing=10
    )

    main_content = ft.Container(
        bgcolor="#faf9e3",
        padding=40,
        content=ft.ResponsiveRow([
            ft.Column([left_col], col={"xs": 12, "md": 5, "xl": 4}),
            ft.Column([right_col], col={"xs": 12, "md": 7, "xl": 8}),
        ], alignment="center", vertical_alignment="center", spacing=0),
        border_radius=30,
        margin=ft.margin.only(top=30, left=20, right=20, bottom=20)
    )

    page.add(
        ft.Column([
            header,
            main_content
        ], expand=True)
    )
    page.update()


