import pandas as pd
import ast
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import requests
import streamlit as st
import random
import df_tmdb_tool as dtt
import requests
import folium



api_key = st.secrets['API_KEY']

# On load les datas (recoltées par l'API TMDB)
@st.cache_data
def load_data():
    file_path = 'https://sevlacgames.com/tmdb/new_tmdb_movie_list2.csv'
    df = pd.read_csv(file_path, sep=',')
    return df

def clean_keywords(keywords, stop_words):
    return [
        word.lower().strip()
        for word in keywords
        if word.isalpha() and word.lower() not in stop_words
    ]

# Chargement et préparation des données
@st.cache_data
def load_and_prepare_data(file_path='https://sevlacgames.com/tmdb/new_tmdb_movie_list2.csv'):
    # Chargement du dataset et convertion des colonne ['genres'] et ['cast'] en dictionnaires, ['origin_country'] en list
    data = dtt.csv_to_df(file_path)

    # Créer une nouvelle colonne contenant uniquement les noms des genres
    data['genre_names'] = data['genres'].apply(lambda genres: [genre['name'] for genre in genres] if genres else [])
    # Créer une nouvelle colonne contenant uniquement les noms des 5 acteurs principaux
    data['cast_names'] = data['cast'].apply(lambda persons: [person['name'] for person in persons[:5]] if persons else [])

    # Utiliser `get_dummies` pour créer des colonnes de mots clés
    keywords_dummies = data['keywords'].str.get_dummies()
    # Utiliser `get_dummies` pour créer des colonnes de genres
    genres_dummies = data['genre_names'].str.join('|').str.get_dummies()
    # Utiliser `get_dummies` pour créer des colonnes de cast
    cast_dummies = data['cast_names'].str.join('|').str.get_dummies()
    
    # Sélectionner les colonnes numériques
    numerical_features = data[['popularity']]

    return data, numerical_features, genres_dummies, cast_dummies, keywords_dummies

def user_define_weights():
        with st.expander("Ajustez les poids des variables", expanded=False):
            #vote_average_weight = st.select_slider("Poids pour 'vote_average'", options=range(1, 11), value=1)
            #vote_count_weight = st.select_slider("Poids pour 'vote_count'", options=range(1, 11), value=1)
            genre_weight = st.select_slider("Poids pour 'genres'", options=range(1, 11), value=1)
            return {
        #'vote_average': vote_average_weight,
        #'vote_count': vote_count_weight,
        'genres': genre_weight
        }

# Préparation du pipeline KNN
@st.cache_data
def create_and_train_pipeline(numerical_features, genres_dummies, cast_dummies, keywords_dummies, weights=None):
    # Définir les poids par défaut pour chaque variable
    if weights is None:
        weights = {
            #'vote_average': 1,  # Plus important
            #'vote_count': 1,    # Moins important
            'genres': 1         # Poids pour les genres
        }

    # Poids pour les colonnes numériques
    numerical_features_weighted = numerical_features.copy()
    for col in numerical_features.columns:
        numerical_features_weighted[col] *= weights.get(col, 1)  # Appliquer les poids dynamiquement

    # Poids pour les genres
    genres_weighted = (genres_dummies**2) * weights['genres']

    # Standardisation des colonnes numériques
    scaler = StandardScaler()
    numerical_features_scaled = scaler.fit_transform(numerical_features_weighted)


    # DataFrame avec l'ensemble des infos
    numerical_features_scaled_df = pd.DataFrame(
        numerical_features_scaled,
        columns=numerical_features.columns,
        index=numerical_features.index
    )

    # Réindexation par sécurité
    numerical_features_scaled_df.reset_index(drop=True, inplace=True)
    genres_weighted.reset_index(drop=True, inplace=True)
    cast_dummies.reset_index(drop=True, inplace=True)
    keywords_dummies.reset_index(drop=True, inplace=True)
    

    # Concaténation de l'ensemble des données (numerique + genre)
    X_extended = pd.concat([numerical_features_scaled_df, genres_weighted, cast_dummies, keywords_dummies], axis=1)
    print(X_extended)

    # Préparation du pipeline pour le modèle KNN
    pipeline = Pipeline([
        ('knn', NearestNeighbors(n_neighbors=26, metric='minkowski'))  # KNN uniquement
    ])

    # Entraînement du modèle KNN
    pipeline.fit(X_extended)

    return pipeline, X_extended, scaler


