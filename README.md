📽️ Système de Recommandation de Films

🎯 Objectif

L'objectif de ce projet est de développer un système de recommandation de films robuste pour un cinéma situé dans la région de la Creuse. Ce système vise à stimuler l'engagement des clients et à remédier à la baisse des revenus en proposant des suggestions de films personnalisées.

🤝 Besoin Client

Fournir un outil efficace et convivial permettant de recommander des films adaptés aux préférences des utilisateurs.

⚠️ Problématique

Le cinéma connaît une baisse de revenus et rencontre des difficultés à attirer le public en raison d'un manque de données sur les préférences des clients.

🚧 Contraintes

Aucune donnée interne sur les goûts des clients n'est disponible.

Délai limité pour la livraison du projet.

📅 Rétroplanning

Un planning a été établi pour garantir la livraison des étapes clés du projet :

Collecte des données : Semaine 1

Développement du modèle : Semaines 2-4

Développement de l'interface : Semaine 5

Tests et déploiement : Semaines 6-7

🛠️ Outils et Technologies

💻 Langages de Programmation

Python : Langage principal pour le développement du projet.

HTML & CSS : Pour la mise en page et le design.

📊 Bibliothèques de Manipulation des Données

Pandas : Analyse et transformation des données.

NumPy : Opérations mathématiques et gestion efficace des tableaux.

🤖 Bibliothèques pour la Recommandation et le Machine Learning

Scikit-learn : Calculs de similarité, algorithmes de recommandation et outils d'apprentissage automatique.

📈 Bibliothèques de Visualisation des Données

Matplotlib & Seaborn : Pour visualiser les tendances et les distributions de données.

🧹 Nettoyage et Gestion des Données

Expressions Régulières (re) : Manipulation et nettoyage des textes.

🌐 APIs

TMDB (The Movie Database) : Construction de la base de données des films, incluant titres, genres, notes, et acteurs.

OpenAI API : Génération de mots-clés à partir des synopsis des films.

🖥️ Développement de l'Interface Utilisateur

Streamlit : Création d'applications web interactives et dynamiques.

🌍 Collaboration et Gestion de Version

GitHub & GitHub Desktop : Contrôle de version et collaboration.

🔍 Le Système de Recommandation

Approche KNN

Le système utilise un algorithme de K-Nearest Neighbors (KNN) basé sur différents types de données :

Données Numériques (TMDB) : Scores de popularité des films, normalisés avec StandardScaler.

Données Non-Numériques (TMDB) : Genres et 5 principaux acteurs de chaque film, convertis en variables numériques avec get_dummies.

Données Non-Numériques (OpenAI) : Trois mots-clés par film générés via l'API OpenAI, transformés en variables numériques avec get_dummies.

Métrique de Distance : Distance de Minkowski avec k=26.

Génération de Mots-Clés

Pour améliorer les recommandations basées sur le contenu, des mots-clés sont générés avec l'API OpenAI :

Entrée : Synopsis de plus de 4 000 films.

Sortie : Trois mots-clés simples et pertinents pour chaque film.

Prompt Utilisé :

Basé sur le synopsis suivant du film '{movie_title}', donne-moi 3 mots-clés pertinents : {movie_overview}. Utilise des mots-clés simples (1 mot) qui résument bien le film. L'objectif est d'avoir des mots-clés pertinents afin de pouvoir entraîner un modèle de machine learning et ainsi faire des suggestions de films.

📜 Structure des Dossiers

├── data/              # Données brutes et transformées
├── src/               # Code source du système de recommandation
├── images/            # Visualisations et graphiques
├── README.txt         # Présentation du projet et documentation (ce fichier)

🚀 Comment Lancer le Projet

Cloner le Dépôt :

git clone https://github.com/your_username/film-recommendation-system.git
cd film-recommendation-system

Installer les Dépendances :

pip install -r requirements.txt

Lancer l'Application Streamlit :

streamlit run app/main.py

Accéder à l'Application :
Ouvrez l'URL fournie dans votre navigateur web.

📬 Contact

Pour toute question ou suggestion, n'hésitez pas à me contacter :

Email : your_email@example.com

GitHub : your_username

