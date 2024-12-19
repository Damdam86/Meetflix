import df_tmdb_tool as dtt

# Charger les données globales
df_tmdb = dtt.csv_to_df('https://sevlacgames.com/tmdb/new_tmdb_movie_list2.csv')
person_dico = dtt.get_all_person_dict(df_tmdb)