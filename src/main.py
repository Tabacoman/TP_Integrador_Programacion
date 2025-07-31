from db.database import Database
from gui.Login import login_interfaz
from gui.Interfaz import main_interfaz  # Esta será la interfaz principal tras el login

def main():
    db = Database()
    # Lanza la interfaz de login. Si el login es exitoso, pasa a la interfaz principal.
    login_interfaz(db, on_login_success=lambda user: main_interfaz(db, user))

if __name__ == "__main__":
    main()