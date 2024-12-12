import streamlit as st

st.set_page_config(
    page_title="Recommandation de Film",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Définir les pages pour la navigation
pages = [
    st.Page("project.py", title="Le projet", icon="🔥"),
    st.Page("team.py", title="L'équipe", icon="🤹‍♀️"),
    st.Page("analyse.py", title="Analyse", icon="📊"),
    st.Page("reco.py", title="Recommandation", icon="🏠"),
    st.Page("search_movies.py", title="Full movies", icon="🎬"),
    st.Page("movie.py", title="Best movies", icon="🎬"),
    st.Page("actor.py", title="Acteurs", icon="🎭"),
]

# Activer la navigation
pg = st.navigation(pages, position="sidebar", expanded=True)
pg.run()
