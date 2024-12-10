import streamlit as st
import requests

# Clé API (remplacez par votre propre clé valide)
api_key =st.secrets['API_KEY']

# Fonction pour récupérer les films
def get_movies():
    base_url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=fr-FR&page=1&primary_release_date.gte=1950-01-01&primary_release_date.lte=2026-01-01&sort_by=popularity.desc&vote_average.gte=5&vote_average.lte=10&vote_count.gte=1000&with_runtime.gte=70&with_runtime.lte=300&api_key={api_key}"
    movies = []  # Liste pour stocker tous les films
    page = 1  # Première page
    total_pages = None  # Le total temporaire

    while total_pages is None or page <= total_pages:
        url = f"{base_url}&page={page}"
        response = requests.get(url)

        if response.status_code != 200:
            st.error(f"Erreur lors de la récupération des données pour la page {page}.")
            break

        movie_data = response.json()

        for movie in movie_data["results"]:
            movies.append({
                "id": movie["id"],
                "title": movie["title"],
                "poster_path": movie.get("poster_path"),  # Utiliser .get pour éviter KeyError
                'genre_ids': movie['genre_ids']
            })

        if total_pages is None:
            total_pages = movie_data["total_pages"]

        page += 1

    return movies


def get_genres(api_key):
    url = f"https://api.themoviedb.org/3/genre/movie/list?language=fr-FR&api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        genres_data = response.json()
        genres = {genre["id"]: genre["name"] for genre in genres_data["genres"]}
        return genres

# Récupération des films
genres = get_genres(api_key)  # Récupération des genres
movies_list = get_movies()  # Récupération des films

# Questions avec feedback
st.markdown("Note de 0 à 5 :")

st.markdown("Je prefère les films qui se déroulent dans des univers imaginaires ou fantastiques")
fantastic_imaginaire = st.feedback(options="stars", key="fantastic_slider", disabled=False, on_change=None, args=None, kwargs=None)

st.markdown("Les comédies font partie de mes genres préférés")
comedie = st.feedback(options="stars", key="comedie", disabled=False, on_change=None, args=None, kwargs=None)

st.markdown("Je prefère un film avec beaucoup d'action à un film plus lent et contemplatif")
action_lent = st.feedback(options="stars", key="action_lent", disabled=False, on_change=None, args=None, kwargs=None)

st.markdown("Les documentaires m’intéressent autant que les films de fiction")
doc_fiction = st.feedback(options="stars", key="doc_fiction", disabled=False, on_change=None, args=None, kwargs=None)

st.markdown("J'évite les films avec des scènes trop violentes ou effrayantes")
violent = st.feedback(options="stars", key="violent", disabled=False, on_change=None, args=None, kwargs=None)

# Filtrage par genre
selected_genre_name = st.selectbox("Filtrez par genre :", ["Tous"] + list(genres.values()))
selected_genre_id = None if selected_genre_name == "Tous" else [k for k, v in genres.items() if v == selected_genre_name][0]

# Filtrer les films par genre sélectionné
if selected_genre_id:
    filtered_movies = [movie for movie in movies_list if selected_genre_id in movie["genre_ids"]]
else:
    filtered_movies = movies_list

# Initialiser la variable de session pour suivre combien de films afficher
if "visible_movies" not in st.session_state:
    st.session_state["visible_movies"] = 20  # Commencer avec 20 films visibles

# Bouton "Afficher plus"
if st.button("Afficher plus"):
    st.session_state["visible_movies"] += 20  # Augmenter de 20 films

# Limiter l'affichage au nombre défini par `visible_movies`
visible_movies = st.session_state["visible_movies"]

# Afficher les films sous forme de vignettes
columns = st.columns(5)  # 5 colonnes
for i, movie in enumerate(filtered_movies[:visible_movies]):  # Utiliser `filtered_movies`
    col = columns[i % 5]  # Répartir les films dans les colonnes
    with col:
        st.markdown(f"**{movie['title']}**")
        if movie["poster_path"]:
            st.image(
                f"https://image.tmdb.org/t/p/w200{movie['poster_path']}",
                width=120  # Ajuster la largeur des images
            )