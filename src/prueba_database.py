# Ejemplo para ver todos los usuarios de la base de datos

from db.database import Database
from db.Querys import QUERY_SELECT_ALL_USERS

def mostrar_usuarios():
    db = Database()
    usuarios = db.fetch_all(QUERY_SELECT_ALL_USERS)
    for usuario in usuarios:
        print(f"ID: {usuario['id']}, Usuario: {usuario['username']}, Rol: {usuario['rol']}")

if __name__ == "__main__":
    mostrar_usuarios()