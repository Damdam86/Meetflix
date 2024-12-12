import pandas as pd
import ast
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import requests
import streamlit as st
import random


api_key = st.secrets['API_KEY']


@st.cache_data
def load_data():
    file_path = 'https://sevlacgames.com/tmdb/new_tmdb_movie_list.csv'
    df = pd.read_csv(file_path, sep=',')
    return df

# Chargement et préparation des données
@st.cache_data
def load_and_prepare_data(file_path='https://sevlacgames.com/tmdb/new_tmdb_movie_list.csv'):
    # Chargement du dataset
    data = pd.read_csv(file_path)
    # Convertir la colonne `genres` en dictionnaires
    data['genres'] = data['genres'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    # Créer une nouvelle colonne contenant uniquement les noms des genres
    data['genre_names'] = data['genres'].apply(lambda genres: [genre['name'] for genre in genres] if genres else [])
    # Utiliser `get_dummies` pour créer des colonnes de genres
    genres_dummies = data['genre_names'].str.join('|').str.get_dummies()
    # Ajouter les genres au DataFrame original
    data_extended = pd.concat([data, genres_dummies], axis=1)

    # Sélectionner les colonnes numériques et les genres dummies
    numerical_features = data[['vote_average', 'vote_count']]  # Ajouter ici d'autres colonnes si nécessaire
    X_extended = pd.concat([numerical_features, genres_dummies], axis=1)

    data.reset_index(drop=True, inplace=True)
    X_extended.reset_index(drop=True, inplace=True)

    return data, X_extended

# Préparation du pipeline KNN
@st.cache_data
def create_and_train_pipeline(X_extended):
    # Préparation du pipeline pour le modèle KNN
    pipeline = Pipeline([
        ('scaler', StandardScaler()),  # Standardisation des données
        ('knn', NearestNeighbors(n_neighbors=11))  ### Modification du n_neighbors pour monter ou diminuer le nbre de recommandation ###
    ])

    # Entraîner le pipeline sur `X_extended`
    pipeline.fit(X_extended)

    return pipeline

# Fonction de recommandation
def recommend_movies(movie_id, data, X_extended, pipeline):
    # Vérifier si l'ID du film existe dans les données
    if not data['id'].isin([movie_id]).any():
        return []

    # Trouver l'index du film à partir de l'ID
    movie_index = data.index[data['id'] == movie_id].tolist()[0]

    # Préparer les données du film à recommander
    movie_data = pd.DataFrame([X_extended.iloc[movie_index]], columns=X_extended.columns)

    # Standardiser les données
    data_scale = pipeline.named_steps['scaler'].transform(movie_data)

    # Obtenir les voisins les plus proches en utilisant KNN
    distances, indices = pipeline.named_steps['knn'].kneighbors(data_scale)
    voisins = data.iloc[indices[0]].copy()
    voisins['Distance'] = distances[0]

    # Filtrer le film original pour ne pas l'afficher comme une recommandation
    voisins = voisins[voisins['id'] != movie_id]

    # Récupérer les informations des voisins (posters et titres) à partir du dataset
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
def get_person_with_id(df: pd.DataFrame, person_id: int) -> dict:
    for _, movie in df.iterrows():
        cast = movie['cast']
        if isinstance(cast, str):  # Convertir les chaînes JSON en liste de dictionnaires
            cast = ast.literal_eval(cast)

        if isinstance(cast, list):  # Vérifiez si c'est bien une liste
            for person in cast:
                if person['id'] == person_id:
                    return person
    return None  # Aucun acteur trouvé

# return a dataframe of all the movie where a person appear in

def get_movies_with_person_id(df: pd.DataFrame, person_id: int) -> pd.DataFrame:
    df_movie = pd.DataFrame()
    person = get_person_with_id(df, person_id)
    if not person or 'known_for_titles' not in person or not isinstance(person['known_for_titles'], list):
        return df_movie  # Retournez un DataFrame vide si la personne ou les titres sont invalides

    for movie_id in person['known_for_titles']:
        if df_movie.empty:
            df_movie = get_movie_with_id(df, movie_id)
        else:
            df_movie = pd.concat([df_movie, get_movie_with_id(df, movie_id)], ignore_index=True)

    return df_movie
