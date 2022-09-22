import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
dbcount = 0
# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global dbcount
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    dbcount = dbcount + 1
    return connection


# Function to get post count
def get_post_count():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM posts')
    count = len(cursor.fetchall())
    connection.close()
    return count


# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      print('Post with id:"' + str(post_id) + '" not found') 
      return render_template('404.html'), 404
    else:
      print('Article "' + post['title'] + '" retrieved') 
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    print('About page retrieved') 
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            print('Article "' + title + '" created') 
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/healthz')
def healthz():
    result = {}
    result['result'] = 'OK-Healthy'
    return json.dumps(result)

@app.route('/metrics')
def metrics():
    global dbcount
    post_count = get_post_count()
    data = {}
    data['db_connection_count'] = dbcount
    data['post_count'] = post_count
    return json.dumps(data)


# start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')
