import requests
import zipfile
import io
import os
import shutil

# Configuration
repo_owner = "utilisateur"
repo_name = "repository"
branch = "main"  # Modifier selon la branche souhaitée
destination_folder = "./mon_projet"  # Dossier où mettre à jour les fichiers

# Télécharger l'archive ZIP du dépôt
url = f"https://github.com/{repo_owner}/{repo_name}/archive/{branch}.zip"
response = requests.get(url)

if response.status_code == 200:
    print("Téléchargement de la dernière version...")
    zip_path = io.BytesIO(response.content)

    # Extraire dans un dossier temporaire
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        temp_folder = f"./{repo_name}-temp"
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder)
        zip_ref.extractall(temp_folder)

    extracted_folder = os.path.join(temp_folder, f"{repo_name}-{branch}")

    # Copier les fichiers du dépôt vers le dossier de destination
    for root, _, files in os.walk(extracted_folder):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, extracted_folder)  # Chemin relatif
            dest_path = os.path.join(destination_folder, rel_path)

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(src_path, dest_path)
            print(f"Mise à jour : {rel_path}")

    # Nettoyage du dossier temporaire
    shutil.rmtree(temp_folder)
    print("Mise à jour terminée avec succès !")

else:
    print(f"Erreur lors du téléchargement ({response.status_code})")
