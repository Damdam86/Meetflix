import streamlit as st

# Titre de la page
st.markdown("""
<div class="banner">
    <h1>🏁 Nos conclusions</h1>
</div>
            <br>
            <br>
            <br>
""", unsafe_allow_html=True)

# Infos client / projet
col1, col2 = st.columns(2)

with col1:
    st.markdown("## ❤️ Ce qu'on a aimé")
    st.write("- Sujet intéressant et motivant.")
    st.write("- Plusieurs techniques : affichage, machine learning, API, étude de bases de données, etc.")
    st.write("- Bonne entente dans le groupe, avec des qualités différentes entre les membres, ce qui permet de prendre le relais sur certains sujets.")

with col2:
    st.markdown("## ⚠️ Ce qu'on a moins aimé")
    st.write("- La différence de niveau dans le groupe, pas forcément facile à gérer au début, mais plus simple vers la fin grâce à une harmonisation progressive au fil des semaines.")
    st.write("- Nous avons parfois été confrontés aux limitations de Streamlit lorsqu'il s'agissait de créer des éléments plus 'esthétiques'.")


st.divider()
st.markdown("### 🆕 Les évolutions possibles")
st.write("- Mise à jour automatique de notre base de données via l'API TMDB : Actuellement, la base est statique et nécessiterait l'utilisation de l'API pour effectuer des mises à jour régulières.")
st.write("- Création d'un espace utilisateur avec la fonctionnalité d'ajout de films 'favoris' : Les utilisateurs pourraient créer une liste de films favoris, qui servirait de base pour générer des recommandations encore plus personnalisées.")
