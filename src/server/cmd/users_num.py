from server.services.database.db import users as User
from server.services.cmd.main import classCMD

class users_num(classCMD):
    def __init__(self):
        super().__init__(
            description="Permet de voir le nombre d'utilisateurs inscrit !",
            args=[]
        )

    def run(self, args=[]):
        print(f"Nombre d'utilisateurs inscrit: {User.len_data()}")