# Fonction de recommandation
def recommend_movies(movie_id, data, X_extended, pipeline, numerical_features, genres_dummies, cast_dummies, keywords_dummies):
    # Vérifier si l'ID du film existe dans les données
    if not data['id'].isin([movie_id]).any():
        return []

    # Trouver l'index du film à partir de l'ID
    movie_index = data.index[data['id'] == movie_id].tolist()[0]

    # Extraire les données du film sélectionné (directement de X_extended)
    movie_data = X_extended.loc[movie_index].to_frame().T

    # Trouver les voisins les plus proches
    distances, indices = pipeline.named_steps['knn'].kneighbors(movie_data)

    # Récupérer les voisins
    voisins = data.iloc[indices[0]].copy()
    voisins['Distance'] = distances[0]

    # Exclure le film original des recommandations
    voisins = voisins[voisins['id'] != movie_id]

    # Construire la liste des recommandations
    voisins = voisins.sort_values(by='Distance')
    recommended_movies = []
    for index in voisins.index:
        voisin_movie = data.loc[index]
        recommended_movies.append({
            "id": voisin_movie['id'],
            "title": voisin_movie['title'],
            "poster": voisin_movie['poster_path'],
            "note": voisin_movie['vote_average'],
            "distance": voisins.loc[index, 'Distance']
        })

    return recommended_movies

# Récupérer les détails d'un acteur
def get_actors_info(actor_id):
    url = f"https://api.themoviedb.org/3/person/{actor_id}?language=fr-FR&api_key={api_key}"
    response = requests.get(url)
    return response.json()

def get_random_backdrops():
    try:
        now_playing_url = f"https://api.themoviedb.org/3/movie/now_playing?language=fr-FR&page=1&api_key={api_key}"
        response = requests.get(now_playing_url)
        response.raise_for_status()
        movies = response.json().get("results", [])
        random_movies = random.sample(movies, min(len(movies), 5))  # Sélectionner jusqu'à 5 films aléatoires

        backdrops = []
        for movie in random_movies:
            movie_id = movie["id"]
            backdrops_url = f"https://api.themoviedb.org/3/movie/{movie_id}/images?include_image_language=fr,en&api_key={api_key}"
            response = requests.get(backdrops_url)
            response.raise_for_status()
            images = response.json().get("backdrops", [])
            #filtered_images = [img for img in images if img["aspect_ratio"] > 4]
            if images:
                backdrops.append({
                    "url": f"https://image.tmdb.org/t/p/w1920_and_h427_multi_faces/{images[0]['file_path']}",
                    "title": movie["title"],
                    "id": movie["id"]
                })
        return backdrops
    except Exception as e:
        st.error(f"Erreur lors de la récupération des backdrops : {e}")
        return []
    
# return a movie dataframe using the movie id
def get_movie_with_id(df : pd.DataFrame, movie_id : int) -> pd.DataFrame :
  return df[df["id"] == movie_id]

# return a person dict using the person id
def get_person_with_id(actor_dico: pd.DataFrame, person_id: int) -> dict:
    """
    Retourne un dict contenant les informations d'une personne selon son ID.
    """
    person = actor_dico.loc[actor_dico['id'] == person_id]
    if not person.empty:
        return person.iloc[0].to_dict()  # Retourne les détails sous forme de dictionnaire
    return None  # Aucun acteur trouvé


def get_movies_with_person_id(df: pd.DataFrame, actor_dico: pd.DataFrame, person_id: int) -> pd.DataFrame:
    """
    Retourne un DataFrame des films associés à une personne selon son ID.
    """
    # Récupérer les informations de la personne
    person = get_person_with_id(actor_dico, person_id)
    if not person or 'known_for_titles' not in person or not isinstance(person['known_for_titles'], list):
        return pd.DataFrame()  # Retourner un DataFrame vide si aucun titre associé

    # Liste des IDs des films dans known_for_titles
    movie_ids = person['known_for_titles']

    # Filtrer les films dans le DataFrame principal avec isin
    df_movies = df[df['id'].isin(movie_ids)].copy()

    return df_movies


def cinema_creuse():
    dic_cinema = {'Cinéma Claude Miller' : 'Place du Mail 23400 Bourganeuf',
              'Cinéma Alpha':'rue de Rentiere 23110 Évaux-les-Bains',
              'Eden':'4 place Saint Jacques 23300 La Souterraine',
              'Le Colbert':'50, Grande-Rue 23200 Aubusson',
              'Le Sénéchal':'1, rue du Sénéchal 23000 Guéret'}
    link_main = 'https://api-adresse.data.gouv.fr/search/?q='
    
    coords_cinema = {}

    for nom, adresse in dic_cinema.items() :
        params = {
        "q" : adresse,
        "format" : "json",
        "limit" : 1
    }
        Response = requests.get(link_main, params=params)
        if Response.status_code == 200 :
            data=Response.json()
            coords_cinema[nom] = data['features'][0]['geometry']['coordinates'][::-1]

    cinema_data = {
        'Nom': list(coords_cinema.keys()),
        'lat': [coord[0] if coord else None for coord in coords_cinema.values()],
        'lon': [coord[1] if coord else None for coord in coords_cinema.values()]
    }
    df_cinema = pd.DataFrame(cinema_data)

    return coords_cinema, df_cinema
