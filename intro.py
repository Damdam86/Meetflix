import os
import streamlit as st
import time
from fonctions import load_data, load_and_prepare_data, get_random_backdrops


# Insertion du CSS
with open('style.css') as c:
    css = c.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Initialisation de la session
if "page" not in st.session_state:
    st.session_state["page"] = "intro"

@st.cache_data
def load_functions():
    load_data()
    load_and_prepare_data()
    get_random_backdrops()
    return True

# Fonction principale
def main():
    if st.session_state["page"] == "intro":
        # Affichage de la vidéo centrée
        VIDEO_DATA = "images/intro.mp4"
        DEFAULT_WIDTH = 32
        side = max((100 - DEFAULT_WIDTH) / 2, 0.5)
        _, container, _ = st.columns([side, DEFAULT_WIDTH, side])
        container.video(data=VIDEO_DATA, autoplay=True)

        # Transition après lecture de la vidéo
        if "video_played" not in st.session_state:
            time.sleep(7)  # Temps 
            st.session_state["video_played"] = True

            # Chargement des données
            load_functions()
            st.session_state["page"] = "reco"

            # Redirection vers la page reco.py
            st.switch_page("reco.py")

# Exécution principale
main()
