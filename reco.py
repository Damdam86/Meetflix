import streamlit as st
import pandas as pd
import random
import requests
from fonctions import load_and_prepare_data, create_and_train_pipeline, recommend_movies, get_random_backdrops

# API key
api_key = st.secrets["API_KEY"]

# Insertion du CSS dans la page Streamlit
with open('style.css') as c:
    css = c.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Récupérer les backdrops aléatoires
backdrops = get_random_backdrops()

# Afficher le carrousel
if backdrops:
    carousel_html = """
    <div class="slideshow-container">
    """
    for i, backdrop in enumerate(backdrops):
        carousel_html += f"""
        <div class="mySlides fade">
          <div class="numbertext">{i + 1} / {len(backdrops)}</div>
          <img src="{backdrop['url']}" style="width:100%; border-radius: 10px;">
          <a href="/movie?movie_id={backdrop['id']}" style="text-decoration: none; color: inherit;">
          <div class="movie-title-big" style="position: absolute; bottom: 10px; left: 45%; transform: translateX(-50%); background: rgba(0, 0, 0, 0.7); color: white; padding: 10px 20px; border-radius: 5px; text-align: center; font-size: 3rem; font-weight: bold;">
            {backdrop['title']}
          </div>
        </div>
        """

    carousel_html += """
    </div>
    <br>
    <div style="text-align:center">
    """

    for i in range(len(backdrops)):
        carousel_html += f'<span class="dot" style="height: 15px; width: 15px; margin: 2px; background-color: rgba(0,0,0,0.7); border-radius: 100%; display: inline-block;"></span> '

    carousel_html += """
    </div>

    <script>
    let slideIndex = 0;
    showSlides();

    function showSlides() {
      let i;
      let slides = document.getElementsByClassName("mySlides");
      let dots = document.getElementsByClassName("dot");
      for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
      }
      slideIndex++;
      if (slideIndex > slides.length) {slideIndex = 1}    
      for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
      }
      slides[slideIndex-1].style.display = "block";  
      dots[slideIndex-1].className += " active";
      setTimeout(showSlides, 7000); // Change image every 7 seconds
    }
    </script>
    """

    # Afficher le carrousel dans Streamlit
    st.components.v1.html(carousel_html, height=500)
else:
    st.error("Aucun backdrop disponible pour afficher le carrousel.")


# Chargement et préparation des données
data, X_extended = load_and_prepare_data()

# Création et entraînement du pipeline
pipeline = create_and_train_pipeline(X_extended)

# Récupérer les films actuellement au cinéma
now_playing_url = f"https://api.themoviedb.org/3/movie/now_playing?language=fr-FR&page=1&api_key={api_key}"
response = requests.get(now_playing_url)
response.raise_for_status()
movies = response.json().get("results", [])

# Récupérer les meilleurs films
top_rated_url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=fr-FR&page=1&sort_by=vote_average.desc&without_genres=99,10755&vote_count.gte=200&api_key={api_key}"
response2 = requests.get(top_rated_url)
response2.raise_for_status()
movies_top_rated = response2.json().get("results", [])


# Sélectionner 5 films aléatoires
random_movies = random.sample(movies, min(len(movies), 5))


st.markdown("# Les films actuellement au cinéma")

# Création de 5 colonnes pour l'affichage
cols = st.columns(5)
for i, movie in enumerate(random_movies):
    with cols[i % 5]:
        # Vérifier si le poster existe
        poster_path = movie.get('poster_path')  # Utilisation de `poster_path`
        movie_name = movie.get('original_title') 
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            poster_url = "https://via.placeholder.com/200x300.png?text=Aucune+affiche"

        # Affichage du film avec titre et note
        st.markdown(f"""
            <div class='movie-card'>
                <a href="/movie?movie_id={movie['id']}" style="text-decoration: none; color: inherit;" target="_self">
                <img src='{poster_url}' class='movie-poster'>
                <p>{movie['title']}</p>
                <p class='movie-meta'>⭐ {movie.get('vote_average', 'N/A')}/10</p>
                </a>
            </div>
        """, unsafe_allow_html=True)

st.markdown("# Testez nos recommandations")

# Distribution et nbre de colonnes
col1, col2, col3 = st.columns([3, 1, 3])


# Mode 1 : Film similaire
with col1:
    st.subheader("Basé sur un film")
    st.write("Indiquez un film et nous vous recommanderons des titres similaires.")
    # Utilisation du selectbox pour choisir un film
    titres = data['title'].tolist()
    selected_movie_title = st.selectbox("Choisissez un film :", titres)
    # Récupérer l'ID du film sélectionné
    selected_movie_id = data[data['title'] == selected_movie_title]['id'].values[0]

with col2:  # Colonne de séparation
    st.text("")

# Mode 2 : Réponse questionnaire
with col3:
    st.subheader("Basé sur vos réponses")
    st.write("3 questions simples et obtenez des recommandations personnalisées.")
    st.button("Commencer", key="start_questionnaire")
    genre = st.radio(
        "Préférez-vous un film récent ?",
        ["Oui", "Non", "Peu importe"]
    )

################################################################################
# Mode 1 : Film similaire
################################################################################

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
            st.write(f"Note : {voisin['note']}")


# Création de 5 colonnes pour l'affichage
st.markdown("# Les films les plus populaires")

# Vérifier si la liste est vide
if movies_top_rated:
    cols = st.columns(6)
    for i, movie in enumerate(movies_top_rated):
        with cols[i % 6]:
            # Vérifier si le poster existe
            poster_path = movie.get('poster_path')
            movie_name = movie.get('title', 'Titre inconnu') 
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/200x300.png?text=Aucune+affiche"

            # Affichage du film
            st.markdown(f"""
                <div class='movie-card'>
                    <a href="/movie?movie_id={movie['id']}" style="text-decoration: none; color: inherit;" target="_self">
                    <img src='{poster_url}' class='movie-poster'>
                    <p>{movie_name}</p>
                    <p class='movie-meta'>⭐ {movie.get('vote_average', 'N/A')}/10</p>
                    </a>
                </div>
            """, unsafe_allow_html=True)
else:
    st.warning("Aucun film populaire trouvé.")