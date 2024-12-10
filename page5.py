import streamlit as st
import requests
from fonctions import get_actors_info

# Clé API pour TMDb
api_key = st.secrets['API_KEY']

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
