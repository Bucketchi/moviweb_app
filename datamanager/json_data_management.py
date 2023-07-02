import json
from moviweb_app.datamanager.data_management import DataManagerInterface


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
