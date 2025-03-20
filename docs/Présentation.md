## Sommaire

## Général
Notre jeu est un jeu de combat de tanks en 2D, développé dans le cadre du Trophée NSI. Il oppose deux joueurs dans une arène où ils doivent s'affronter à l'aide de tanks armés de canons. L'objectif est simple : éliminer l'adversaire tout en évitant ses tirs.
## L'histoire
Tout est parti de notre passion pour la programmation et les jeux vidéo. Quand le professeur nous a parlé du Trophée NSI, nous avons voulu créer un jeu simple, stratégique et compétitif. L’idée d’un combat de tanks en 2D est née de notre envie d’un gameplay rapide à prendre en main, mais avec du challenge. D’abord en local, puis en ligne grâce à Flask, nous avons relevé le défi de gérer la physique, les collisions et la connexion des joueurs. Après des semaines de travail, nous sommes fiers de présenter un jeu fluide.
## Technologies
Pour ce projet, nous avons principalement utilisé **Python** et **Pygame** pour la base du jeu. Nous avons également intégré **Flask** afin de créer un serveur permettant aux joueurs de s'affronter en ligne.
### Gameplay
Ce jeu propose des affrontements **1 contre 1 en ligne**. Les joueurs peuvent se connecter au **serveur officiel** ou à des **serveurs personnels**. Ils peuvent affronter des adversaires aléatoires ou créer des parties privées avec leurs amis. L'objectif est de cumuler un maximum de points pour atteindre la première place du classement sur son serveur.
## Elya
Elya est une documentaliste virtuelle conçu par nous qui permet de répond à la plus part des questions que vous pouvez avoir. Celle-ci a appris l'entière du code et documentation du projet. Elle peut donc répondre de manière précise. Nous avons choisir de faire une partir de cette manière pour que tout les questions est une réponse.

Note : Celle-ci fonction grâce à "Llama 3" sur serveur nous appartenant
Aucune donnée d'historique de conversation n'est sauvegarder avec celle-ci

## Démarrage
#### Arguments
Tout les arguments sauf une exceptions (celle-ci sont spécifier en dessous) sont de se format ci-contre : '--{clé} {valeur}'
Le type dans le tableau correspond sur quelle parti du programme cette arguments peux influer 
Listes des arguments existant :

| Clé         | Valeur Attendu                                | Fonction                                                                                                                               | Type   |
| ----------- | --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| dev         | Aucune (cas spécial)                          | Permet de passer entre le mode "prod" ou "dev"<br>Et d'afficher ou non certaine logs/débogage                                          | All    |
| type        | client/server/local                           | Permet de choisir quel partie du projet doit être lancer (local lance les deux en même et modifie les configuration pour les lier)     | All    |
| config      | valeur au choix<br>(ne peut pas être "all")   | Permet de passer outre le système de [[Config]] de base entre prod et dev (cela permet d'avoir une troisième [[Config]] pour des test) | All    |
| clear-data  | client/server/all                             | Permet de supprimer les donnée d'une ou l'autre parti selon la valeur (all supprimer les deux)<br>                                     | All    |
| data-path   | valeur de vôtre choix                         | Permet de changer le dossiers pour stocker les données                                                                                 | All    |
| server-host | valeur de vôtre choix                         | Permet de choisir sur quelle host le client va se connecter directement<br>Attention : cela ne fonction que en mode "client"           | Client |
| server-port | valeur de vôtre choix (compris entre 1-50000) | Permet de choisir le port sur lequelle va se lancer le serveur                                                                         | Server |

## Structure
Voici la structure de dossiers et fichier du projet ainsi que leurs fonctions de celui-ci

| Dossiers                                                                                                                                                                                                                                                                                                                      | Fonctions                                                                                                                                     |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Dossiers sources avec tout le code de l'application<br>Celui-ci est réparti en 3 sous-dossiers et le loader :<br>- loader (Ficher main principale pour choisir qu'elle parti lancer)<br>- common (se sont des petit fonctions utils entre le client et le serveur)<br>- server (code du serveur)<br>- client (code du client) |                                                                                                                                               |
| "data"                                                                                                                                                                                                                                                                                                                        | Dossiers ou sont stocker les données de l'application<br>Attention : celui-ci peux être modifié par un argument ([[Démarrage]])               |
| docs                                                                                                                                                                                                                                                                                                                          | Toute la documentation de l'application                                                                                                       |
| config                                                                                                                                                                                                                                                                                                                        | Dossiers des trois configurations (common/server/client)<br>common est appliquer au deux partie<br>Pour créer d'autre mode de config ses dire |
| assets                                                                                                                                                                                                                                                                                                                        |                                                                                                                                               |
| scripts                                                                                                                                                                                                                                                                                                                       | Contient divers script pour [[Build]] ou voir le nombre de lignes, etc... (Pour plus d'info [[Scripts]])                                      |

## Scripts
Les scripts sont des petits programmes réaliser en python ou en bat permettant de réaliser certain action. Voici la listes des scripts disponible :

| Chemin                    | fonction                                                                                                                                                                                           |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ./boot.exe                | [[Démarrage\|voir démarrage]]                                                                                                                                                                      |
| ./scripts/build.bat       | Permet de build l'appli [[Build]]                                                                                                                                                                  |
| ./scripts/dependances.bat | Permet d'installer les dépendances (librairie python) nécessaire au bon fonctionnement de l'application                                                                                            |
| ./scripts/line.exe        | Permet une fois lancer, de lui passer un "chemin" et d'y calculer le nombre de lignes total que comporte tout les fichier python qui si trouve. Pour nombre projet il faut donc renseigner "./src" |


## Build 
Nôtre projet peux être "build" pour en récupérer un exécutable plus simple pour le partager, il permet aussi de ne plus avoir besoin de python ainsi que d'installer des dépendances.
Vous pouvez utiliser le [[Scripts]] build.bat pour cela
