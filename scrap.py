#!/usr/bin/env python3
import argparse
import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Ensemble global pour stocker les URLs déjà visitées
visited = set()

def get_output_filename(url, output_dir):
    """
    Calcule le nom de fichier (avec la structure de dossier relative) à partir de l'URL.
    Pour les URLs se terminant par un slash ou dont le chemin est vide, "index.html" est utilisé.
    """
    parsed = urlparse(url)
    file_path = parsed.path.lstrip("/")
    if not file_path or file_path.endswith("/"):
        file_path = os.path.join(file_path, "index.html")
    final_file = os.path.join(output_dir, file_path)
    return final_file

def process_url(url, depth, allowed_netloc, output_dir):
    """
    Récupère une URL (uniquement si c'est un document HTML), extrait le contenu du 
    <div class="container"> qui se trouve dans <div id="main-wrap">, l'enregistre dans un fichier
    (conservant le même nom que dans l'URL d'origine) et traite récursivement les liens <a>
    trouvés dans ce conteneur.

    Args:
        url (str): URL à traiter.
        depth (int): Profondeur de récursion restante.
        allowed_netloc (str): Le domaine à autoriser (on ne suit que les liens sur ce domaine).
        output_dir (str): Répertoire où les fichiers seront sauvegardés.
    """
    global visited

    if depth <= 0:
        return

    # Éviter de traiter plusieurs fois la même URL.
    if url in visited:
        return
    visited.add(url)

    print(f"[Profondeur {depth}] Récupération : {url}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Échec lors de la récupération de {url} : {e}")
        return

    # On ne traite que les documents HTML
    content_type = response.headers.get("Content-Type", "")
    if "text/html" not in content_type:
        print(f"Passage de {url} car le contenu n'est pas du HTML (Content-Type: {content_type})")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Chercher d'abord le <div id="main-wrap">, puis le <div class="container"> à l'intérieur.
    main_wrap = soup.find("div", id="main-wrap")
    if main_wrap is None:
        print(f"Pas de <div id='main-wrap'> trouvé dans {url}")
        return

    container = main_wrap.find("div", class_="container")
    if container is None:
        print(f"Pas de <div class='container'> trouvé dans <div id='main-wrap'> de {url}")
        return

    # Déterminer le nom de fichier et s'assurer que le dossier existe
    output_file = get_output_filename(url, output_dir)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Sauvegarder le contenu extrait du container dans une structure HTML minimale
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n<html>\n<head>\n<meta charset='utf-8'>\n")
            f.write(f"<title>{url}</title>\n</head>\n<body>\n")
            f.write(str(container))
            f.write("\n</body>\n</html>")
        print(f"Enregistré : {output_file}")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de {output_file} : {e}")
        return

    # Extraire tous les liens (<a>) à l'intérieur du container
    links = []
    for a_tag in container.find_all("a", href=True):
        href = a_tag.get("href")
        absolute_link = urljoin(url, href)
        parsed_link = urlparse(absolute_link)
        # On traite uniquement les liens qui appartiennent au même domaine
        if parsed_link.netloc and parsed_link.netloc == allowed_netloc:
            links.append(absolute_link)

    # Petite pause pour être poli avec le serveur.
    time.sleep(1)

    # Appeler récursivement process_url sur les liens extraits.
    for link in links:
        process_url(link, depth - 1, allowed_netloc, output_dir)

def main():
    parser = argparse.ArgumentParser(
        description="Récupère de manière récursive des pages HTML à partir d'une URL donnée, "
                    "en extrayant uniquement le contenu dans le <div class='container'> situé dans <div id='main-wrap'>. "
                    "Seuls les documents HTML sont traités (les images, scripts, etc., sont ignorés). "
                    "Les fichiers sont sauvegardés avec le même nom et la même structure que dans l'URL d'origine."
    )
    parser.add_argument("url", help="URL de départ")
    parser.add_argument("--depth", type=int, default=3, help="Profondeur de récursion (par défaut : 3)")
    parser.add_argument("--output", default="pages", help="Répertoire de sortie pour les pages sauvegardées")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    # On limite la récursion au même domaine que l'URL de départ.
    allowed_netloc = urlparse(args.url).netloc

    # Démarrage du traitement récursif.
    process_url(args.url, args.depth, allowed_netloc, args.output)

if __name__ == "__main__":
    main()

