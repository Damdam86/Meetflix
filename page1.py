import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_antd_components as sac
import streamlit.components.v1 as components

css = """
<style>
:root {
    --background-color: #121212;
    --primary-color: #01d277;
    --secondary-color: #ffffff;
    --text-color: #e0e0e0;
    --text-muted: #9e9e9e;
    --font-family: 'Roboto', sans-serif;
    --border-radius: 8px;
    --transition-speed: 0.3s ease-in-out;
}
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
body {
    background-color: var(--background-color);
    color: var(--text-color);
    font-family: var(--font-family);
    line-height: 1.6;
}
header {
    background-color: #1c1c1c;
    padding: 10px 20px;
    position: fixed;
    width: 100%;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
}
header a {
    color: var(--secondary-color);
    text-decoration: none;
    margin-right: 20px;
    transition: color var(--transition-speed);
}
header a:hover {
    color: var(--primary-color);
}
header .logo {
    font-size: 24px;
    font-weight: bold;
}
.banner {
    position: relative;
    height: 0.02vh;
    display: flex;
    align-items: center;
    justify-content: center;
    color: 000000;
    text-align: center;
    margin-top: 60px;
}
.banner h1 {
    font-size: 48px;
}
</style>
"""

# Insertion du CSS dans la page Streamlit
st.markdown(css, unsafe_allow_html=True)

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
