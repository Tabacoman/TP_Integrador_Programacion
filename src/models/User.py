class User:
    def __init__(self, username, password, rol, id=None):
        self.id = id
        self.username = username
        self.password = password
        self.rol = rol