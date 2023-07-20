import json
import requests
from moviweb_app.datamanager.data_management import DataManagerInterface

API_KEY = "81cc18ae"


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        # Return a list of all users
        with open(self.filename, "r") as file:
            users = json.load(file)
            return users

    def get_user_movies(self, user_id):
        # Return a list of all movies for a given user
        with open(self.filename, "r") as file:
            users = json.load(file)
            return [user["movies"] for user in users if user["id"] == user_id][0]

    def get_username_by_id(self, user_id):
        with open(self.filename, "r") as file:
            users = json.load(file)
            return [user["name"] for user in users if user["id"] == user_id][0]

    def get_movie_by_id(self, user_id, movie_id):
        users = self.get_all_users()
        for user in users:
            if user['id'] == user_id:
                for movie in user['movies']:
                    if movie['id'] == movie_id:
                        return movie

    def add_user(self, user_name):
        users = self.get_all_users()
        new_id = 1
        for user in users:
            if user['id'] == new_id:
                new_id += 1
            else:
                break
        new_user = {
            'id': new_id,
            'name': user_name,
            'movies': []
        }
        users.append(new_user)
        with open(self.filename, "w") as file:
            file.write(json.dumps(users))

    def add_movie(self, user_id, movie_name):
        users = self.get_all_users()

        try:
            res = requests.get(f"http://www.omdbapi.com/?apikey={API_KEY}&t={movie_name}")
        except Exception:
            print("Failed to connect to Movie API")
            return
        movie_info = res.json()
        new_id = 1
        for user in users:
            if user['id'] == user_id:
                for movie in user['movies']:
                    if movie['id'] == new_id:
                        new_id += 1
                    else:
                        break
                new_movie = {
                    'id': new_id,
                    'name': movie_info['Title'],
                    'director': movie_info['Director'],
                    'year': int(movie_info['Year']),
                    'rating': float(movie_info["imdbRating"])
                }
                user['movies'].append(new_movie)
                break

        with open(self.filename, "w") as file:
            file.write(json.dumps(users))

    def update_movie(self, user_id, movie_id, movie_name, movie_director, movie_year, movie_rating):
        users = self.get_all_users()

        for user in users:
            if user['id'] == user_id:
                for movie in user['movies']:
                    if movie['id'] == movie_id:
                        movie['name'] = movie_name
                        movie['director'] = movie_director
                        movie['year'] = movie_year
                        movie['rating'] = movie_rating
                        break
                break
        with open(self.filename, "w") as file:
            file.write(json.dumps(users))

    def delete_movie(self, user_id, movie_id):
        users = self.get_all_users()

        for user in users:
            if user['id'] == user_id:
                for movie in user['movies']:
                    if movie['id'] == movie_id:
                        user['movies'].remove(movie)
                        break
        with open(self.filename, "w") as file:
            file.write(json.dumps(users))