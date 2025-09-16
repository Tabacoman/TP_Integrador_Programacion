import flet as ft
from Utilities.funtions import log_in, insert_usuario
from models.Libro import Libro
from models.User import User

def login_view(page: ft.Page, db, on_login_success):
    #funcion boton ingresar
    def btn_ingresar(usuario, contrasena):
        user = User(usuario, contrasena,"")
        user = log_in(db, user)
        if user:
            on_login_success(page, user)
        else:
            mensaje_error.value = "Usuario o contraseña incorrectos"
        page.update()

    # --- Registro de nuevo usuario ---
    def abrir_registro(e):
        page.open(dlg_registro)

    def cerrar_registro(e=None):
        page.close(dlg_registro)

    def registrar_usuario(e):
        user = nuevo_usuario.value.strip()
        pwd = nueva_contrasena.value.strip()
        pwd2 = confirmar_contrasena.value.strip()

        if not user or not pwd or not pwd2:
            registro_error.value = "Todos los campos son obligatorios."
        elif pwd != pwd2:
            registro_error.value = "Las contraseñas no coinciden."
        else:
            ok = insert_usuario(db, User(user,pwd,"user"))
            if ok:
                registro_error.value = "Usuario registrado correctamente. Ahora puede iniciar sesión."
                registro_error.color = "green"
                # limpiar campos
                nuevo_usuario.value = ""
                nueva_contrasena.value = ""
                confirmar_contrasena.value = ""
                page.update()
                return
            else:
                registro_error.value = "Error al registrar usuario (ya existe o inválido)."
                registro_error.color = "red"
        page.update()

    # --- UI login ---
    page.title = "Bienvenido a la Biblioteca"
    page.clean()

    usuario = ft.TextField(label="Usuario", width=300, bgcolor=ft.Colors.LIGHT_BLUE_100, color="black")
    contrasena = ft.TextField(label="Contraseña", password=True, width=300, bgcolor=ft.Colors.LIGHT_BLUE_100, color="black")
    mensaje_error = ft.Text("", color="red", size=16)

    # --- Dialogo de registro ---
    nuevo_usuario = ft.TextField(label="Nuevo usuario", width=250)
    nueva_contrasena = ft.TextField(label="Contraseña", password=True, width=250)
    confirmar_contrasena = ft.TextField(label="Confirmar contraseña", password=True, width=250)
    registro_error = ft.Text("", color="red", size=14)

    dlg_registro = ft.AlertDialog(
        modal=True,
        title=ft.Text("Registro de nuevo usuario"),
        content=ft.Column(
            [nuevo_usuario, nueva_contrasena, confirmar_contrasena, registro_error],
            tight=True,
            scroll="adaptive"
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_registro),
            ft.ElevatedButton("Registrar", on_click=registrar_usuario),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    fondo = ft.Container(
        expand=True,
        bgcolor="#f5f5dc",
        content=ft.Column([
            ft.Icon(name="menu_book", size=80, color="#568ec7"),
            ft.Text("Bienvenido a la Biblioteca Virtual", size=32, weight="bold", color="#2d3e50"),
            usuario,
            contrasena,
            mensaje_error,
            ft.ElevatedButton(
                "Ingresar",
                width=300,
                on_click=lambda e: btn_ingresar(usuario.value, contrasena.value)
            ),
            ft.ElevatedButton("Registrarse",width=300 ,  on_click=abrir_registro)  # <-- Botón nuevo
        ], alignment="center", horizontal_alignment="center"),
        alignment=ft.alignment.center
    )

    page.theme = ft.Theme(font_family="Times New Roman")
    page.add(fondo)
    page.update()
