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

notebook_path = "C:/Users/cohen/Desktop/Data/Projet_2/source/Les_etapes_cleaning_merging.ipynb"

file_path = 'https://sevlacgames.com/tmdb/new_tmdb_movie_list.csv'
df = pd.read_csv(file_path, sep=',')

def load_notebook_as_html(notebook_path):
    # Lire le fichier .ipynb
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

# Chargement des données
data = pd.read_csv('https://sevlacgames.com/tmdb/new_tmdb_movie_list.csv')

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
        sac.StepsItem(title='Etape 1', description="Etude des données TMDB"),
        sac.StepsItem(title='Etape 2', description="Fusion des tables et filtrage avec TMDB"),
        sac.StepsItem(title='Etape 3', description="Gestion de l'API IMDB et filtrage"),
        sac.StepsItem(title='Etape 4', description="Intégartion dans streamlit, Analyse et statistique"),
        sac.StepsItem(title='Etape 5', description="La base de données finale"),
    ], 
)

# Affichage basé sur la sélection
if selection == "Etape 1":
    st.image("images/etape1.png")
elif selection == "Etape 2":
    st.image("images/etape2.png")
    st.image("images/etape3.png")
    st.title("Les requettes pour la création de la base avec IMDB")
    html_content = load_notebook_as_html(notebook_path)
    components.html(html_content, height=800, scrolling=True)
elif selection == "Etape 3":
    st.title("Les requettes pour la création de la base avec TMDB et l'API")
    html_content = load_notebook_as_html(notebook_path)
    components.html(html_content, height=800, scrolling=True)
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



    #selected_X = st.selectbox(label="Choisissez la colonne X", options=data.columns)
    #selected_Y = st.selectbox(label="Choisissez la colonne Y", options=data.columns)
    #selected_color = st.selectbox(label="Choisissez la colonne pour l'affichage couleur", options=data.columns)
    #selected_size = st.selectbox(label="Choisissez la colonne pour l'affichage de la taille", options=data.columns)
    #selected_graph = st.selectbox(label="Quel graphique veux tu utiliser ?", options=["scatter", "bar",'line'])

    #correlation_box = st.checkbox(label= "Afficher la matrice de corrélation")

    #if selected_graph == "scatter":
        #try:
            #data[selected_size] = pd.to_numeric(data[selected_size], errors='coerce')
            #data[selected_X] = pd.to_numeric(data[selected_X], errors='coerce')
            #data[selected_Y] = pd.to_numeric(data[selected_Y], errors='coerce')
        #except KeyError:
           # st.error("Veuillez sélectionner une colonne valide contenant des données numériques.")
            #fig = px.scatter(
                #data,
                #x=selected_X,
                #y=selected_Y,
                #color=selected_color,
                #size=selected_size
            #)
            #st.plotly_chart(fig)
    #elif selected_graph == "bar":
        #fig1 = px.bar(
            #data,
            #x=selected_X,
            #y=selected_Y,
            #color=selected_color)
        #st.plotly_chart(fig1)
    #elif selected_graph == "line":
        #fig2 = px.line(
            #data,
            #x=selected_X,
            #y=selected_Y,
            #color=selected_color,
            #size=selected_size)
        #st.plotly_chart(fig2)

    #if correlation_box :
        #st.subheader("Matrice de corrélation")
        #corr = data.corr(numeric_only=True)
        #fig, ax = plt.subplots()
        #sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        #st.pyplot(fig)
elif selection == "Etape 5":
    @st.cache_data
    def load_data():
        df = pd.read_csv(file_path)
        return df
    df = data
    st.header("Result DataFrame")
    st.dataframe(df)