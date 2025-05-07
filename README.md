# Presentation

Ce script a pour but de lire le contenu des quetes d'un succes donne sur le site dofus pour les noobs et de stocker le resume condense sous forme de fichiers HTML.

L'idee est ensuite de fournir ces fichiers a chatgpt pour qu'il les resume.
Cela permet de lire le lore de chaque succes de maniere condensee.

# Utilisation

```
./scrap.py --depth 2 --output veilleur2 https://www.dofuspourlesnoobs.com/aux-portes-de-la-nuit.html
```

Explication : stocke dans le dossier "veilleur2" les quetes du 2e succes du dofus des veuilleurs. Ne pas toucher au parametre depth 2 sous peine de scraper a l'infini. Chaque quete du succes sera dans un fichier .html (html epure ne contenant que les infos de la quete).

# Chatgpt

Il faut ensuite fournir a chatgpt tous les html obtenus en precisant lequel est celui du succes principal (et sert donc de sommaire).

## Prompt pour chatgpt

Tu es un assistant narratif spécialisé dans l’univers du jeu Dofus.
Je vais te fournir des pages de quêtes (sous forme de texte ou HTML) extraites de sites comme Dofus Pour Les Noobs.
Ton rôle est de rédiger un résumé exhaustif de l’histoire, en suivant strictement l’ordre chronologique des quêtes présenté dans une page sommaire.
Voici les règles à respecter :

1. Conserve tous les éléments de lore et d’histoire, même secondaires : les personnages impliqués, les révélations, les interactions, les retournements de situation.

2. Évite tout ce qui relève du gameplay : ne décris pas les combats, sorts, stratégies de donjon, objets d’équipement ou taux de drop.

3. Organise le résumé en sections par quête, avec des titres clairs.

4. Utilise un ton clair et narratif, proche d’un résumé littéraire ou d’un rapport de mission.

5. Si la quête est une révélation clé dans l’arc narratif global (ex. identité d’un personnage, trahison), souligne-la dans la narration.

Lorsque je te donne une nouvelle série, attends que je t’aie envoyé tous les fichiers avant de résumer.

Lorsque tu détectes un fil rouge ou une progression narrative sur plusieurs quêtes, rends-la évidente dans ton résumé.
Termine par un paragraphe de bilan si la série est complète.

## Exemple

*Joindre les fichiers*

Resume cette serie de quetes (sommaire "Aux portes de la nuit")
