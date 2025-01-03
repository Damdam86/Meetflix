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
import ast
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json


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
        sac.StepsItem(title='Etape 4', description="Algorythmes de recommandation"),
        sac.StepsItem(title='Etape 5', description="La base de données finale"),
    ], 
)

# Affichage basé sur la sélection

#Etape 1
if selection == "Etape 1":
    st.markdown("<p>Pour mener à bien notre projet, nous disposions de plusieurs DataFrames issus d'IMDB ainsi que de la possibilité d'utiliser l'API TMDB</p>", unsafe_allow_html=True)
    st.markdown("<p>Nous avons commencé par analyser et nettoyer les différents DataFrames d'IMDB afin de déterminer comment les rassembler en un seul DataFrame.</p>", unsafe_allow_html=True)
    st.image("images/etape1.png")
    st.image("images/etape2.png")
    st.image("images/etape3.png")
    st.markdown("<p>Nous nous sommes rapidement rendu compte qu'il manquait plusieurs informations importantes dans les DataFrames d'IMDB, telles que les résumés des films et leurs images.</p>", unsafe_allow_html=True)
    st.markdown("<p>Nous avons donc décidé d'utiliser l'API TMDB, qui contenait les mêmes informations qu'IMDB, mais avec les données manquantes en supplément.</p>", unsafe_allow_html=True)
    
#Etape 2
elif selection == "Etape 2":
    st.markdown("<p>Pour construire notre DataFrame de films en utilisant l'API TMDB, nous avons appliqué des filtres précis afin de répondre aux attentes de notre public cible, composé principalement de personnes âgées de plus de 70 ans.</p>", unsafe_allow_html=True)
    st.markdown("<p>Voici les étapes détaillées de notre sélection :</p>", unsafe_allow_html=True)
    st.markdown("""
                <p><strong>Premièrement</strong>, nous avons utilisé la référence Discover de l'API TMDB pour rechercher et filtrer les films selon des critères précis.</p>
                <div style="margin-left: 40px;">   
                    <h2>Première sélection : les films classiques</h2>
                    <p>Nous avons filtré les films avec les critères suivants :</p>
                    <ul>
                        <li><strong>Date de sortie :</strong> entre le <code>1950-01-01</code> et le <code>2024-08-30</code></li>
                        <li><strong>Note moyenne :</strong> supérieure ou égale à <code>6</code></li>
                        <li><strong>Nombre de votes :</strong> supérieur ou égal à <code>1000</code> afin d'éviter les films ayant une bonne note, mais uniquement votés par un faible nombre de personnes, comme la famille ou des proches.</li>
                        <li><strong>Durée :</strong> entre <code>70</code> et <code>300</code> minutes pour inclure des films d'une durée comprise entre 1h10 (minimum) et 5h (maximum), en prenant en compte les versions longues comme les directors' cut.</li>
                    </ul>
                    <p>Ces critères nous permettent de sélectionner des films emblématiques comme <em>La Grande Vadrouille</em>, qui correspondent aux attentes de notre public cible, principalement composé de personnes de plus de 70 ans.</p>
                </div> 
                <div style="margin-left: 40px;"> 
                    <h2>Deuxième sélection : les sorties récentes</h2>
                    <p>Nous avons également effectué une deuxième sélection pour les films plus récents, sortis ces trois derniers mois, avec des critères adaptés :</p>
                    <ul>
                        <li><strong>Date de sortie :</strong> entre le <code>2024-09-01</code> et le <code>2024-11-30</code></li>
                        <li><strong>Note moyenne :</strong> supérieure ou égale à <code>6</code></li>
                        <li><strong>Nombre de votes :</strong> supérieur ou égal à <code>500</code> un seuil plus bas que pour les films classiques, car les sorties récentes, comme Gladiator 2, n'ont pas encore accumulé un grand nombre de votes malgré leur succès.</li>
                        <li><strong>Durée :</strong> entre <code>70</code> et <code>300</code> minutes</li>
                    </ul>
                    <p>Cette approche nous permet d'inclure des films populaires récents tout en filtrant rigoureusement la qualité et la représentativité des avis. Ainsi, nous disposons d'une sélection équilibrée entre classiques et nouveautés adaptées à notre public cible.</p>
                </div>  
                <p><strong>Deuxièmement</strong>, nous avons utilisé la référence <strong>Details</strong> de <strong>Movie</strong> pour récupérer des informations supplémentaires sur chaque film, telles que la durée exacte (runtime).</p>
                <p><strong>Troisièmement</strong>, nous avons récupéré la distribution (le cast) de chaque film grâce à la référence <strong>Credits</strong> de <strong>Movie</strong>, ce qui nous a permis d'obtenir la liste complète des acteurs et des membres de l'équipe associés à chaque œuvre.</p>
                <p><strong>Quatrièmement</strong>, nous avons récupéré des informations détaillées sur chaque personne du cast en utilisant la référence <strong>Details</strong> de <strong>Person</strong>. Cela nous a permis d'enrichir nos données avec des détails tels que la biographie, la date de naissance, ou encore la filmographie de chaque acteur et membre de l'équipe.</p>
                
                """, unsafe_allow_html=True)
    

