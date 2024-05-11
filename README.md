# Sakugabooru Video Scraper

Ce script Python permet d'extraire les URLs de vidéos, ainsi que les noms des artistes et des animes associés à partir du site web Sakugabooru, et de les stocker dans une base de données MySQL.

## Prérequis

- Python 3.x
- BeautifulSoup (`pip install beautifulsoup4`)
- Requests (`pip install requests`)
- MySQL Connector (`pip install mysql-connector-python`)

## Configuration de la base de données

Avant d'exécuter le script, assurez-vous de configurer la connexion à votre base de données MySQL en modifiant les informations de connexion .

## Structure de la base de données

Ce projet suppose l'existence d'une base de données avec la structure suivante :

### Table `videos`

- `video_id` : Identifiant unique de la vidéo (clé primaire)
- `url` : URL de la vidéo
- `artiste_id` : Identifiant de l'artiste associé (clé étrangère vers la table `artistes`)
- `anime_id` : Identifiant de l'anime associé (clé étrangère vers la table `animes`)

### Table `artistes`

- `artiste_id` : Identifiant unique de l'artiste (clé primaire)
- `nom_principal` : Nom principal de l'artiste

### Table `animes`

- `anime_id` : Identifiant unique de l'anime (clé primaire)
- `titre_principal` : Titre principal de l'anime

## Utilisation

Assurez-vous de remplacer `post_id` par l'ID du post que vous souhaitez traiter.

## Contributions

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une demande d'extraction.
