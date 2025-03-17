from client.lib.screen.controller import setArgs, showScreen
def goProfil(userID):
    setArgs("show_profil_id", userID)
    showScreen("profil")