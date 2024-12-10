import pandas as pd
import ast
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import requests
import streamlit as st

api_key = st.secrets['API_KEY']

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


def recommend_movies_with_filters(pipeline, data, X_extended, genres=None, actors=None, min_duration=0, max_duration=300):
    # Filtrer par genres si spécifiés
    if genres:
        data = data[data['genre_names'].apply(lambda x: any(genre in x for genre in genres))]
    
    # Filtrer par acteurs si spécifiés (nécessite une colonne 'actors' dans les données)
    if actors and 'actors' in data.columns:
        data = data[data['actors'].apply(lambda x: any(actor in x for actor in actors))]
    
    # Filtrer par durée si spécifiée
    if 'runtime' in data.columns:
        data = data[(data['runtime'] >= min_duration) & (data['runtime'] <= max_duration)]
    
    # Si le DataFrame est vide après filtrage, retourner une liste vide
    if data.empty:
        return []

    # Ajouter les colonnes manquantes avec des zéros pour correspondre au pipeline
    missing_columns = set(X_extended.columns) - set(data.columns)
    for col in missing_columns:
        data[col] = 0

    # Réordonner les colonnes pour correspondre au pipeline
    data = data[X_extended.columns]

    # Obtenir les voisins les plus proches en utilisant KNN
    distances, indices = pipeline.named_steps['knn'].kneighbors(
        pipeline.named_steps['scaler'].transform(data[['vote_average', 'vote_count']])
    )

    # Récupérer les recommandations avec distances
    recommended_movies = []
    for idx, movie_index in enumerate(indices[0]):
        movie = data.iloc[movie_index]
        recommended_movies.append({
            'id': movie['id'],
            'title': movie['title'],
            'poster_path': movie['poster_path'],
            'vote_average': movie['vote_average'],
            'distance': distances[0][idx]
        })

    return recommended_movies




# Récupérer les détails d'un acteur
def get_actors_info(actor_id):
    url = f"https://api.themoviedb.org/3/person/{actor_id}?language=fr-FR&api_key={api_key}"
    response = requests.get(url)
    return response.json()