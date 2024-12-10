import streamlit as st
import ast
from fonctions import load_and_prepare_data, create_and_train_pipeline, recommend_movies

# Chargement et préparation des données
data, X_extended = load_and_prepare_data()
# Création et entraînement du pipeline
pipeline = create_and_train_pipeline(X_extended)

# Récupérer le movie_id depuis l'URL
query_params = st.experimental_get_query_params()  # Utilisation de experimental_get_query_params
movie_id = query_params.get("movie_id", [None])[0]

# CSS pour la page
css = """
<style>
:root {
    --background-color: #121212;
    --primary-color: #01d277;
    --secondary-color: #ffffff;
    --text-color: #e0e0e0;
    --text-muted: #9e9e9e;
    --font-family: 'Roboto', sans-serif;
    --border-radius: 8px;
    --transition-speed: 0.3s ease-in-out;
}
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
body {
    background-color: var(--background-color);
    color: var(--text-color);
    font-family: var(--font-family);
    line-height: 1.6;
}
.circular-image {
    display: block;
    margin: 0 auto;
    border-radius: 50%;
    width: 100px;
    height: 100px;
    object-fit: cover;
}
.actor-container {
    text-align: center;
    margin-bottom: 30px;
}
.film-container {
    text-align: center;
    margin-bottom: 30px;
}
.actor-name {
    font-weight: bold;
    margin-top: 10px;
}
.actor-role {
    font-style: italic;
    color: gray;
}
a {
    color: black;
    text-decoration: none;
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
</style>
"""

# Insertion du CSS dans la page Streamlit
#st.markdown(css, unsafe_allow_html=True)


#page = st_navbar(["Accueil", "Documentation", "Examples", "Community", "About"])
#st.write(page)


######################################## Affichage du film sélectionné ####################################################

# Il y aura toujours un movie_id valide
titres = data['title'].tolist()
selected_movie_id = int(movie_id) if movie_id else data.loc[data['title'] == st.selectbox("Choisissez un film :", titres, key="selectbox_movie"), 'id'].values[0]
selected_movie_title = data.loc[data['id'] == selected_movie_id, 'title'].values[0]

##################################### Titre de la page #####################################
st.title(selected_movie_title)

######################################### Partie haute #####################################
# Contenu principal avec deux colonnes
col1, col2, col3 = st.columns([1, 1, 3])
image_width = 100  # Largeur de l'image en pixels

with col1:  # Affiche
    poster_path = data.loc[data['id'] == selected_movie_id, 'poster_path'].values[0]
    if poster_path:
        st.image(
            f"https://image.tmdb.org/t/p/original/{poster_path}",
            caption=selected_movie_title,
            use_container_width=True
        )
    else:
        st.image("https://via.placeholder.com/200x300.png?text=Aucune+affiche", caption=selected_movie_title, use_container_width=True)

with col2:  # Informations principales
    st.markdown(f"**Date de sortie :** {data.loc[data['id'] == selected_movie_id, 'release_date'].values[0]}")
    st.markdown(f"**Durée :** {data.loc[data['id'] == selected_movie_id, 'runtime'].values[0]} minutes")
    genres = data.loc[data['id'] == selected_movie_id, 'genres'].values[0]
    if genres:
        genre_names = [genre['name'] for genre in genres]
        st.markdown(f"**Genres :** {', '.join(genre_names)}")
    st.markdown(f"**Note TMDb :** ⭐ {data.loc[data['id'] == selected_movie_id, 'vote_average'].values[0]}")
    st.markdown(f"**Nbre de votes :** 👍 {data.loc[data['id'] == selected_movie_id, 'vote_count'].values[0]}")
    st.button("Ajouter à la liste de favoris")
    st.button("Réservez votre place")
    st.markdown(f"**A voir sur :** ")


with col3:  # Résumé et détails techniques
    st.markdown("#### 📝 Résumé")
    st.write(data.loc[data['id'] == selected_movie_id, 'overview'].values[0])

    # Affichage des acteurs principaux
    st.markdown("#### 📸 Têtes d'affiche :")
    crew = data.loc[data['id'] == selected_movie_id, 'cast'].values[0]
    actors = ast.literal_eval(crew) if isinstance(crew, str) else crew
    actor_cols = st.columns(5)  # Crée 5 colonnes pour les acteurs
    for i, actor in enumerate(actors[:5]):
        with actor_cols[i % 5]:
            st.markdown(f"""
            <div class="actor-container">
                <img class="circular-image" src="https://image.tmdb.org/t/p/original/{actor['profile_path']}" alt="{actor['name']}">
                <a href="/page5?actor_id={actor['id']}" target="_self">
                    <div class='actor-name'>{actor['name']}</div>
                </a>
                <div class="actor-role">{actor['character']}</div>
            </div>
            """, unsafe_allow_html=True)

############################################### PARTIE BASSE ###################################################

# Nos recommandations
st.markdown("#### 📸 Nos recommandations")
st.write(f"Films recommandés pour le film sélectionné : {selected_movie_title}")
voisins = recommend_movies(selected_movie_id, data, X_extended, pipeline)
cols = st.columns(5)  # Création de 5 colonnes pour l'affichage en ligne
for i, voisin in enumerate(voisins):
    with cols[i % 5]:  # Répartir les films dans les colonnes de manière circulaire
        if voisin['poster']:
            poster_url = f"https://image.tmdb.org/t/p/w500{voisin['poster']}"
        else:
            poster_url = "https://via.placeholder.com/200x300.png?text=Aucune+affiche"

        st.markdown(f"""
            <div class="film-container" style="text-align: center; margin-bottom: 20px;">
                <a href="/page4?movie_id={voisin['id']}" target="_self">
                    <img src="{poster_url}" alt="{voisin['title']}" width="100" style="display:block; margin:auto;"/>
                    <div class='film-name' style="color: black; text-decoration: none; margin-top: 10px;">
                        {voisin['title']}
                    </div>
                </a>
            </div>
            """, unsafe_allow_html=True)

# Bande-annonce et avis
col1, col2, col3 = st.columns([1, 1, 3])

with col1:
    st.markdown("#### 🎥 Bande-Annonce")
    st.markdown('**Bande-annonce non disponible**')

with col3:
    st.markdown("#### 💬 Critique")
    st.markdown('**Aucun avis disponible**')
