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

st.markdown(
    """
        <style>
            .center-image {
                display: flex;
                justify-content: center;
            }
        </style>
    """, unsafe_allow_html=True)

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
        sac.StepsItem(title='Etape 1', description="Etude de marché sur la consomation de cinéma dans la région de la Creuse"),
        sac.StepsItem(title='Etape 2', description="Etude, filtrage, fusion des données IMDB"),
        sac.StepsItem(title='Etape 3', description="Etude API TMDB, création de la nouvelle base"),
        sac.StepsItem(title='Etape 4', description="Statistiques TMDB"),
        sac.StepsItem(title='Etape 5', description="Algorithmes de recommandation - machine learning"),
        sac.StepsItem(title='Etape 6', description="La base de données finale"),
    ], 
)

# Affichage basé sur la sélection

#Etape 1
if selection == "Etape 1":
    st.markdown("<br><br><h1>C’est quoi ? C’est où la Creuse ?</h1><br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2, vertical_alignment="center")
    with col1:        
        st.markdown("""
            <p>Département (23) qui tire son nom de la rivière Creuse qui le traverse.</p>
            <p>Dans la région nouvelle Aquitaine. Au centre de la France.</p>
            <p>Second département français le moins peuplé avec <strong>115 702</strong> habitants en 2021.</p> 
            <p>Sa plus grande ville et sa préfecture est <strong>Guéret</strong>.</p>
            <p>L'économie de la Creuse repose traditionnellement sur <strong>deux secteurs</strong>:<br>
                    - l'agriculture (majoritairement l'élevage mais aussi la sylviculture);<br>
                    - l'artisanat (comme la tapisserie d'Aubusson).</p>
            <p>Depuis quelques années, <strong>le développement du tourisme vert</strong> rapproche celui-ci du niveau des départements limitrophes par la création de nombreuses structures d'accueil, chambres d'hôtes, gîtes ruraux.</p>
        """, unsafe_allow_html=True)
    with col2:
        #st.image("images/ecu_creuse.png")
        st.image("images/carte_france_creuse.png")

    st.markdown("<br><br><h1>La population</h1>", unsafe_allow_html=True)
    st.markdown("<p>Selon les estimations de l'INSEE au 1ᵉʳ janvier 2021, la Creuse, avec une population de 115 702 habitants, est le deuxième département le moins peuplé de France métropolitaine, juste après la Lozère.</p>", unsafe_allow_html=True)
    col3, col4 = st.columns(2, vertical_alignment="center")
    with col3: 
        st.markdown("""
            <p>En 2021, la population totale de la Creuse était de <strong>115 702</strong> habitants.</p> 

            <p>Parmi eux, <strong>69 661</strong> personnes étaient âgées de <strong>45 ans ou plus, ce qui représente environ <strong>60,2 %</strong> de la population totale.</p>

            <p>En moyenne, la population de la Creuse est répartie de manière <strong>équilibrée entre hommes et femmes</strong> dans chaque tranche d'âge.</p> 

            <p>Cependant, <strong>pour les 75 ans et plus</strong>, les femmes représentent une majorité significative, avec environ <strong>60 %</strong> de femmes.</p>
        """, unsafe_allow_html=True)
    with col4: 
        st.image("images/repart_pop_creuse.png")

    st.markdown("<br><p>Selon les estimations de l'INSEE au 1ᵉʳ janvier 2021, la Creuse, avec une population de 115 702 habitants, est le deuxième département le moins peuplé de France métropolitaine, juste après la Lozère.</p>", unsafe_allow_html=True)
    col5, col6 = st.columns(2, vertical_alignment="center")
    with col5: 
        st.markdown("""
            <p>Depuis 1968, la Creuse a connu une diminution significative de sa population, passant de <strong>156 876 habitants à 115 702 en 2021</strong>.</p> 

            <p>Cette tendance à la baisse reflète les défis démographiques auxquels le département est confronté, notamment l'exode rural et le vieillissement de la population.</p>

            <p>Ces facteurs peuvent influencer la fréquentation des cinémas locaux, avec une diminution potentielle du nombre de spectateurs.</p> 
        """, unsafe_allow_html=True)
    with col6: 
        st.image("images/evol_pop_creuse.png")

    st.markdown("<br><br><h1>Le cinéma - Données générales</h1>", unsafe_allow_html=True)
    st.markdown("<p>Les habitudes de fréquentation des salles de cinéma en France varient selon l'âge et le sexe. Selon une étude de l'INSEE en 2022, la proportion de personnes étant allées au cinéma au cours des douze derniers mois est la suivante :</p>", unsafe_allow_html=True)
    st.image("images/frequ_cinema.png")
    st.markdown("<p>Ces données indiquent que la fréquentation des salles de cinéma diminue avec l'âge pour les deux sexes, avec une proportion légèrement plus élevée de femmes n'allant pas au cinéma, notamment dans les tranches d'âge supérieures.</p>", unsafe_allow_html=True)
    st.markdown("<strong><p>Il est important de noter que ces statistiques sont nationales et peuvent varier localement, notamment dans des départements comme la Creuse, où la population est plus âgée et moins dense. Ces facteurs peuvent influencer la fréquentation des cinémas locaux.</p></strong><br>", unsafe_allow_html=True)
    col7, col8 = st.columns(2, vertical_alignment="center")
    with col7: 
        st.markdown("""
            <p>Les préférences cinématographiques varient selon l'âge et le sexe des spectateurs. Ces deux graphiques montrent les genres préférés au cinéma par les hommes et les femmes selon les tranches d'âge en France.</p> 

            <p><strong>Genre dominant par sexe :</strong> Les femmes préfèrent les comédies et les comédies romantiques, tandis que les hommes montrent une plus forte préférence pour les films d'action et les thrillers.</p>

            <p><strong>Variation avec l'âge :</strong> La popularité des genres évolue avec l'âge. Par exemple, les jeunes (18-24 ans) préfèrent les films fantastiques et d'action, tandis que les plus âgés (65 ans et plus) tendent à apprécier davantage les comédies et les films historiques.</p> 

            <p><strong>Genres stables et déclinants :</strong> La comédie reste un genre populaire dans toutes les tranches d'âge, mais les films de science-fiction et d'action sont plus appréciés par les jeunes, avec une baisse de popularité chez les spectateurs plus âgés.</p>
        """, unsafe_allow_html=True)
    with col8: 
        st.image("images/pref_genre.png")

    st.markdown("<br><br><h1>Le cinéma dans la Creuse </h1>", unsafe_allow_html=True)
    col9, col10 = st.columns(2, vertical_alignment="center")
    with col9: 
        data_cinema = {
            "Info 2023": [
                "Salles", "Fauteuils", "Entrées", "Recettes", 
                "Recettes moyennes / entrées", "Séances", 
                "Entrées par habitant en 2023", "Taux d'occupation des fauteuilles", 
                "PdM en entrées des films français (%)", "PdM en entrées des films américains (%)"
            ],
            "France": [
                "6 320", "1 160 000", "180,4M", "13 339M€", 
                "7,39", "8 300 000", "2,71", "12,40%", 
                "40,00%", "42,00%"
            ],
            "Creuse": [
                "7", "2 150", "1,4M", "9,3M€", 
                "6,76", "72 617", "2,47", "11,40%", 
                "50,10%", "34,20%"
            ]
        }

        df_cinema = pd.DataFrame(data_cinema)
        st.dataframe(df_cinema)

    with col10: 
        st.markdown("""
            <p>Le département de la Creuse est un des département les moins bien équipé en salle de France. Il possède cependant une des population les plus faibles de france. Ce que l’on peut noter des données du CNC :</p> 

            <p>     - Il n’y a pas de multiplex (Pathé, Gaumont etc.).</p>

            <p>     - Les recettes sont plus faibles que la moyenne nationale et le taux d’occupation légèrement plus faible également.</p> 

            <p>     - On peut également noter que la répartition films français / américains est nettement différente qu’au niveau national (8% de moins pour les films américains et 10% de plus pour les films français).</p>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    col11, col12, col13 = st.columns(3)
    with col11:
        st.image("images/evol_idf_creuse.png")
    with col12:
        st.image("images/evol_recette.png")
    with col13:
        st.image("images/evol_taux_occup.png")
    
    st.markdown("""
        <p>D'après les données du CNC sur les fréquentations, recette et taux d’occupation des départements, la Creuse, malgré son faible niveau de service dans les ICC (Industrie Culturelles et Créatives), semble en évolution positive sur ces 3 critères.</p> 

        <p>Il faut cependant noter une chute importante de la fréquentation, des recettes et du taux d’occupation pendant la crise du COVID qui a pu mettre en difficulté votre établissement.</p>
        <br>
    """, unsafe_allow_html=True)
    # <p><strong>La baisse d’activité de votre cinéma ne semble donc pas lié à un désamour du cinéma part les Creusois.</strong></p> 

    st.image("images/swot.png")

    st.markdown("<br><br><h1>Nos conclusions</h1>", unsafe_allow_html=True)
    st.markdown("<p>Pour concevoir une application de recherche de films pour un cinéma en tenant compte des préférences démographiques et cinématographiques, voici la marche à suivre basée sur nos analyses et graphiques :</p>", unsafe_allow_html=True)
    col14, col15 = st.columns(2, vertical_alignment="center")
    with col14: 
        st.markdown("""
            <p><strong>1. Segmenter les utilisateurs par âge et sexe</strong></p> 
            <p>L’application pourrait <strong>demander l’âge et le sexe des utilisateurs</strong> dès l’inscription, ou les recueillir de façon optionnelle <strong>pour proposer une sélection de films personnalisée.</strong></p>
            <br>
            <p><strong>2. Personnalisation des recommandations</strong></p> 
            <p>     - <strong>Jeunes utilisateurs (18-34 ans) : Mettre en avant des films d’action, fantastiques et comédies romantiques.</strong> Ces genres sont particulièrement populaires dans ce segment.</p>
            <p>     - <strong>Public plus âgé (35 ans et plus) : Proposer davantage de comédies et de films historiques</strong>, genres majoritairement appréciés par les 50 ans et plus, avec <strong>un accent particulier sur les films d’auteur et les drames</strong> pour les seniors. Nous ferons également <strong>un focus sur les films français</strong> (au regard des informations collectés lors de l’étude de marché).</p>

        """, unsafe_allow_html=True)
    with col15: 
        st.markdown("""
            <p><strong>3. Filtrage et recherche avancée</strong></p> 
            <p>Intégrer un <strong>système de filtres permettant aux utilisateurs de rechercher des films par genre</strong> (action, comédie, drame, etc.) et éventuellement par sous-genre.</p>
            <br>
            <p><strong>4. Feedback et interaction utilisateur</strong></p> 
            <p>     - Permettre aux utilisateurs de <strong>noter et de commenter les films, afin d’optimiser les recommandations basées sur les préférences locales et les tendances du public.</strong></p>
            <p>     - <strong>Recueillir des données d’utilisation pour affiner les propositions</strong> et améliorer l’application.</p>
            <p>     - Diffuser des <strong>notifications pour des sorties de films correspondant aux préférences des utilisateurs</strong>, augmentant ainsi l’engagement et la fréquentation.</p>
            <p>     - <strong>Affichers les films les plus votés, pourrait vous permettre de proposer des rediffusions de ces films</strong> à intervalles réguliers.</p>

        """, unsafe_allow_html=True)

#Etape 2
if selection == "Etape 2":
    st.markdown("<p>Pour mener à bien notre projet, nous disposions de plusieurs DataFrames issus d'IMDB ainsi que de la possibilité d'utiliser l'API TMDB</p>", unsafe_allow_html=True)
    st.markdown("<p>Nous avons commencé par analyser et nettoyer les différents DataFrames d'IMDB afin de déterminer comment les rassembler en un seul DataFrame.</p>", unsafe_allow_html=True)
    st.image("images/etape1.png")
    st.image("images/etape2.png")
    st.image("images/etape3.png")
    st.markdown("<p>Nous nous sommes rapidement rendu compte qu'il manquait plusieurs informations importantes dans les DataFrames d'IMDB, telles que les résumés des films et leurs images.</p>", unsafe_allow_html=True)
    st.markdown("<p>Nous avons donc décidé d'utiliser l'API TMDB, qui contenait les mêmes informations qu'IMDB, mais avec les données manquantes en supplément.</p>", unsafe_allow_html=True)
    
#Etape 3
elif selection == "Etape 3":
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
                <p><strong>Résultat : Le nombre de films dans la base est de 3 672.</strong>
                """, unsafe_allow_html=True)
    

#Etape 4
elif selection == "Etape 4":
    st.title("Statistiques TMDB")
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

        # Afficher le heatmap
        #st.markdown("<p style='font-size:10px;'>Top 10 des acteurs les mieux notés avec au moins 10 films</p>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.image("images/Heatmap.png")
       # st.image("images/Heatmap.png")

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
        
        #col1, col2 = st.columns(2)
        #with col1:
            st.header("Cast")          
            st.image("images/Top 10 Acteurs.png")

        #with col2: 
            st.header(' Crew')   
            director_votes = df.explode('cast')
            director_votes = director_votes[director_votes['cast'].apply(
                lambda x: isinstance(x, dict) and x.get('known_for_department') == 'Directing')]

            director_votes['director_name'] = director_votes['cast'].apply(lambda x: x.get('name') if isinstance(x, dict) else None)


            director_votes = director_votes.dropna(subset=['director_name'])


            director_stats = director_votes.groupby('director_name').agg({
                'vote_average': 'mean',
                'vote_count': 'sum',
                'original_title': 'count'
        }).reset_index()


            director_stats.rename(columns={
                'original_title': 'film_count',
                'vote_average': 'average_rating',
                'vote_count': 'total_votes'
        }, inplace=True)


            director_stats = director_stats.sort_values(by='film_count', ascending=False)
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


#Etape 5
elif selection == "Etape 5":
    st.title("Le système de recommandation")
    st.image('images/KNN.png')
    
    col1, col2 = st.columns(2)
    with col1:
        st.title("KNN")
        st.write("""
        Notre approche KNN s'appuie sur des données diverses pour trouver les films les plus similaires selon plusieurs critères :  
        - **Données numériques TMDB utilisées** : Utilisation de la popularité des films avec application d'un scaler `StandardScaler`.
        - **Données non numériques TMDB utilisées** : Conversion de tous les genres + les acteurs principaux (5 premiers) en variables numériques via `get_dummies`.  
        - **Données non numériques autres utilisées** : Ajout des 3 mots-clés par film créer à partir de l'API OpenAI. Ses mots clés sont ensuites convertis en variable numérique avec `get_dummies`. 
        - **Distance :** Choix de la distance de Minkowski avec un paramètre `n_neighbors = 26`.  
        """)

    with col2:
        st.title("Génération de mots-clés")
        st.text("Exploitation de l'API OpenAI pour enrichir les données de contenu.")
        st.write(
            """
            - **Principe :** Analyse des synopsis de plus de 4000 films pour générer des mots-clés représentatifs.  
            - **Utilisation :** Ces mots-clés sont utilisés pour améliorer la précision des recommandations basées sur le contenu.
            - **Model utilisé** : gpt-4-turbo-preview
            - **Prompt utilisé :** f"Basé sur le synopsis suivant du film '{movie_title}', donne-moi 3 mots-clés pertinents :{movie_overview}. Utilise des mots-clés simples (1 mot) qui résument bien le film. L'objectif est d'avoir des mots-clés pertinents afin de pouvoir entraîner un modèle de machine learning et ainsi faire des suggestions de films."
            """
        )

#Etape 6
elif selection == "Etape 6":
    st.header("Result DataFrame")
    def dict_list_to_str(lst):
        return [", ".join(f"{k}: {v}" for k, v in d.items()) for d in lst]
    
    df['genres'] = df['genres'].apply(dict_list_to_str)
    df['cast'] = df['cast'].apply(dict_list_to_str)
    st.dataframe(df)