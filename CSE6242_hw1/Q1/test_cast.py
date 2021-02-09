
from submission import * 

tm = TMDBAPIUtils(api_key='fa0b74631406cb7e556e50abc1edb711')

lf_best_movies = tm.get_movie_credits_for_person('2975', 8.0)

movie_ids = [lf_best_movies[i]['id'] for i in range(len(lf_best_movies))]

cast_lens = []

for id in movie_ids: 
	new_cast = tm.get_movie_cast(str(id), 3)
	print(new_cast)
	print('\n')