#Etape 3
elif selection == "Etape 3":
    st.title("Statistique TMDB")
    tab1, tab2, tab3, tab4 = st.tabs(["Cinematic Overview", "Genres", "RunTime", "Cast & Crew"])
    with tab1:
        df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year
        yearly_movies = df['release_year'].value_counts().reset_index()
        yearly_movies.columns = ['Année', 'Nombre de films']
        yearly_movies = yearly_movies.sort_values('Année')

        fig2 = px.line(yearly_movies, x='Année', y='Nombre de films', title="Évolution des sorties de films par année")
        fig2.update_traces(line=dict(color='indigo'))
        fig2.update_layout(xaxis_title="Année", yaxis_title="Nombre de films", height=600, margin=dict(l=50, r=50, t=50, b=50))
        st.plotly_chart(fig2, use_container_width=True)

        #st.subheader("Nombre de films par pays d'origine (Top 5 + Autres)")

        df['origin_country'] = df['origin_country'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
        countries_expanded = df.explode('origin_country')
        country_counts = countries_expanded['origin_country'].value_counts().reset_index()
        country_counts.columns = ['country', 'count']

        top_5_countries = country_counts.head(5)
        autres_count = country_counts.iloc[5:]['count'].sum()
        autres_row = pd.DataFrame({'country': ['Autres'], 'count': [autres_count]})
        top_5_with_autres = pd.concat([top_5_countries, autres_row], ignore_index=True)

        custom_colors = px.colors.sequential.Plasma[:4] + ["#FFD700"]
        fig3 = px.pie(top_5_with_autres, values='count', names='country', title="Nombre de films par pays d'origine (Top 5 + Autres)", hole=0.4, color_discrete_sequence=custom_colors)
        fig3.update_traces(textposition='inside', textinfo='percent+label')

        st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        st.header("Genres")
        col1, col2 = st.columns(2)
        with col1:
             st.title('')
             df['genres'] = df['genres'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
             all_genres = df.explode('genres')
             all_genres['genre_name'] = all_genres['genres'].apply(lambda x: x['name'] if isinstance(x, dict) and 'name' in x else None)
             all_genres = all_genres.dropna(subset=['genre_name'])
             genre_counts = all_genres['genre_name'].value_counts().reset_index()
             genre_counts.columns = ['Genre', 'Count']
             fig1 = px.bar(
                    genre_counts,
                    x='Genre',
                    y='Count',
                    color='Count',
                    title="Distribution des Genres les Plus Fréquents",
                    labels={'Count': 'Nombre de films', 'Genre': 'Genre'},
                    color_continuous_scale='viridis'
        )
             fig1.update_layout(
                    xaxis_title="Genre",
                    yaxis_title="Nombre de films",
                    xaxis={'categoryorder': 'total descending'},  # Trier les genres par ordre décroissant de popularité
                    height=600,
                    width=1250,
                    margin=dict(l=50, r=50, t=50, b=150)
        )   
             st.plotly_chart(fig1, use_container_width=True)
        with col2:
             st.title('')
             # Assurez-vous que la colonne 'genres' est bien en liste de dictionnaires
             df['genres'] = df['genres'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

            # Étendre le DataFrame pour exploser les genres
             all_genres = df.explode('genres')

            # Extraire le nom du genre de chaque dictionnaire
             all_genres['genre_name'] = all_genres['genres'].apply(lambda x: x['name'] if isinstance(x, dict) and 'name' in x else None)

            # Supprimer les lignes sans genre valide
             all_genres = all_genres.dropna(subset=['genre_name'])

            # Grouper les votes par genre
             votes_by_genre = all_genres.groupby('genre_name', as_index=False)['vote_count'].sum()

            #   Grouper par genre et calculer la moyenne des notes (vote_average)
             average_votes_by_genre = all_genres.groupby('genre_name', as_index=False)['vote_average'].mean()

            # Créer un sous-graphe avec deux graphiques l'un en dessous de l'autre
             fig2 = make_subplots(
                rows=2, cols=1,  # Deux sous-graphes dans deux lignes
                subplot_titles=('Nombre de Votes par Genre', 'Moyenne des Notes par Genre')
            )

            # Créer un graphique pour les votes avec la palette 'Viridis'
             fig2.add_trace(
                go.Bar(
                    x=votes_by_genre['genre_name'],
                    y=votes_by_genre['vote_count'],
                    marker=dict(
                        color=votes_by_genre['vote_count'],  # Appliquer la couleur en fonction du nombre de votes
                        colorscale='Viridis',  # Palette de couleurs Viridis
                        showscale=True  # Afficher l'échelle de couleurs
                    ),
                    name="Nombre de votes"
                ),
                row=1, col=1
            )

            # Créer un graphique pour la moyenne des notes avec la palette 'Viridis'
             fig2.add_trace(
                go.Bar(
                    x=average_votes_by_genre['genre_name'],
                    y=average_votes_by_genre['vote_average'],
                    marker=dict(
                        color=average_votes_by_genre['vote_average'],  # Appliquer la couleur en fonction de la moyenne des notes
                        colorscale='Viridis',  # Palette de couleurs Viridis
                        showscale=True  # Afficher l'échelle de couleurs
                    ),
                    name="Moyenne des notes"
                ),
                row=2, col=1
            )

            # Mettre à jour la disposition du graphique
             fig2.update_layout(
                title="Répartition des Films par Genre",
                height=900,  # Augmenter la hauteur pour deux graphiques
                width=1250,
                showlegend=False,
                xaxis_title="Genre",
                yaxis_title="Nombre de votes",
                xaxis2_title="Genre",
                yaxis2_title="Moyenne des notes",
                xaxis={'categoryorder': 'total descending'},  # Trier les genres par ordre décroissant de popularité
                margin=dict(l=50, r=50, t=50, b=150),# Ajouter des marges pour une meilleure lisibilité
            )

            # Afficher le graphique
             st.plotly_chart(fig2, use_container_width=True)
  
    with tab3:
        st.header("Durée")
        col1, col2 = st.columns(2)
        with col1:          
            df_cleaned = df.dropna(subset=['runtime'])
            fig3 = make_subplots(
                rows=1, cols=2,
                subplot_titles=("Histogramme des Durées", "Boîte à Moustaches des Durées"),
                column_widths=[0.5, 0.5]  
        ) 
            fig3.add_trace(
                go.Histogram(
                x=df_cleaned['runtime'],
                nbinsx=30,
                name="Histogramme",
                marker_color='indigo'
            ),
            row=1, col=1
    )
# Ajouter la boîte à moustaches au sous-graphique 2
            fig3.add_trace(
                go.Box(
                y=df_cleaned['runtime'],
                name="distribution des durées des films",
                marker_color='indigo'
            ),
            row=1, col=2
    )
            fig3.update_yaxes(tickprefix='min ', row=1, col=2)

            fig3.update_layout(
            title="Distribution des Durées des Films",
            xaxis_title="Durée des films (minutes)",
            yaxis_title="Fréquence",
            showlegend=False,
            height=600
    )
            st.plotly_chart(fig3, use_container_width=True)

        with col2:
        
            top_10_longest = df[['title', 'runtime']].sort_values(by='runtime', ascending=False).head(10)
            top_10_shortest = df[['title', 'runtime']].sort_values(by='runtime').head(10)

# Bar chart : Films les plus longs
            fig4 = px.bar(top_10_longest, x='title', y='runtime',
                title="Top 10 des films les plus longs", labels={'title': 'Titre des films', 'runtime': 'Durée (min)'}, color_discrete_sequence=['indigo'])
            fig4.update_xaxes(tickangle=45)
            st.plotly_chart(fig4, use_container_width=True)

# Bar chart : Films les plus courts
            fig5 = px.bar(top_10_shortest, x='title', y='runtime',
              title="Top 10 des films les plus courts", labels={'title': 'Titre des films', 'runtime': 'Durée (min)'}, color_discrete_sequence=['yellow'])
            fig5.update_xaxes(tickangle=45)
            st.plotly_chart(fig5, use_container_width=True)

    with tab4:
        
        col1, col2 = st.columns(2)
        with col1:
            st.header("Cast")          
            def extract_names(column_data):
                try:
        # Essaie de convertir le texte en liste et de retourner les 5 premiers noms
                    actors_list = ast.literal_eval(column_data) if column_data else []
                    return [person['name'] for person in actors_list][:5]  # Limite aux 5 premiers noms
                except Exception as e:
                    print(f"Erreur lors de l'extraction des noms : {e}")
                    return []

#Application de la fonction sur la colonne 'cast' pour extraire les acteurs
            df['actors'] = df['cast'].apply(extract_names)

#Exploser la colonne 'actors' pour avoir une ligne par acteur
            data_actors = df.explode('actors')

#Compter la fréquence d'apparition des acteurs
            actor_counts = data_actors['actors'].value_counts()

            #Sélectionner les 50 acteurs les plus fréquents
            top_50_actors = actor_counts.head(50).index.tolist()

            #Filtrer les données pour ne conserver que les films des top 50 acteurs
            data_top_50_actors = data_actors[data_actors['actors'].isin(top_50_actors)]

            #Extraire l'année de la colonne 'release_date'
            data_top_50_actors['year'] = pd.to_datetime(data_top_50_actors['release_date']).dt.year

            #Créer un DataFrame pour compter le nombre de films par acteur et par année
            film_counts = data_top_50_actors.groupby(['actors', 'year']).size().reset_index(name='film_count')

            #Créer un histogramme du nombre de films par acteur par année
            fig1 = px.histogram(
                film_counts,
                x="year",  # L'année des films
                y="film_count",  # Nombre de films
                color="actors",  # Couleur par acteur
                animation_frame="actors",  # Animation par acteur
                title="Nombre de Films par Acteur par Année (Top 50)",
                labels={"year": "Année", "film_count": "Nombre de Films", "actors": "Acteurs"},
                nbins=20,  # Nombre de bins pour l'histogramme
                hover_data=["actors", "year", "film_count"]
)
#Afficher le graphique
            st.plotly_chart(fig1, use_container_width=True)

        with col2: 
            st.header(' Crew')   
            director_votes = df.explode('cast')

# Filtrer les lignes où 'cast' correspond à un directeur
            director_votes = director_votes[director_votes['cast'].apply(
                lambda x: isinstance(x, dict) and x.get('known_for_department') == 'Directing')]

# Extraire le nom du directeur
            director_votes['director_name'] = director_votes['cast'].apply(lambda x: x.get('name') if isinstance(x, dict) else None)

# Supprimer les lignes sans nom de directeur valide
            director_votes = director_votes.dropna(subset=['director_name'])

# Grouper par nom du directeur et calculer les statistiques
            director_stats = director_votes.groupby('director_name').agg({
                'vote_average': 'mean',
                'vote_count': 'sum',
                'original_title': 'count'
        }).reset_index()

# Renommer les colonnes pour plus de clarté
            director_stats.rename(columns={
                'original_title': 'film_count',
                'vote_average': 'average_rating',
                'vote_count': 'total_votes'
        }, inplace=True)

# Trier par le nombre de films
            director_stats = director_stats.sort_values(by='film_count', ascending=False)

# Visualisation des résultats
            import plotly.express as px

# Histogramme pour le nombre de films par directeur
            fig2 = px.bar(
            director_stats.head(10),  # Afficher les 10 meilleurs
            x='director_name',
            y='film_count',
            title="Top 10 des directeurs par nombre de films",
            labels={'film_count': 'Nombre de films', 'director_name': 'Directeur'},
            color='film_count',
            color_continuous_scale='Plasma'
    )
            st.plotly_chart(fig2, use_container_width=True)

# Diagramme pour la moyenne des votes par réalisateur
            fig3 = px.scatter(
            director_stats.head(10),
            x='director_name',
            y='average_rating',
            size='total_votes',
            title="Analyses de notes de top 10 directeurs(moyenne des notes vs total des votes)",
            labels={'average_rating': 'Moyenne des notes', 'total_votes': 'Total des votes', 'director_name': 'Directeur'},
            color='average_rating',
            color_continuous_scale='Plasma'
    )
            st.plotly_chart(fig3, use_container_width=True)


#Etape 4
elif selection == "Etape 4":
    st.title("Le système de recommandation")
    st.text("Nous avons fait le choix de partir sur plusieurs solutions de recommandation.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.title("KNN")
        st.text("Nous avons fait le choix de partir sur plusieurs solutions de recommandation.")
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
    with col2:
        st.title("BERT")
        st.text("Nous avons fait le choix de partir sur plusieurs solutions de recommandation.")

#Etape 5
elif selection == "Etape 5":
    st.header("Result DataFrame")
    def dict_list_to_str(lst):
        return [", ".join(f"{k}: {v}" for k, v in d.items()) for d in lst]
    
    df['genres'] = df['genres'].apply(dict_list_to_str)
    df['cast'] = df['cast'].apply(dict_list_to_str)
    st.dataframe(df)