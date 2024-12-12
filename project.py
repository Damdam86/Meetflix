import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_antd_components as sac
import streamlit.components.v1 as components

# Insertion du CSS dans la page Streamlit
with open('./files/wave.css') as c:
    css = c.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Titre de la page
st.markdown("""
<div class="banner">
    <h1>📽️ Projet : Recommandation de films</h1>
</div>
            <br>
            <br>
            <br>
""", unsafe_allow_html=True)

# Infos client / projet
col1, col2 = st.columns(2)

with col1:
    st.markdown("## 🎯 Objectif")
    st.write("L'objectif est de mettre en place un système de recommandation de films...")
    st.markdown("## 🤝 Besoin client")
    st.write("Disposer d’un outil pour la recommandation de films...")

with col2:
    st.markdown("## ⚠️ Problématique")
    st.write("Votre cinéma est actuellement en perte de vitesse avec une baisse du chiffre d'affaires.")
    st.markdown("## 🚧 Contraintes")
    st.write("Aucune donnée interne sur les goûts des clients...")
    st.markdown("## 🏢 Votre métier")
    st.write("Cinéma situé dans la Creuse.")


# Livraison
st.divider()
st.markdown("### 📅 Délai de livraison")

# Utilisation de components.html pour intégrer le widget de countdown ! 
components.html(
    """
    <script src="https://cdn.logwork.com/widget/countdown.js"></script>
    <a href="https://logwork.com/countdown-hu2f" 
    class="countdown-timer" 
    data-timezone="Europe/Paris" 
    data-language="fr" 
    data-textcolor="#000000" 
    data-date="2025-01-07 14:00" 
    data-background="#000000" 
    data-digitscolor="#ffffff" 
    data-unitscolor="#000000">🕐</a>
    <br>
    <br>
    """,
    height=300  # Ajustez la hauteur selon vos besoins
)
progress_text = "Avancement du projet"
my_bar = st.progress(0.4, text=progress_text)  

# Rétroplanning 
st.divider()
st.header("📅 Rétroplanning")
st.write("Voici le rétroplanning du projet.")

retroplanning = {
    "Étape": ["Réaliser une étude de marché sur la consommation de cinéma dans la Creuse", 
              "Réaliser une étude de marché sur la consommation de cinéma dans la Creuse", 
              "Appropriation, exploration des données et nettoyage (Pandas, Matplotlib, Seaborn)", 
              "Appropriation, exploration des données et nettoyage (Pandas, Matplotlib, Seaborn)", 
              "Machine learning et recommandations (scikit-learn)",
              "Machine learning et recommandations (scikit-learn)",
              "Affinage, interface et présentation"],
    "Timing": ["Semaine 1", 
               "Semaine 2", 
               "Semaine 3", 
               "Semaine 4",
               "Semaine 5",
               "Semaine 6",
               "Semaine 7"],
    "Statut": ["✅", "✅", "✅", "✅", "🛠️", "🛠️", "📅"]
}
df_retroplanning = pd.DataFrame(retroplanning)

st.write(df_retroplanning)

# Détails du système de recommandation avec conteneur de fond et icônes
st.divider()
st.header("🔧 Détails du Système de Recommandation")
st.write("Le tableau ci-dessous présente les principales caractéristiques de notre système de recommandation.")

system_features = {
    "Caractéristique": [
        "🎯 Personnalisation",
        "🌐 Utilisation de données externes",
        "👥 Filtrage collaboratif",
        "📑 Filtrage basé sur le contenu"
    ],
    "Description": [
        "Recommandations personnalisées basées sur les préférences des utilisateurs",
        "Utilisation de données externes pour pallier l'absence de données internes",
        "Suggestions basées sur les préférences d'autres utilisateurs",
        "Recommandations basées sur les caractéristiques des films"
    ],
    "Statut": ["🛠️", "✅", "🛠️", "📅"]
}
df_system_features = pd.DataFrame(system_features)
st.write(df_system_features)