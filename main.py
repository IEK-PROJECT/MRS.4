import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Movie:
    def __init__(self, title, genre, release_date, overview):
        self.title = title
        self.genre = ', '.join([g['name'] for g in genre])  # Λίστα ειδών σε string
        self.release_date = release_date
        self.overview = overview

class TMDbAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3/"

    def get_movie_data(self, movie_title):
        search_url = f"{self.base_url}search/movie?api_key={self.api_key}&query={movie_title}"
        response = requests.get(search_url)
        results = response.json().get('results')
        if results:
            for result in results:
                release_date = result.get('release_date', '')
                if release_date and "1911" <= release_date.split("-")[0] <= "2023":
                    movie_id = result['id']
                    movie_url = f"{self.base_url}movie/{movie_id}?api_key={self.api_key}"
                    movie_response = requests.get(movie_url)
                    movie_data = movie_response.json()
                    return Movie(movie_data['title'], movie_data['genres'], movie_data['release_date'], movie_data['overview'])
        return None


class MovieRecommender:
    def __init__(self, api_key):
        self.api_key = api_key
        self.tmdb_api = TMDbAPI(api_key)
        self.movies = []
        self.vectorizer = TfidfVectorizer()

    def fetch_movies(self, movie_titles):
        for title in movie_titles:
            movie = self.tmdb_api.get_movie_data(title)
            if movie:
                self.movies.append(movie)

    def fit(self):
        overviews = [movie.overview for movie in self.movies]
        self.tfidf_matrix = self.vectorizer.fit_transform(overviews)

    def recommend(self, input_movie_title):
        input_movie = self.tmdb_api.get_movie_data(input_movie_title)
        if not input_movie:
            return "Η ταινία δεν βρέθηκε."
        input_vec = self.vectorizer.transform([input_movie.overview])
        cosine_similarities = cosine_similarity(input_vec, self.tfidf_matrix).flatten()

        # Διαγνωστικές εκτυπώσεις
        print("Μέγεθος cosine_similarities:", len(cosine_similarities))
        print("Μέγεθος self.movies:", len(self.movies))
        print("Πρώτες τιμές cosine_similarities:", cosine_similarities[:5])

        # Ταξινόμηση βάσει σκορ
        similar_movies = sorted(zip(cosine_similarities, self.movies), key=lambda x: x[0], reverse=True)
        return similar_movies[1:6]

def main():
    api_key = "3ef749f8c526bc42fb7720f376d78327"  # Βάλτε το API κλειδί σας εδώ
    recommender = MovieRecommender(api_key)

    # Παραδείγματα τίτλων ταινιών για αρχική φόρτωση
    initial_movie_titles = ["Inception", "The Matrix", "Avatar", "Titanic", "Interstellar"]
    recommender.fetch_movies(initial_movie_titles)
    recommender.fit()

    while True:
        user_input = input("Εισάγετε τον τίτλο της ταινίας ή 'exit' για έξοδο: ")
        if user_input.lower() == 'exit':
            break

        recommended_movies = recommender.recommend(user_input)
        if isinstance(recommended_movies, str):
            print(recommended_movies)
        else:
            print("Προτεινόμενες ταινίες:")
            for score, movie in recommended_movies:
                print(f"{movie.title} (Score: {score})")

if __name__ == "__main__":
    main()
