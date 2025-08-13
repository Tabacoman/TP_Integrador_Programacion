import flet as ft
from Utilities.funtions import log_in

def login_view(page: ft.Page, db, on_login_success):
    def btn_ingresar(usuario, contrasena):
        print("funcion ejecutada", usuario, contrasena)
        user = log_in(db, usuario, contrasena)
        if user:
            on_login_success(page, user)
        else:
            mensaje_error.value = "Usuario o contraseña incorrectos"
        page.update()

    page.title = "Bienvenido a la Biblioteca"
    page.clean()

    usuario = ft.TextField(label="Usuario", width=300, bgcolor= ft.Colors.LIGHT_BLUE_100, color="black",hint_text="Usuario",hint_style=ft.TextStyle(color="black"))
    contrasena = ft.TextField(label="Contraseña", password=True, width=300, bgcolor= ft.Colors.LIGHT_BLUE_100, color="black",hint_text="Password",hint_style=ft.TextStyle(color="black"))
    mensaje_error = ft.Text("", color="red", size=16)

    fondo = ft.Container(
        expand=True,
        bgcolor="#f5f5dc",
        
        # bgimage_src="ruta/a/tu/imagen.jpg",  # Descomenta y pon la ruta si quieres fondo de imagen
        content=ft.Column([
            ft.Icon(name="menu_book", size=80, color="#568ec7"),
            ft.Text("Bienvenido a la Biblioteca Virtual", size=32, weight="bold", color="#2d3e50"),
            ft.Text("Un lugar para relajarte y disfrutar la lectura", size=18, color="#2d3e50"),
            usuario,
            contrasena,
            mensaje_error,
            ft.ElevatedButton(
                "Ingresar",
                width=300,
                on_click=lambda e: btn_ingresar(usuario.value, contrasena.value)
            )
        ], alignment="center", horizontal_alignment="center"),
        alignment=ft.alignment.center
    )
    page.theme = ft.Theme(font_family="Times New Roman")
    page.add(fondo)
    page.update()