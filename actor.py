import streamlit as st
import pandas as pd
import ast
import requests
from fonctions import get_actors_info, get_movie_with_id, get_person_with_id, get_movies_with_person_id, load_data
from data_manager import person_dico

# Clé API pour TMDb
api_key = st.secrets['API_KEY']

# Insertion du CSS dans la page Streamlit
with open('style.css') as c:
    css = c.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

actor_dico = pd.DataFrame(person_dico.values())

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
query_params = st.query_params  # Récupération des paramètres
actor_id = query_params.get("actor_id")

if actor_id:
    try:
        actor_id = int(actor_id)
    except ValueError:
        actor_id = None

# Vérifier si l'ID de l'acteur est valide
if actor_id is None:
    st.markdown("### 👨‍🎤 Liste des acteurs disponibles")
    
    # Charger les données des acteurs
    actor_dico = pd.DataFrame(person_dico.values())

    # Liste des noms des acteurs
    actor_names = actor_dico['name'].tolist()
    
    # Affichez une liste déroulante pour sélectionner un acteur
    selected_actor_name = st.selectbox("Choisissez un acteur :", ["Sélectionnez un acteur"] + actor_names)

    if selected_actor_name != "Sélectionnez un acteur":
        selected_actor_id = actor_dico.loc[actor_dico['name'] == selected_actor_name, 'id'].values[0]
        
        # Mettre à jour les paramètres de l'URL
        query_params.update(actor_id=selected_actor_id)
        st.rerun()
    else:
        st.warning("Veuillez sélectionner un acteur pour voir ses détails.")
else:
    # Chargement des données des films
    df_movies_full = load_data()
    df = load_data() # Chargement des films
    df_movies = get_movies_with_person_id(df_movies_full, actor_dico, actor_id).head(10)

    # Récupérer les détails de l'acteur sélectionné
    actor_details = get_person_with_id(actor_dico, actor_id)    

    # Vérifier que les détails de l'acteur ont été correctement récupérés
    if actor_details is None:
        st.error("Impossible de récupérer les détails de l'acteur. Veuillez vérifier l'ID.")
    else:
        st.title(actor_details.get("name", "Nom inconnu"))

        # Afficher l'image de l'acteur
        col1, col3 = st.columns([2, 3])
        with col1:
            profile_path = actor_details.get("profile_path")
            if profile_path:
                st.image(f"https://image.tmdb.org/t/p/original/{profile_path}", width=300)
            st.markdown(f"**Date de naissance :** {actor_details.get('birthday', 'Non spécifiée')}")
            st.markdown(f"**Lieu de naissance :** {actor_details.get('place_of_birth', 'Non spécifié')}")

        with col3:
            st.markdown(f"**Biographie :** {actor_details.get('biography', 'Biographie non disponible')}")


        #statistique
        # Fonction pour extraire les noms des acteurs principaux
        def extract_actors(cast_list, top_n=2):
            try:
                cast = ast.literal_eval(cast_list)  # Convertir en liste de dictionnaires
                return ', '.join([person['name'] for person in cast[:top_n]])  # Prendre les top_n premiers acteurs
            except:
                return None

        # Extraire les acteurs principaux
        df['main_actors'] = df['cast'].apply(lambda x: extract_actors(x, top_n=2))

        def analyse_films_par_acteur(acteur_nom):
            # Filtrer les films de l'acteur
            films_acteur = df[df['main_actors'].str.contains(acteur_nom, na=False)]

            # Vérifier si des films ont été trouvés
            if films_acteur.empty:
                st.warning(f"Aucun film trouvé pour l'acteur : {acteur_nom}")
                return

            # 1. Nombre de films par année
            films_acteur['release_year'] = pd.to_datetime(films_acteur['release_date'], errors='coerce').dt.year
            fig2 = px.histogram(
                films_acteur, 
                x='release_year', 
                nbins=20, 
                title=f"Nombre de films par année avec {acteur_nom}",
                color_discrete_sequence=['indigo']
            )
            fig2.update_layout(
                xaxis_title="Année de sortie",
                yaxis_title="Nombre de films",
                height=600,
                width=1250,
                margin=dict(l=50, r=50, t=50, b=100)
            )

            # 2. Top films par note moyenne (limité aux films ayant plus de 5 votes)
            films_acteur_avec_votes = films_acteur[films_acteur['vote_count'] >= 5]
            top_films_note = films_acteur_avec_votes.sort_values(by='vote_average', ascending=False).head(10)
            fig3 = px.bar(
                top_films_note, 
                x='title', 
                y='vote_average', 
                title=f"Top 10 des films les mieux notés avec {acteur_nom}",
                color='vote_average', 
                color_continuous_scale='viridis'
            )
            fig3.update_layout(
                xaxis_tickangle=-45,
                xaxis_title="Titre des films",
                yaxis_title="Note moyenne",
                height=600,
                width=1250,
                margin=dict(l=50, r=50, t=50, b=150)
            )

            st.plotly_chart(fig2, use_container_width=True)
            st.plotly_chart(fig3, use_container_width=True)

        analyse_films_par_acteur(selected_actor_name)

        # Affichage des films
        st.markdown("#### 🎥 Films de l'acteur :")
        if df_movies.empty:
            st.info("Aucun film trouvé pour cet acteur.")
        else:
            movie_cols = st.columns(5)
            for i, (_, movie) in enumerate(df_movies.iterrows()):
                with movie_cols[i % 5]:
                    poster_url = f"https://image.tmdb.org/t/p/original/{movie.get('poster_path', '')}"
                    movie_title = movie.get("title", "Titre inconnu")
                    movie_id = movie.get("id")
                    st.markdown(f"""
                    <div class='movie-card'>
                    <a href="/movie?movie_id={movie_id}" style="text-decoration: none; color: inherit;" target="_self">
                        <img src="{poster_url}" style="width: 150px; height: 225px; border-radius: 10px;">
                        <p>{movie_title}</p>
                    </div>
                    """, unsafe_allow_html=True)