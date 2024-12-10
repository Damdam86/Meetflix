import streamlit as st
import streamlit_antd_components as sac

# CSS personnalisé
css = """
<style>
}
.banner {
    position: relative;
    background-color: #333333;
    height: 60vh;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--secondary-color);
    text-align: center;
    margin-top: 60px;
}
.banner h1 {
    font-size: 48px;
}
.banner .buttons {
    margin-top: 20px;
}
.banner .buttons button {
    background-color: var(--primary-color);
    color: var(--secondary-color);
    border: none;
    padding: 10px 20px;
    border-radius: var(--border-radius);
    margin: 0 10px;
    cursor: pointer;
    transition: transform var(--transition-speed);
}
</style>
"""

# Insertion du CSS dans la page Streamlit
st.markdown(css, unsafe_allow_html=True)

# Header
st.markdown("""
<header>
    <div class="logo">YVDF Recommandation</div>
    <nav>
        <a href="#">Movies</a>
        <a href="#">TV Shows</a>
        <a href="#">People</a>
        <a href="#">More</a>
    </nav>
</header>
""", unsafe_allow_html=True)

# Banner
st.markdown("""
<div class="banner">
    <div class="content">
        <h1>Quoi regarder ce soir ?</h1>
        <div class="buttons">
            <button>Sélection à partir de votre film favoris</button>
            <button>Sélection à partir d'un petit questionnaire</button>
        </div>
    </div>
</div>
            <br>
            <br>
""", unsafe_allow_html=True)



sac.steps(
    items=[
        sac.StepsItem(title='Etape 1', description="Tester notre système de recommandation à partir d'un film ou d'un questionnaire"),
        sac.StepsItem(title='Etape 2', description="Laissez l'algorythme travailler"),
        sac.StepsItem(title='Etape 3', description="Un peu de popcorn et c'est parti pour une soirée film"),
    ], 
)

# Main content
st.markdown("""
<div class="main-content">
    <div class="card">
        <img src="https://www.themoviedb.org/t/p/original/movie-poster.jpg" alt="Movie Poster">
        <div class="info">
            <h3>Movie Title</h3>
            <p>Rating: 8.5/10</p>
        </div>
    </div>
    <div class="card">
        <img src="https://www.themoviedb.org/t/p/original/movie-poster.jpg" alt="Movie Poster">
        <div class="info">
            <h3>Movie Title</h3>
            <p>Rating: 7.9/10</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<footer>
    <p>&copy; 2024 YVDF. All rights reserved.</p>
</footer>
""", unsafe_allow_html=True)
