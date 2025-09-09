import flet as ft
from db.database import Database
from gui.login_flet import login_view
from gui.interfaz_flet import main_menu

db = Database()
def on_login_success(page, user):
    main_menu(page,db, user, on_login_success)

def main(page: ft.Page):
    # Lanza la interfaz de login. Si el login es exitoso, pasa a la interfaz principal.
    login_view(page, db, on_login_success)

ft.app(target=main)