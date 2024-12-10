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
import streamlit_pandas as sp
from st_aggrid import AgGrid

notebook_path = "C:/Users/cohen/Desktop/Data/Projet_2/source/Les_etapes_cleaning_merging.ipynb"

file_path = 'C:/Users/cohen/Desktop/Data/Projet_2/source/tmdb_movie_list.csv'
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

# Chargement des données
data = pd.read_csv('source/tmdb_movie_list.CSV')

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
    st.image("https://raw.githubusercontent.com/Damdam86/Recommandation_film/main/images/etape1.png")
elif selection == "Etape 2":
    st.image("https://raw.githubusercontent.com/Damdam86/Recommandation_film/main/images/etape2.png")
    st.image("https://raw.githubusercontent.com/Damdam86/Recommandation_film/main/images/etape3.png")
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
        df = pd.read_csv(file)
        return df
    df = data
    all_widgets = sp.create_widgets(df)
    res = sp.filter_df(df, all_widgets)
    st.header("Result DataFrame")
    st.write(res)