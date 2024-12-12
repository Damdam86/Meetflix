import streamlit as st
import ast
from fonctions import load_and_prepare_data, create_and_train_pipeline, recommend_movies

# Chargement et préparation des données
data, X_extended = load_and_prepare_data()
# Création et entraînement du pipeline
pipeline = create_and_train_pipeline(X_extended)

# Récupérer le movie_id depuis l'URL
query_params = st.query_params  # Méthode mise à jour
movie_id = query_params.get("movie_id")

if isinstance(movie_id, list):  # Gérer le cas où c'est une liste
    movie_id = movie_id[0]

movie_id = int(movie_id) if movie_id else None  # Convertir ou None

# CSS pour la page
css = """
<style>
.stApp {
    background-color: #00050d;
    color: white;
}

/* Navigation */
.nav-container {
    background-color: rgba(0, 5, 13, 0.9);
    padding: 1rem;
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 1000;
    display: flex;
    align-items: center;
}
.nav-links {
    display: flex;
    gap: 2rem;
    margin-left: 2rem;
}
.nav-links a {
    color: #cccccc;
    text-decoration: none;
    font-size: 0.9rem;
}
.nav-links a:hover {
    color: white;
}
/* Buttons */
.return-button {
    position: relative;
    top: 20px;
    margin-bottom: 20px;
    background-color: rgba(255, 255, 255, 0.1);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 10px 15px;
    border-radius: 5px;
    font-size: 14px;
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
    transition: background-color 0.3s ease, color 0.3s ease;
}
.return-button:hover {
    background-color: rgba(255, 255, 255, 0.2);
    color: white;
}
.play-button {
    background-color: #00a8e1;
    color: white;
    border: none;
    padding: 8px 24px;
    border-radius: 4px;
    cursor: pointer;
    margin-right: 1rem;
}
.info-button {
    background-color: rgba(255,255,255,0.1);
    color: white;
    border: none;
    padding: 8px 24px;
    border-radius: 4px;
    cursor: pointer;
}
/* Movie Details */
.movie-title {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}
.movie-info {
    font-size: 1rem;
    margin-bottom: 0.5rem;
}
.movie-meta {
    color: #cccccc;
    font-size: 0.9rem;
}
.movie-card {
    cursor: pointer;
    transition: transform 0.2s;
}
.movie-card:hover {
    transform: scale(1.05);
}
.movie-poster {
    width: 60%;
    border-radius: 4px;
}
/* Cast Section */
.circular-image {
    display: block;
    margin: 0 auto;
    border-radius: 50%;
    width: 150px;
    height: 150px;
    object-fit: cover;
}
.circular-image:hover {
    transform: scale(1.05);
}
.actor-container {
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

/* Recommendations */
.recommendations {
    margin-top: 3rem;
}
</style>

"""

# Insertion du CSS dans la page Streamlit
st.markdown(css, unsafe_allow_html=True)

previous_page_url = "/page4"  # Remplace par l'URL de la page précédente si nécessaire
st.markdown(f"""
    <a href="{previous_page_url}" class="return-button" target="_self">← Retour</a>
""", unsafe_allow_html=True)

######################################## Affichage du film sélectionné ####################################################

# Il y aura toujours un movie_id valide
titres = data['title'].tolist()
selected_movie_id = int(movie_id) if movie_id else data.loc[data['title'] == st.selectbox("Choisissez un film :", titres, key="selectbox_movie"), 'id'].values[0]
selected_movie_title = data.loc[data['id'] == selected_movie_id, 'title'].values[0]

##################################### Titre de la page #####################################


st.title(selected_movie_title)



######################################### Partie haute #####################################
# Contenu principal avec deux colonnes
# Ajouter le bouton "Retour" en utilisant le style "info-button"


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
   # Buttons
    st.markdown("""
    <button class='play-button'>▶ Voir le film</button>
    <button class='info-button'>+ Ajouter aux favoris</button>
    """, unsafe_allow_html=True)
    st.markdown(f"**A voir sur :** ")


with col3:  # Résumé et détails techniques
    st.markdown("#### 📝 Synopsis")
    st.write(data.loc[data['id'] == selected_movie_id, 'overview'].values[0])

    # Affichage des acteurs principaux
    st.markdown("#### 📸 Distribution :")
    crew = data.loc[data['id'] == selected_movie_id, 'cast'].values[0]
    actors = ast.literal_eval(crew) if isinstance(crew, str) else crew
    actor_cols = st.columns(5)  # Crée 5 colonnes pour les acteurs
    for i, actor in enumerate(actors[:5]):
        with actor_cols[i % 5]:
            st.markdown(f"""
            <div class="actor-container">
                <img class="circular-image" src="https://image.tmdb.org/t/p/original/{actor['profile_path']}" alt="{actor['name']}">
                <a href="/actor?actor_id={actor['id']}" target="_self">
                    <div class='actor-name'>{actor['name']}</div>
                </a>
                <div class="actor-role">{actor['character']}</div>
            </div>
            """, unsafe_allow_html=True)

############################################### PARTIE BASSE ###################################################

# Nos recommandations
st.markdown(f"#### 📸 Nos recommandations pour '{selected_movie_title}'")
voisins = recommend_movies(selected_movie_id, data, X_extended, pipeline)
cols = st.columns(5)  # Création de 5 colonnes pour l'affichage en ligne
for i, voisin in enumerate(voisins):
    with cols[i % 5]:  # Répartir les films dans les colonnes de manière circulaire
        if voisin['poster']:
            poster_url = f"https://image.tmdb.org/t/p/w500{voisin['poster']}"
        else:
            poster_url = "https://via.placeholder.com/200x300.png?text=Aucune+affiche"

        st.markdown(f"""
            <div class='movie-card'>
                <a href="?movie_id={voisin['id']}" style="text-decoration: none; color: inherit;" target="_self">
                <img src='{poster_url}' class='movie-poster'>
                <p>{voisin['title']}</p>
                <p class='movie-meta'>⭐ {voisin['note']:.1f}/10</p>
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


st.markdown("</div>", unsafe_allow_html=True)