from flask import Flask, render_template, request, redirect, url_for
from datamanager.json_data_manager import JSONDataManager
import os
import random

app = Flask(__name__)
data_manager = JSONDataManager('example.json')


@app.route('/')
def home():
    # Get a list of all files in the "images" folder
    images_folder = os.path.join(app.static_folder, 'images')
    image_files = [f for f in os.listdir(images_folder) if os.path.isfile(os.path.join(images_folder, f))]

    # Select a random image filename
    random_image_filename = random.choice(image_files)
    users = data_manager.get_all_users()
    return render_template('index.html', users=users, random_image=random_image_filename)


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def list_user_movies(user_id):
    username = data_manager.get_username_by_id(user_id)
    movies = data_manager.get_user_movies(user_id)
    try:
        return render_template("movies.html", movies=movies, username=username, user_id=user_id)
    except TypeError:
        error_message = "No user with provided ID"
        return render_template("500.html", error_message=error_message)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_name = request.form['user_name']
        if user_name == "":
            error_message = "No name entered"
            return render_template("500.html", error_message=error_message)
        data_manager.add_user(user_name)
        return redirect(url_for('home'))
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        if movie_name == "":
            error_message = "No title entered"
            return render_template("500.html", error_message=error_message)
        if data_manager.add_movie(user_id, movie_name):
            error_message = "Couldn't find movie"
            return render_template("500.html", error_message=error_message)
        return redirect(f'/users/{user_id}')
    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        movie_director = request.form['movie_director']
        movie_year = request.form['movie_year']
        movie_rating = request.form['movie_rating']

        data_manager.update_movie(user_id, movie_id, movie_name, movie_director, movie_year, movie_rating)
        return redirect(f'/users/{user_id}')
    movie = data_manager.get_movie_by_id(user_id, movie_id)
    return render_template('update_movie.html', user_id=user_id, movie_id=movie_id, movie=movie)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(user_id, movie_id)
    return redirect(f'/users/{user_id}')


if __name__ == '__main__':
    app.run(debug=True)
