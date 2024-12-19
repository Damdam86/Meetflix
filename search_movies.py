import streamlit as st
import requests
import ast
from fonctions import load_and_prepare_data, create_and_train_pipeline, recommend_movies, load_and_prepare_keywords
import df_tmdb_tool as dtt
from data_manager import df_tmdb

# Insertion du CSS dans la page Streamlit
with open('style.css') as c:
    css = c.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Clé API (remplacez par votre propre clé valide)
api_key =st.secrets['API_KEY']

# Chargements des données via load_and_prepare_data
data, numerical_features, genres_dummies, cast_dummies, keywords_dummies = load_and_prepare_data()

# Fonction pour récupérer les films
@st.cache_data
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

@st.cache_data
def get_genres(api_key):
    url = f"https://api.themoviedb.org/3/genre/movie/list?language=fr-FR&api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        genres_data = response.json()
        genres = {genre["id"]: genre["name"] for genre in genres_data["genres"]}
        return genres


######################################################################## BARRE DE NAVIGATION ########################################################################

# Diviser l'affichage en deux colonnes
col1, col2 = st.columns([1, 12])

# Colonne 1 : Affichage du logo
with col1:
    st.image("images/logo.png", width=150)

# Colonne 2 : Affichage du slider
with col2:
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    # Navigation haute
    with col1:
        st.markdown("""
    <br><a href="/reco" style="text-decoration: none;" target="_self">
        <button class="button-navbar-haut">🛖 Accueil</button>
    </a>
    """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
    <br><a href="/movie" style="text-decoration: none;" target="_self">
        <button class="button-navbar-haut">🎬 Les films</button>
    </a>
    """, unsafe_allow_html=True)
    with col3:
        st.markdown("""   
    <br><a href="/actor" style="text-decoration: none;" target="_self">
        <button class="button-navbar-haut">👨‍🎤 Les acteurs</button>
    </a>
    """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
    <br><a href="/search_movies" style="text-decoration: none;" target="_self">
        <button class="button-navbar-haut">🔎 Rechercher</button>
    </a>
    """, unsafe_allow_html=True)

###########################################################################################

# Initialiser la variable de session pour suivre combien de films afficher
if "visible_movies" not in st.session_state:
    st.session_state["visible_movies"] = 20  # Commencer avec 20 films visibles

# Récupération des films
movies_list = df_tmdb 
df_movie_filtered = df_tmdb

genres = dtt.get_all_genre_names()  # Récupération des genres
keywords = dtt.get_all_keywords(df_tmdb)

most_older_year = dtt.get_most_older_year(movies_list)
most_recent_year = dtt.get_most_recent_year(movies_list)

min_vote_average = dtt.get_min_vote_average(movies_list)
max_vote_average = dtt.get_max_vote_average(movies_list)


col1, col2, col3 = st.columns([4,1,4])

with col1: 
    selected_genre = st.multiselect("Filtrez par genre :", genres)
    selected_year = st.slider("Sélectionner une plage d'années", most_older_year, most_recent_year, (most_older_year, most_recent_year))

with col2: #Colonne de séparation
    st.title("")

with col3: 
    selected_keywords = st.multiselect("Filtrez par mots clés :", keywords)
    selected_vote_average = st.slider("Sélectionner une plage de vote", min_vote_average, max_vote_average, (min_vote_average, max_vote_average))

    if selected_genre or selected_year or selected_vote_average or selected_keywords :
        df_movie_filtered = dtt.get_filtered_df(movies_list, genres = selected_genre, min_year = selected_year[0], max_year = selected_year[1], min_vote_average = selected_vote_average[0], max_vote_average = selected_vote_average[1], keywords = selected_keywords)

st.title("") # Texte de séparation

# Limiter l'affichage au nombre défini par `visible_movies`
visible_movies = st.session_state["visible_movies"]
column_number_page = 5

nb_line = int(visible_movies/column_number_page)+1


film = 0
for line in range(0,nb_line,1):
        cols = st.columns(column_number_page)
        for col in cols:
            if film >= visible_movies:
                break
            with col:
                movie = df_movie_filtered.iloc[film]
                #st.markdown(f"**{movie['title']}**")
                if movie["poster_path"]:
                    st.markdown(f"""
                    <div class='movie-card'>
                        <a href="movie?movie_id={movie['id']}" style="text-decoration: none; color: inherit;" target="_self";>
                        <img src='https://image.tmdb.org/t/p/w200{movie['poster_path']}' class='movie-poster'>
                        <p>{movie['title']}</p>
                        </a>
                    </div>
                """, unsafe_allow_html=True)
            film += 1
# Bouton "Afficher plus"
if st.button("Afficher plus"):
    st.session_state["visible_movies"] += 20  # Augmenter de 20 films

