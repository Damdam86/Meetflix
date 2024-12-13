import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit_antd_components as sac
import streamlit.components.v1 as components
from streamlit_jupyter import StreamlitPatcher, tqdm
import nbformat
from nbconvert import HTMLExporter
from fonctions import load_data


# Chargement des données
df = load_data()

@st.cache_data
def load_notebook_as_html(notebook_path):
    # Lire le fichier .ipynb
    notebook_path = "C:/Users/cohen/Desktop/Data/Projet_2/source/Les_etapes_cleaning_merging.ipynb"
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    # Convertir le notebook en HTML
    html_exporter = HTMLExporter()
    html_exporter.template_name = "classic"  # Utilisez un template pour un rendu lisible
    (body, _) = html_exporter.from_notebook_node(notebook)
    return body

# Insertion du CSS dans la page Streamlit
with open('style.css') as c:
    css = c.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Titre de la page
st.markdown("""
<div class="banner">
    <h1>📊 Analyse de la base de données</h1>
</div>
            <br>
            <br>
            <br>
""", unsafe_allow_html=True)

st.divider()

selection = sac.steps(
    items=[
        sac.StepsItem(title='Etape 1', description="Etude, filtrage, fusion des données IMDB"),
        sac.StepsItem(title='Etape 2', description="Etude API TMDB, création de la nouvelle base"),
        sac.StepsItem(title='Etape 3', description="Statistique TMDB"),
        sac.StepsItem(title='Etape 4', description="Algorythme de   "),
        sac.StepsItem(title='Etape 5', description="La base de données finale"),
    ], 
)

# Affichage basé sur la sélection

#Etape 1
if selection == "Etape 1":
    st.image("images/etape1.png")


#Etape 2
elif selection == "Etape 2":
    st.image("images/etape2.png")
    st.image("images/etape3.png")
    st.title("Les requettes pour la création de la base avec IMDB")
    html_content = load_notebook_as_html(notebook_path)
    components.html(html_content, height=800, scrolling=True)

#Etape 3
elif selection == "Etape 3":
    st.title("Les requettes pour la création de la base avec TMDB et l'API")
    html_content = load_notebook_as_html(notebook_path)
    components.html(html_content, height=800, scrolling=True)

#Etape 4
elif selection == "Etape 4":
    fig1 = px.histogram(
        df, 
        x='vote_count', 
        nbins=20, 
        title='Distribution du nbre de vote par film',
        labels={'vote_count': 'Vote Count'}
    )

    fig2 = px.histogram(
        df, 
        x='vote_average', 
        title='Distribition de la note moyenne par film',
    )

    # Sélectionner les films populaires (avec plus de 1000 votes)
    popular_movies = df[df['vote_count'] >= 1000]
    # Trier les films populaires par note moyenne de manière descendante et prendre les 10 meilleurs
    top_rated_movies = popular_movies.sort_values(by='vote_average', ascending=False).head(10)
    # Créer un bar chart avec Plotly
    fig3 = px.bar(
        top_rated_movies,
        x='vote_average',
        y='title',
        color='vote_average',
        color_continuous_scale='viridis',
        title='Films les plus appréciés'
    )
    
    #scatter plot des votes vs notes
    fig4 = px.scatter(df, x='vote_count', y='vote_average', hover_data=['title'], title='Votes vs Notes')

    # Affichage côte à côte dans Streamlit
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig3, use_container_width=True)


    with col2:
        st.plotly_chart(fig2, use_container_width=True)
        st.plotly_chart(fig4, use_container_width=True)

#Etape 5
elif selection == "Etape 5":
    st.header("Result DataFrame")
    st.dataframe(df)