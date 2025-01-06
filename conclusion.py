import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_antd_components as sac
import streamlit.components.v1 as components
from fonctions import cinema_creuse
from fonctions import load_data

# Titre de la page
st.markdown("""
<div class="banner">
    <h1>🏁 Nos conclusion</h1>
</div>
            <br>
            <br>
            <br>
""", unsafe_allow_html=True)

# Infos client / projet
col1, col2 = st.columns(2)

with col1:
    st.markdown("## 🎯 Ce qu'on a aimé")
    st.write("L'objectif est de mettre en place un système de recommandation de films...")
    st.markdown("## 🤝 Besoin client")
    st.write("Disposer d’un outil pour la recommandation de films...")

with col2:
    st.markdown("## ⚠️ Ce qu'on a moins aimé")
    st.write("Votre cinéma est actuellement en perte de vitesse avec une baisse du chiffre d'affaires.")
    st.markdown("## 🚧 Contraintes")
    st.write("Aucune donnée interne sur les goûts des clients...")
    st.markdown("## 🏢 Votre métier")
    st.write("Cinéma situé dans la Creuse.")

# Livraison
st.divider()
st.markdown("### 📅 Les évolutions possibles")

