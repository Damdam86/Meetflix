import streamlit as st
import requests
from fonctions import get_actors_info, get_movie_with_id, get_person_with_id, get_movies_with_person_id, load_data
# Clé API pour TMDb
api_key = st.secrets['API_KEY']



# Insertion du CSS dans la page Streamlit
with open('./files/wave.css') as c:
    css = c.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)




######################################## DEBUT PAGE ####################################################

# Récupération des paramètres de l'URL pour obtenir l'ID de l'acteur
query_params = st.query_params  # Méthode mise à jour
actor_id = query_params.get("actor_id")



# Ajouter le bouton "Retour" en utilisant le style "info-button"
previous_page_url = "/page4"  # Remplace par l'URL de la page précédente si nécessaire
st.markdown(f"""
    <a href="{previous_page_url}" class="return-button" target="_self">← Retour</a>
""", unsafe_allow_html=True)

if isinstance(actor_id, list):  # Gérer le cas où c'est une liste
    actor_id = actor_id[0]

actor_id = int(actor_id) if actor_id else None  # Convertir ou None

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
    df = load_data()
    actor_details = get_actors_info(actor_id)
    df_movies = get_movies_with_person_id(df, actor_id).head(10)


    # Vérifier que les détails de l'acteur ont été correctement récupérés
    if actor_details is None or "status_code" in actor_details:
        st.error("Impossible de récupérer les détails de l'acteur. Veuillez vérifier l'ID.")
    else:
        # Affichage des informations détaillées de l'acteur sélectionné
        st.title(actor_details.get("name", "Nom inconnu"))

        # Afficher l'image de l'acteur
        image_width = 300  # Largeur de l'image en pixels

        col1, col2, col3 = st.columns([2,1,12])

        with col1:
            profile_path = actor_details.get("profile_path")
            if profile_path:
                st.image(f"https://image.tmdb.org/t/p/original/{profile_path}", caption=actor_details.get("name", "Nom inconnu"), width=image_width)
            st.markdown(f"**Date de naissance :** {actor_details.get('birthday', 'Date de naissance non spécifiée')}")
            st.markdown(f"**Lieu de naissance :** {actor_details.get('place_of_birth', 'Lieu de naissance non spécifié')}")

        # Affichage des autres informations
        with col2:
            st.markdown("")
        
        with col3:
            st.markdown(f"**Biographie :** {actor_details.get('biography', 'Biographie non disponible')}")


st.markdown("#### 🎥 Films de l'acteur :")
movie_cols = st.columns(5)  # Crée 5 colonnes pour afficher les films
    
for i, (_, movie) in enumerate(df_movies.iterrows()):
    with movie_cols[i % 5]:  # Répartir les films dans les colonnes
        movie_poster = movie.get("poster_path")
        movie_title = movie.get("title", "Titre inconnu")
        movie_id = movie.get("id")

        # Affichage de l'affiche et du titre
        if movie_poster:
            poster_url = f"https://image.tmdb.org/t/p/original/{movie_poster}"
        else:
            poster_url = "https://via.placeholder.com/200x300.png?text=Aucune+affiche"

        st.markdown(f"""
        <div class="movie-card">
            <a href="/movie?movie_id={movie_id}" style="text-decoration: none; color: inherit;" target="_self">
            <img src="{poster_url}" class="movie-poster">
            <p>{movie_title}</p>
            </a>
        </div>
        """, unsafe_allow_html=True)