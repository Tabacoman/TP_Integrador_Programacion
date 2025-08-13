from db.database import Database

def log_in(db, usuario, contrasena):
    try: 
        user = db.fetch_one(
            "SELECT * FROM usuarios WHERE username = ? AND password = ?",
            (usuario, contrasena)
        )
        print(user)
        return user
    except Exception as e:
        print(e)
        return False

