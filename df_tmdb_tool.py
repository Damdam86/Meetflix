import pandas as pd
from typing import Optional, List, Union

all_genres = [
  {
    "id": 28,
    "name": "Action"
  },
  {
    "id": 12,
    "name": "Aventure"
  },
  {
    "id": 16,
    "name": "Animation"
  },
  {
    "id": 35,
    "name": "Comédie"
  },
  {
    "id": 80,
    "name": "Crime"
  },
  {
    "id": 99,
    "name": "Documentaire"
  },
  {
    "id": 18,
    "name": "Drame"
  },
  {
    "id": 10751,
    "name": "Familial"
  },
  {
    "id": 14,
    "name": "Fantastique"
  },
  {
    "id": 36,
    "name": "Histoire"
  },
  {
    "id": 27,
    "name": "Horreur"
  },
  {
    "id": 10402,
    "name": "Musique"
  },
  {
    "id": 9648,
    "name": "Mystère"
  },
  {
    "id": 10749,
    "name": "Romance"
  },
  {
    "id": 878,
    "name": "Science-Fiction"
  },
  {
    "id": 10770,
    "name": "Téléfilm"
  },
  {
    "id": 53,
    "name": "Thriller"
  },
  {
    "id": 10752,
    "name": "Guerre"
  },
  {
    "id": 37,
    "name": "Western"
  }
  ]

# Create the dataframe from CSV and apply eval() to convert ['genres'] ['origin_country'] and ['cast'] from string to list or dictionnary
def csv_to_df(csv_tmdb : str) -> pd.DataFrame: 
  df_tmdb = pd.read_csv(csv_tmdb)
  df_tmdb = eval_df(df_tmdb)
  return df_tmdb

# Convert ['genres'] ['origin_country'] and ['cast'] from string to list or dictionnary
def eval_df(df_tmdb : pd.DataFrame) -> pd.DataFrame:
  df_tmdb['genres'] = df_tmdb['genres'].apply(eval)
  df_tmdb['origin_country'] = df_tmdb['origin_country'].apply(eval)
  df_tmdb['cast'] = df_tmdb['cast'].apply(eval)
  return df_tmdb

# get the most older year from the column release_date
def get_most_older_year(df_tmdb : pd.DataFrame) -> int:
  df_tmdb['year'] = pd.to_datetime(df_tmdb['release_date']).dt.year
  return df_tmdb['year'].min()

# get the most recent year from the column release_date
def get_most_recent_year(df_tmdb : pd.DataFrame) -> int:
  df_tmdb['year'] = pd.to_datetime(df_tmdb['release_date']).dt.year
  return df_tmdb['year'].max()

# get the minimum vote average from the column vote_average
def get_min_vote_average(df_tmdb : pd.DataFrame) -> float:
  return df_tmdb['vote_average'].min()

# get the maximum vote average from the column vote_average
def get_max_vote_average(df_tmdb : pd.DataFrame) -> float:
  return df_tmdb['vote_average'].max()

# get the minimum vote count from the column vote_count
def get_min_vote_count(df_tmdb : pd.DataFrame) -> int:
  return df_tmdb['vote_count'].min()

# get the maximum vote count from the column vote_count
def get_max_vote_count(df_tmdb : pd.DataFrame) -> int:
  return df_tmdb['vote_count'].max()

# get the minimum runtime from the column runtime
def get_min_runtime(df_tmdb : pd.DataFrame) -> int:
  return df_tmdb['runtime'].min()

# get the maximum runtime from the column runtime
def get_max_runtime(df_tmdb : pd.DataFrame) -> int:
  return df_tmdb['runtime'].max()

# get all genre from the column name in all_genres
def get_all_genre_names():
  all_genres_list = []
  for genre in all_genres:
    all_genres_list.append(genre['name'])
  return all_genres_list

# return the genre id associated to the genre name given in parameter  
def return_genre_id(genre_name : str) -> int :
  for genre in all_genres:
    if genre['name'].lower() == genre_name.lower():
      return genre['id']
  raise ValueError("La valeur entré ne correspond à aucun genre")

# return the genre name associated to the genre id given in parameter           
def return_genre_name(genre_id : int) -> str :
  for genre in all_genres:
    if genre['id'] == genre_id:
      return genre['name']
  raise ValueError("La valeur entré ne correspond à aucun genre")

# verify if the genre id given in parameter exist  
def verify_if_genre_id_exist(genre_id : int) -> bool :
  for genre in all_genres:
    if genre['id'] == genre_id:
      return True
  return False

