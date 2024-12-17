import streamlit as st
import pandas as pd
import ast
import requests
from fonctions import get_actors_info, get_movie_with_id, get_person_with_id, get_movies_with_person_id, load_data
# Clé API pour TMDb
api_key = st.secrets['API_KEY']

# Insertion du CSS dans la page Streamlit
with open('style.css') as c:
    css = c.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


######################################################################## BARRE DE NAVIGATION ########################################################################

# Diviser l'affichage en deux colonnes
col1, col2 = st.columns([1, 12])

# Colonne 1 : Affichage du logo
with col1:
    st.image("https://github.com/Damdam86/Meetflix/blob/main/images/logo.png?raw=true", width=150)

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

######################################## DEBUT PAGE ####################################################

# Récupérer le movie_id depuis l'URL
query_params = st.query_params  # Méthode mise à jour
actor_id = query_params.get("actor_id")

if actor_id:
    try:
        actor_id = int(actor_id)
    except ValueError:
        actor_id = None

# Vérifier si l'ID de l'acteur est valide
if actor_id is None:
    st.markdown("### 👨‍🎤 Liste des acteurs disponibles")
    
    # Charger les données des films
    df = load_data()
    
    # Extraire tous les acteurs uniques à partir de la colonne "cast"
    all_cast = []
    for cast_list in df['cast']:
        if isinstance(cast_list, str):  # Vérifier que la donnée est une chaîne JSON
            cast = ast.literal_eval(cast_list)
            all_cast.extend(cast)
    
    # Créer un DataFrame des acteurs uniques
    df_cast = pd.DataFrame(all_cast).drop_duplicates(subset='id', keep='first')
    actor_names = df_cast['name'].tolist()
    
    # Affichez une liste déroulante pour sélectionner un acteur
    selected_actor_name = st.selectbox("Choisissez un acteur :", ["Sélectionnez un acteur"] + actor_names)
    
    if selected_actor_name != "Sélectionnez un acteur":
        selected_actor_id = df_cast.loc[df_cast['name'] == selected_actor_name, 'id'].values[0]
        st.experimental_set_query_params(actor_id=selected_actor_id)
        st.experimental_rerun()
    else:
        st.warning("Veuillez sélectionner un acteur pour voir ses détails.")
else:
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
    movie_cols = st.columns(5)  # Crée 5 colonnes
