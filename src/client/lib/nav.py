from client.lib.screen.controller import setArgs, showScreen

# Fonction pour afficher le profil d'un utilisateur par son ID
def goProfil(userID):
    setArgs("show_profil_id", userID)
    showScreen("profil")