# return a dataframe of movie that contain the genres given in parameter  
def get_df_with_genres(df_tmdb : pd.DataFrame, genres : List[Union[int, str]]) -> pd.DataFrame : 
  genre_ids = set()
  for genre in genres:
    if isinstance(genre, str):
      genre_id = return_genre_id(genre)
      genre_ids.add(genre_id)
    elif isinstance(genre, int):
      if verify_if_genre_id_exist(genre):
        genre_ids.add(genre)
    else:
      raise ValueError("La valeur entré n'est ni un int ni un str")
  return df_tmdb[df_tmdb['genres'].apply(lambda x: any(g['id'] in genre_ids for g in x))]

# return a dataframe of movies that contain the origin countries given in parameter 
def get_df_with_origin_country(df_tmdb : pd.DataFrame, origin_country : List[str]) -> pd.DataFrame : 
    country_set = set(c.upper() for c in origin_country)
    return df_tmdb[df_tmdb['origin_country'].apply(lambda x: any(c in country_set for c in x))]
    
# return a dataframe of movies using the filters given in parameter     
def get_filtered_df(df_tmdb : pd.DataFrame, 
                    genres : Optional[List[Union[int, str]]] = [], 
                    origin_country : Optional[List[str]]  = None, 
                    status : Optional[str] = None,
                    min_year : Optional[int] = None, 
                    max_year : Optional[int] = None, 
                    min_vote_average : Optional[float] = None, 
                    max_vote_average : Optional[float] = None, 
                    min_vote_count : Optional[int] = None, 
                    max_vote_count : Optional[int] = None, 
                    min_runtime : Optional[int] = None,
                    max_runtime : Optional[int] = None
                    ) -> pd.DataFrame:
  
  df_tmdb['release_date'] = pd.to_datetime(df_tmdb['release_date'], errors='coerce')
  df_tmdb['release_year'] = df_tmdb['release_date'].dt.year
  if len(genres) > 0:
    df_tmdb = get_df_with_genres(df_tmdb, genres)

  if origin_country != None:
    df_tmdb = get_df_with_origin_country(df_tmdb, origin_country)

  if status != None:
    df_tmdb = df_tmdb[df_tmdb["status"] == status]

  if min_year != None:
    df_tmdb = df_tmdb[df_tmdb['release_year'] >= min_year]
  
  if max_year != None:
    df_tmdb = df_tmdb[df_tmdb['release_year'] <= max_year]

  if min_vote_average != None:
    df_tmdb = df_tmdb[df_tmdb["vote_average"] >= min_vote_average]
  
  if max_vote_average != None:
    df_tmdb = df_tmdb[df_tmdb["vote_average"] <= max_vote_average]

  if min_vote_count != None:
    df_tmdb = df_tmdb[df_tmdb["vote_count"] >= min_vote_count]

  if max_vote_count != None:
    df_tmdb = df_tmdb[df_tmdb["vote_count"] <= max_vote_count]

  if min_runtime != None:
    df_tmdb = df_tmdb[df_tmdb["runtime"] >= min_runtime]

  if max_runtime != None:
    df_tmdb = df_tmdb[df_tmdb["runtime"] <= max_runtime]

  return df_tmdb

# divide the movie dataframe df_tmdb into nb_movies_by_page pages
def create_movie_pages(df_tmdb : pd.DataFrame, nb_movies_by_page : int) -> list[pd.DataFrame] :
  pages = []
  
  for start_index in range(0, len(df_tmdb), nb_movies_by_page):
    end_index = start_index + nb_movies_by_page
    
    page = df_tmdb.iloc[start_index:end_index]

    pages.append(page)
    
  return pages

# return a movie dataframe using the movie id
def get_movie_with_id(df_tmdb : pd.DataFrame, movie_id : int) -> dict :
  film = df_tmdb[df_tmdb["id"] == movie_id]
  film_dict = film.to_dict('records')[0] if not film.empty else None
  return film_dict

# return a person dict using the person id
def get_person_with_id(df_tmdb : pd.DataFrame, person_id : int) -> dict :
  for _, movie in df_tmdb.iterrows():
    for person in movie['cast']:
      if person['id'] == person_id:
        return person

# return a dataframe of all the movie where a person appear in
def get_movies_with_person_id(df_tmdb : pd.DataFrame, person_id : int) -> pd.DataFrame :
  df_movie = pd.DataFrame
  person = get_person_with_id(df_tmdb, person_id)
  cpt = 0
  for movie_id in person['known_for_titles']:
    if cpt == 0:
      df_movie = get_movie_with_id(df_tmdb, movie_id)
      cpt += 1
    else:
      df_movie = pd.concat([df_movie, get_movie_with_id(df_tmdb, movie_id)], ignore_index=True)
  
  return df_movie

# return a dict id : info of all the person in df_tmdb
def get_all_person_dict(df_tmdb : pd.DataFrame) -> dict :
  person_dico = {}

  for  _, movie in df_tmdb.iterrows():
    for person in movie['cast']:
      person_id = person['id']
      if person_id not in person_dico:
        person_dico[person_id] = person
  
  return person_dico
