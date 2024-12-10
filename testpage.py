import streamlit as st
import ast
from fonctions import load_and_prepare_data, create_and_train_pipeline, recommend_movies, recommend_movies_with_filters

def ask_user_preferences(data):
    st.sidebar.title("Vos Préférences")
    if 'genre_names' in data.columns:
        data['genre_names'] = data['genre_names'].fillna('').apply(lambda x: x if isinstance(x, list) else [])
        genres = st.sidebar.multiselect("Quels genres de films aimez-vous ?", data['genre_names'].explode().unique())
    else:
        genres = []
    actors = st.sidebar.text_input("Acteurs préférés (séparés par des virgules)")
    min_duration = st.sidebar.slider("Durée minimale (en minutes)", 0, 300, 90)
    max_duration = st.sidebar.slider("Durée maximale (en minutes)", 0, 300, 120)
    return genres, actors.split(","), min_duration, max_duration

# Chargement et préparation des données
data, X_extended = load_and_prepare_data()
# Création et entraînement du pipeline
pipeline = create_and_train_pipeline(X_extended)

# Récupérer le movie_id depuis l'URL
query_params = st.experimental_get_query_params()  # Utilisation de experimental_get_query_params
movie_id = query_params.get("movie_id", [None])[0]

# CSS pour le design
css = """
<style>
:root {
    --background-color: #121212;
    --primary-color: #01d277;
    --secondary-color: #ffffff;
    --text-color: #e0e0e0;
    --font-family: 'Roboto', sans-serif;
    --border-radius: 8px;
    --transition-speed: 0.3s ease-in-out;
}
body {
    background-color: var(--background-color);
    color: var(--text-color);
    font-family: var(--font-family);
    margin: 0;
    padding: 0;
}
header {
    background-color: #1c1c1c;
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
header a {
    color: var(--secondary-color);
    text-decoration: none;
    margin: 0 15px;
    font-size: 18px;
}
header a:hover {
    color: var(--primary-color);
}
.carousel {
    position: relative;
    margin: 20px auto;
    width: 80%;
    border-radius: var(--border-radius);
    overflow: hidden;
}
.carousel img {
    width: 100%;
    display: block;
}
.carousel-content {
    position: absolute;
    bottom: 20px;
    left: 20px;
    color: var(--secondary-color);
}
.carousel-content h2 {
    font-size: 28px;
    margin: 0;
}
.carousel-content p {
    font-size: 18px;
    margin: 10px 0;
}
.button {
    display: inline-block;
    margin-top: 10px;
    padding: 10px 20px;
    background-color: var(--primary-color);
    color: var(--secondary-color);
    text-decoration: none;
    border-radius: var(--border-radius);
    transition: background-color var(--transition-speed);
}
.button:hover {
    background-color: #029960;
}
.section {
    margin: 20px auto;
    width: 80%;
}
.section h3 {
    margin-bottom: 10px;
    font-size: 24px;
}
.film-container {
    display: inline-block;
    margin: 10px;
    text-align: center;
    width: 150px;
}
.film-container img {
    width: 100%;
    border-radius: var(--border-radius);
}
.film-container a {
    color: var(--text-color);
    text-decoration: none;
    display: block;
    margin-top: 10px;
}
.film-container a:hover {
    color: var(--primary-color);
}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

# En-tête de navigation
st.markdown(
    """
    <header>
        <a href="#">Accueil</a>
        <a href="#">Films</a>
        <a href="#">Acteurs</a>
        <a href="#">Recherche</a>
    </header>
    """,
    unsafe_allow_html=True
)

# Carrousel principal
if movie_id:
    backdrop_path = data.loc[data['id'] == int(movie_id), 'backdrop_path'].values[0] if 'backdrop_path' in data.columns else '/default_backdrop.jpg'
    title = data.loc[data['id'] == int(movie_id), 'title'].values[0] if 'title' in data.columns else 'Titre inconnu'
    overview = data.loc[data['id'] == int(movie_id), 'overview'].values[0] if 'overview' in data.columns else 'Aucune description disponible.'
else:
    backdrop_path = '/default_backdrop.jpg'
    title = 'Avengers: Endgame'
    overview = 'Description du film principal.'

st.markdown(
    f"""
    <div class="carousel">
        <img src="https://image.tmdb.org/t/p/w1280{backdrop_path}" alt="Film principal">
        <div class="carousel-content">
            <h2>{title}</h2>
            <p>{overview}</p>
            <a href="#" class="button">En savoir plus</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Section "Vos Préférences"
genres, actors, min_duration, max_duration = ask_user_preferences(data)

if genres or actors or min_duration or max_duration:
    recommended_movies = recommend_movies_with_filters(pipeline, data, genres, actors, min_duration, max_duration)
    st.markdown(
        """
        <div class="section">
            <h3>Recommandations Personnalisées</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    rec_cols = st.columns(5)
    for idx, movie in enumerate(recommended_movies):
        with rec_cols[idx % 5]:
            st.markdown(
                f"""
                <div class="film-container">
                    <img src="https://image.tmdb.org/t/p/w500{movie['poster_path']}" alt="{movie['title']}">
                    <a href="/page4?movie_id={movie['id']}">{movie['title']}</a>
                </div>
                """,
                unsafe_allow_html=True
            )

# Section "Nos Genres"
st.markdown(
    """
    <div class="section">
        <h3>Nos Genres</h3>
    </div>
    """,
    unsafe_allow_html=True
)

genre_cols = st.columns(5)
unique_genres = data['genre_names'].explode().unique() if 'genre_names' in data.columns else []
for idx, genre in enumerate(unique_genres[:5]):
    with genre_cols[idx % 5]:
        st.markdown(
            f"""
            <div class="film-container">
                <img src="https://via.placeholder.com/150" alt="{genre}">
                <a href="#">{genre}</a>
            </div>
            """,
            unsafe_allow_html=True
        )

# Ajouter les autres genres dans un expander
with st.expander("Voir plus de genres"):
    extra_genre_cols = st.columns(5)
    for idx, genre in enumerate(unique_genres[5:]):
        with extra_genre_cols[idx % 5]:
            st.markdown(
                f"""
                <div class="film-container">
                    <img src="https://via.placeholder.com/150" alt="{genre}">
                    <a href="#">{genre}</a>
                </div>
                """,
                unsafe_allow_html=True
            )

# Section "Films Populaires"
st.markdown(
    """
    <div class="section">
        <h3>Films Populaires</h3>
    </div>
    """,
    unsafe_allow_html=True
)

popular_cols = st.columns(5)
for idx, (index, row) in enumerate(data.sort_values(by='popularity', ascending=False).head(10).iterrows()):
    with popular_cols[idx % 5]:
        st.markdown(
            f"""
            <div class="film-container">
                <img src="https://image.tmdb.org/t/p/w500{row['poster_path']}" alt="{row['title']}">
                <a href="/page4?movie_id={row['id']}">{row['title']}</a>
            </div>
            """,
            unsafe_allow_html=True
        )
