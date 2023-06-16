import os
import re
import tkinter as tk
from tkinter import filedialog

# Fonction pour extraire les liens du fichier
def extract_links(file_name):
    file_path = os.path.join(app_directory, file_name)
    with open(file_path, 'r', encoding='iso-8859-1') as file:
        php_links = []
        htm_links = []
        js_links = []
        content = file.read()
        updated_content = content

 # Fonction pour extraire les liens du fichier
def extract_links(file_name):
    file_path = os.path.join(app_directory, file_name)
    with open(file_path, 'r', encoding='iso-8859-1') as file:
        php_links = []
        htm_links = []
        js_links = []
        content = file.read()
        updated_content = content

        for i, line in enumerate(updated_content.splitlines()):
            line = line.strip()
            if line.startswith('require_once(') or line.startswith('require(') or line.startswith('include_once(') or line.startswith('include('):
                link = re.search(r"'(.*?)'", line)
                if link:
                    link = link.group(1)
                    if link.endswith('.php') and link.startswith('ajax_'):
                        php_links.append(link)
                        updated_link = './ajax/' + link
                        updated_content = updated_content.replace(link, updated_link)
                        # Mettre à jour la ligne dans le contenu mis à jour
                        updated_content = '\n'.join(updated_content.splitlines()[:i]) + line.replace(link, updated_link) + '\n'.join(updated_content.splitlines()[i+1:]) 
                    elif link.endswith('.php'):
                        print(link)
                        if link =="includes/common.php":
                            php_links.append(link)
                            updated_link = '../includes/common_ref.php'
                            
                            updated_content = updated_content.replace(link, updated_link)
                            # Mettre à jour la ligne dans le contenu mis à jour
                            updated_content = '\n'.join(updated_content.splitlines()[:i]) + line.replace(link, updated_link) + '\n'.join(updated_content.splitlines()[i+1:]) 
                        else :
                            php_links.append(link)
                            updated_link = '../' + link
                            updated_content = updated_content.replace(link, updated_link)
                            # Mettre à jour la ligne dans le contenu mis à jour
                            updated_content = '\n'.join(updated_content.splitlines()[:i]) + line.replace(link, updated_link) + '\n'.join(updated_content.splitlines()[i+1:]) 
                        print("lien update : "+updated_link)
                    elif link.endswith('.js'):
                        js_links.append(link)
                        updated_link = '../' + link
                        updated_content = updated_content.replace(link, updated_link)
                        # Mettre à jour la ligne dans le contenu mis à jour
                        updated_content = '\n'.join(updated_content.splitlines()[:i]) + line.replace(link, updated_link) + '\n'.join(updated_content.splitlines()[i+1:]) 
    
    # Écrire le contenu mis à jour dans le fichier
    with open(file_path, 'w', encoding='iso-8859-1') as file:
        file.write('\n'+ updated_content)
    return php_links, htm_links, js_links

# Fonction pour ranger le fichier sélectionné dans le dossier choisi
def move_file(file_name, destination_folder):
    print(file_name+" deplacer dans le dossier "+destination_folder)
    
    # Extraction des liens du fichier
    php_links, htm_links, js_links = extract_links(file_name)
    
    # Affichage des liens trouvés
    print("Liens PHP :")
    for link in php_links:
        print(link)
    
    print("Liens HTML :")
    for link in htm_links:
        print(link)
    
    print("Liens JavaScript :")
    for link in js_links:
        print(link)
    

    # Déplacement du fichier
    source_path = os.path.join(app_directory, file_name)
    destination_path = os.path.join(app_directory, destination_folder, file_name)
    os.rename(source_path, destination_path)

    # Affichage du fichier suivant
    show_next_file()

# Fonction pour passer au fichier suivant sans le déplacer
def skip_file():
    # Affichage du fichier suivant
    show_next_file()

# Fonction pour afficher le fichier suivant
def show_next_file():
    global current_file_index
    if current_file_index < len(file_list):
        file_name = file_list[current_file_index]
        label.config(text=file_name)
        current_file_index += 1
    else:
        label.config(text="Tous les fichiers ont été traités.")

def create_folder():
    new_folder_path = filedialog.askdirectory()
    if new_folder_path:
        new_folder_name = os.path.basename(new_folder_path)
        new_folder_dir = os.path.join(app_directory, new_folder_name)
        os.makedirs(new_folder_dir)
        folder_list.append(new_folder_name)
        button = tk.Button(window, text=new_folder_name, command=lambda folder=new_folder_name: move_file(label.cget("text"), folder))
        button.pack()

# Création de la fenêtre principale
window = tk.Tk()

# Obtenir le répertoire de l'application
app_directory = os.path.dirname(os.path.abspath(__file__))

# Parcourir les fichiers et dossiers
file_list = [f for f in os.listdir(app_directory) if os.path.isfile(os.path.join(app_directory, f)) and (f.endswith(".php") or f.endswith(".htm")) ]
folder_list = [f for f in os.listdir(app_directory) if os.path.isdir(os.path.join(app_directory, f))]

# Index du fichier actuel
current_file_index = 0

# Affichage initial du premier fichier
label = tk.Label(window, text="")
label.pack()
show_next_file()

# Bouton pour passer au fichier suivant sans le déplacer
skip_button = tk.Button(window, text="Skip", command=skip_file)
skip_button.pack()

# Bouton pour crée un nouveau fichier
create_folder_button = tk.Button(window, text="Créer un dossier", command=create_folder)
create_folder_button.pack()

# Afficher les dossiers en tant que boutons
for folder in folder_list:
    button = tk.Button(window, text=folder, command=lambda folder=folder: move_file(label.cget("text"), folder))
    button.pack()


# Lancement de la boucle principale de l'interface graphique
window.mainloop()