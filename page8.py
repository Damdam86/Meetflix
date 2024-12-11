import streamlit as st
from fonctions import load_and_prepare_data, create_and_train_pipeline, recommend_movies


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
    width: 50%;
    border-radius: 4px;
}

/* Cast Section */
.circular-image {
    display: block;
    margin: 0 auto;
    border-radius: 50%;
    width: 140px;
    height: 140px;
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

# Chargement et préparation des données
data, X_extended = load_and_prepare_data()

# Création et entraînement du pipeline
pipeline = create_and_train_pipeline(X_extended)

# Conteneur pour l'image et le texte superposé
with st.container():
    # Affichage de l'image 
    st.image("images/header_image.png")

    # Ajout de texte superposé via Markdown
    st.markdown("""
        <div style="position: relative; text-align: center; color: white; margin-top: -180px;">
            <h1 style="background: rgba(0, 0, 0, 0.5); padding: 10px; border-radius: 10px; display: inline-block;">
                Meetflix
            </h1>
        </div>
    """, unsafe_allow_html=True)


# Distribution et nbre de colonnes
col1, col2, col3 = st.columns([3, 1, 3])

# Mode 1 : Film similaire
with col1:
    st.subheader("Basé sur un film que vous aimez")
    st.write("Indiquez un film et nous vous recommanderons des titres similaires.")
    # Utilisation du selectbox pour choisir un film
    titres = data['title'].tolist()
    selected_movie_title = st.selectbox("Choisissez un film :", titres)
    # Récupérer l'ID du film sélectionné
    selected_movie_id = data[data['title'] == selected_movie_title]['id'].values[0]

    # Afficher les recommandations si un film est sélectionné

with col2: # Colonne de séparation
    st.text("")

# Mode 2 : Réponse questionnaire
with col3:
    st.subheader("Basé sur vos réponses")
    st.write("3 questions simples et obtenez des recommandations personnalisées.")
    st.button("Commencer", key="start_questionnaire")
    genre = st.radio(
    "Préférez-vous un film récent ?",
    ["Oui", "Non", "Peu importe"])

################################################################################ Mode 1 : Film similaire ##############################################################################

# Diviser les recommandations en colonnes pour une meilleure lisibilité
cols = st.columns(5)  # Création de 5 colonnes pour l'affichage en ligne

if selected_movie_id is not None and st.button("Recommander des films similaires"):
    st.write(f"Films recommandés pour le film sélectionné : {selected_movie_title}")
    voisins = recommend_movies(selected_movie_id, data, X_extended, pipeline)
    for i, voisin in enumerate(voisins):
        with cols[i % 5]:  # Répartir les films dans les colonnes de manière circulaire
            # Si le poster est disponible
            if voisin['poster']:
                poster_url = f"https://image.tmdb.org/t/p/w500{voisin['poster']}"
            else:
                poster_url = "https://via.placeholder.com/200x300.png?text=Aucune+affiche"

            # Affichage des détails du film
            st.image(poster_url, width=100, caption=voisin['title'])
            st.write(f"Distance : {voisin['distance']:.2f}")
            st.write(f"note : {voisin['note']}")