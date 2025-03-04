# Démarrage
Vous pouvez utiliser le **"./start.bat"** pour démarrer Elyon :
### **Arguments** :
Tout les arguments sauf une exceptions (celle-ci sont spécifier en dessous) sont de se format ci-contre : '--{clé} {valeur}'
Listes des arguments existant :

Le type dans le tableau correspond sur quelle parti du programme cette arguments peux influer 

| Clé         | Valeur Attendu                                | Fonction                                                                                                                           | Type   |
| ----------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------ |
| dev         | Aucune (cas spécial)                          | Permet de passer entre le mode "prod" ou "dev"<br>Et d'afficher ou non certaine logs/débogage                                      | All    |
| type        | client/server/local                           | Permet de choisir quel partie du projet doit être lancer (local lance les deux en même et modifie les configuration pour les lier) | All    |
| config      | valeur au choix<br>(ne peut pas être "all")   | Permet de passer outre le système de config de base entre prod et dev (cela permet d'avoir une troisième config pour des test)     | All    |
| clear-data  | client/server/all                             | Permet de supprimer les donnée d'une ou l'autre parti selon la valeur (all supprimer les deux)<br>                                 | All    |
| data-path   | valeur de vôtre choix                         | Permet de changer le dossiers pour stocker les données                                                                             | All    |
| server-host | valeur de vôtre choix                         | Permet de choisir sur quelle host le client va se connecter directement<br>Attention : cela ne fonction que en mode "client"       | Client |
| server-port | valeur de vôtre choix (compris entre 1-50000) | Permet de choisir le port sur lequelle va se lancer le serveur                                                                     | Server |
