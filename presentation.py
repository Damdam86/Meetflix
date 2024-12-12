import streamlit as st

st.set_page_config(
    page_title="Recommandation de Film",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Définir les pages pour la navigation
pages = [
    st.Page("page2.py", title="Le projet", icon="🔥"),
    st.Page("page1.py", title="L'équipe", icon="🤹‍♀️"),
    st.Page("page3.py", title="Analyse", icon="📊"),
    st.Page("page8.py", title="Recommandation", icon="🏠"),
    st.Page("page6.py", title="Full movies", icon="🎬"),
    st.Page("page4.py", title="Best movies", icon="🎬"),
    st.Page("page5.py", title="Acteurs", icon="🎭"),
]

# Activer la navigation
pg = st.navigation(pages, position="sidebar", expanded=True)
pg.run()
