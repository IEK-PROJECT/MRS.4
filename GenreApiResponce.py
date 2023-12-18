import requests

class TMDbAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3/"

    def get_movie_genres(self):
        url = f"{self.base_url}genre/movie/list?api_key={self.api_key}&language=en-US"
        response = requests.get(url)
        genres_data = response.json()
        return [genre['name'] for genre in genres_data['genres']]

def main():
    api_key = "3ef749f8c526bc42fb7720f376d78327"  # Βάλτε το API κλειδί σας εδώ
    tmdb_api = TMDbAPI(api_key)
    
    movie_genres = tmdb_api.get_movie_genres()
    print("Είδη Ταινιών:")
    for genre in movie_genres:
        print(genre)

if __name__ == "__main__":
    main()
