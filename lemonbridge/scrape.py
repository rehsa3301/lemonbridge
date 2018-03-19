# -*- coding: utf-8 -*-

from imdbpie import Imdb

IMDB_IMG_SUFFIX = 'UX182_CR0,0,182,268_AL_'


def get_movies(search_query):
    from main import session
    
    imdb = Imdb(session=session)
    results = imdb.search_for_title(search_query)[:4] # top 4 results

    movies = []
    for r in results:
        movie_id = r['imdb_id']

        try:
            movie = imdb.get_title(movie_id)
            title = movie['base']['title']
            year = movie['base']['year']
        except:
            continue

        try:
            poster = movie['base']['image']['url']
        except KeyError:
            poster = None

        if poster:
            poster = poster.rstrip('.jpg') + IMDB_IMG_SUFFIX + '.jpg'
        else:
            pass

        movies.append( {'title': title, 'year': year, 'poster': poster} )

    return movies


# goodreads
def get_books(search_query):
    pass


# AniDB
def get_anime(search_query):
    pass


def get_tv(search_query):
    pass