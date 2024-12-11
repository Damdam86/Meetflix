import streamlit as st
import requests
from fonctions import get_actors_info

# Clé API pour TMDb
api_key = st.secrets['API_KEY']



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

######################################## DEBUT PAGE ####################################################

# Récupération des paramètres de l'URL pour obtenir l'ID de l'acteur
query_params = st.experimental_get_query_params()  # Utilisation de experimental_get_query_params car je n'arrive pas à faire fonctionner st.query_params :(
actor_id = query_params.get("actor_id", [None])[0]

# Vérifier si l'ID de l'acteur est valide
if actor_id is None or actor_id == "None":
    st.error("Aucun acteur sélectionné.")
else:
    # Convertir l'ID en entier si nécessaire (certaines APIs peuvent le nécessiter)
    try:
        actor_id = int(actor_id)
    except ValueError:
        st.error("ID de l'acteur non valide.")
        st.stop()

    # Récupérer les détails de l'acteur sélectionné
    actor_details = get_actors_info(actor_id)

    # Vérifier que les détails de l'acteur ont été correctement récupérés
    if actor_details is None or "status_code" in actor_details:
        st.error("Impossible de récupérer les détails de l'acteur. Veuillez vérifier l'ID.")
    else:
        # Affichage des informations détaillées de l'acteur sélectionné
        st.title(actor_details.get("name", "Nom inconnu"))

        # Afficher l'image de l'acteur
        image_width = 300  # Largeur de l'image en pixels

        col1, col2 = st.columns([2, 3])

        with col1:
            profile_path = actor_details.get("profile_path")
            if profile_path:
                st.image(f"https://image.tmdb.org/t/p/original/{profile_path}", caption=actor_details.get("name", "Nom inconnu"), width=image_width)

        # Affichage des autres informations
        with col2:
            st.markdown(f"**Date de naissance :** {actor_details.get('birthday', 'Date de naissance non spécifiée')}")
            st.markdown(f"**Lieu de naissance :** {actor_details.get('place_of_birth', 'Lieu de naissance non spécifié')}")

        st.markdown(f"**Biographie :** {actor_details.get('biography', 'Biographie non disponible')}")
