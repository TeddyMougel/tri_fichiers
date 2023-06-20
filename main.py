import os
import re
import tkinter as tk
from tkinter import filedialog,messagebox

def extract_additional_links(file_content):
    open_links = re.findall(r'window\.open\([\'"](.*?)[\'"]', file_content)
    href_links = re.findall(r'href=[\'"](.*?)[\'"]', file_content)
    redirect_links = re.findall(r"redirection\([\'\"](.*?)[\'\"]", file_content)
    return open_links, href_links, redirect_links

def extract_links(file_path):
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
                        updated_content = updated_content.replace(link, updated_link, 1)
                    elif link.endswith('.php'):
                        if link == "includes/common.php":
                            php_links.append(link)
                            updated_link = '../includes/common_ref.php'
                        elif link.startswith("fonction"):
                            php_links.append(link)
                            updated_link = '../fonctions/' + link 
                        else :
                            php_links.append(link)
                            updated_link = '../' + link
                        if updated_link not in updated_content:
                            updated_content = updated_content.replace(link, updated_link, 1)
                    elif link.endswith('.js'):
                        js_links.append(link)
                        updated_link = '../' + link
                        if updated_link not in updated_content:
                            updated_content = updated_content.replace(link, updated_link, 1)

    with open(file_path, 'w', encoding='iso-8859-1') as file:
        file.write(updated_content)

    return php_links, htm_links, js_links

def move_file(file_name, destination_folder):
    print(file_name + " déplacé dans le dossier " + destination_folder)

    source_path = os.path.join(app_directory, file_name)
    destination_path = os.path.join(app_directory, destination_folder, file_name)
    os.rename(source_path, destination_path)

    php_links, htm_links, js_links = extract_links(destination_path)

    print("Liens PHP :")
    for link in php_links:
        print(link)

    print("Liens HTML :")
    for link in htm_links:
        print(link)

    print("Liens JavaScript :")
    for link in js_links:
        print(link)

    with open(destination_path, 'r', encoding='iso-8859-1') as file:
        content = file.read()
        open_links, href_links, redirect_links = extract_additional_links(content)

        if open_links or href_links or redirect_links:
            additional_links_window = tk.Toplevel()
            additional_links_window.title("Liens supplémentaires")

            links = open_links + href_links + redirect_links
            current_link_index = 0

            def update_link(folder):
                nonlocal current_link_index
                link = links[current_link_index]
                updated_link = "../" + folder + "/" + os.path.basename(link)
                updated_content = content.replace(link, updated_link)
                with open(destination_path, 'w', encoding='iso-8859-1') as file:
                    file.write(updated_content)
                current_link_index += 1
                show_next_link()

            def show_next_link():
                if current_link_index < len(links):
                    link = links[current_link_index]
                    link_label.config(text=link)
                else:
                    additional_links_window.destroy()
                    show_next_file()
            def skip_link():
                nonlocal current_link_index
                current_link_index += 1
                show_next_link()
            
            link_label = tk.Label(additional_links_window, text="Traitement des liens")
            link_label.pack()

            skipbutton = tk.Button(additional_links_window,text="Ignoré",command=skip_link)
            skipbutton.pack()

            folder_buttons = []
            for folder in folder_list:
                button = tk.Button(additional_links_window, text=folder, command=lambda folder=folder: update_link(folder))
                button.pack()
                folder_buttons.append(button)

            show_next_link()

        else:
            show_next_file()

def skip_file():
    show_next_file()

def show_next_file():
    global current_file_index
    if current_file_index < len(file_list):
        file_name = file_list[current_file_index]
        label.config(text=file_name)
        current_file_index += 1
    else:
        label.config(text="Tous les fichiers ont été traités.")

def create_folder():
    def validate_folder():
        new_folder_name = folder_entry.get()
        if new_folder_name:
            new_folder_dir = os.path.join(app_directory, new_folder_name)
            if not os.path.exists(new_folder_dir):
                os.makedirs(new_folder_dir)
                folder_list.append(new_folder_name)
                button = tk.Button(window, text=new_folder_name, command=lambda folder=new_folder_name: move_file(label.cget("text"), folder))
                button.pack()
                folder_window.destroy()
            else:
                messagebox.showerror("Erreur", "Le dossier existe déjà.")
        else:
            messagebox.showerror("Erreur", "Veuillez entrer un nom de dossier.")

    folder_window = tk.Toplevel(window)
    folder_window.title("Créer un dossier")

    folder_label = tk.Label(folder_window, text="Nom du dossier :")
    folder_label.pack()

    folder_entry = tk.Entry(folder_window)
    folder_entry.pack()

    validate_button = tk.Button(folder_window, text="Valider", command=validate_folder)
    validate_button.pack()

window = tk.Tk()
app_directory = os.path.dirname(os.path.abspath(__file__))

file_list = [f for f in os.listdir(app_directory) if os.path.isfile(os.path.join(app_directory, f)) and (f.endswith(".php") or f.endswith(".htm"))]
folder_list = [f for f in os.listdir(app_directory) if os.path.isdir(os.path.join(app_directory, f))]

current_file_index = 0
label = tk.Label(window, text="")
label.pack()
show_next_file()

skip_button = tk.Button(window, text="Skip", command=skip_file)
skip_button.pack()

create_folder_button = tk.Button(window, text="Créer un dossier", command=create_folder)
create_folder_button.pack()

for folder in folder_list:
    button = tk.Button(window, text=folder, command=lambda folder=folder: move_file(label.cget("text"), folder))
    button.pack()

window.mainloop()