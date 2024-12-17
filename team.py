import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_antd_components as sac
import streamlit.components.v1 as components


# Titre de la page
st.markdown("""
<div class="banner">
    <h1>🤹‍♀️ L'équipe projet</h1>
</div>
            <br>
            <br>
            <br>
""", unsafe_allow_html=True)
st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.header("Yosser")
    st.image("https://raw.githubusercontent.com/Damdam86/Recommandation_film/main/images/Yosser.png")

with col2:
    st.header("Vincent")
    st.image("https://raw.githubusercontent.com/Damdam86/Recommandation_film/main/images/Vincent.png")

with col3:
    st.header("Damien")
    st.image("https://raw.githubusercontent.com/Damdam86/Recommandation_film/main/images/Damien.png")

with col4:
    st.header("Fatma")
    st.image("https://raw.githubusercontent.com/Damdam86/Recommandation_film/main/images/Fatma.png")
