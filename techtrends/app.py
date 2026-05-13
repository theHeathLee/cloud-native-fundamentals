import os
import sqlite3
import logging
import sys
from flask import Flask, jsonify, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']

connection_count = 0


def db_connect():
    global connection_count
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    connection_count += 1
    return conn


def fetch_post(post_id):
    conn = db_connect()
    article = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return article


@app.route('/')
def index():
    conn = db_connect()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    article = fetch_post(post_id)
    if article is None:
        app.logger.error('A non-existing article was accessed. ID: {}'.format(post_id))
        return render_template('404.html'), 404
    app.logger.info('Article "{}" retrieved!'.format(article['title']))
    return render_template('post.html', post=article)


@app.route('/about')
def about():
    app.logger.info('"About Us" page retrieved!')
    return render_template('about.html')


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('A title is required to submit a post!')
        else:
            conn = db_connect()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            app.logger.info('New article created with title: "{}"'.format(title))
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/healthz')
def healthz():
    return jsonify(result='OK - healthy'), 200


@app.route('/metrics')
def metrics():
    conn = db_connect()
    total_posts = conn.execute('SELECT COUNT(*) FROM posts').fetchone()[0]
    conn.close()
    return jsonify(db_connection_count=connection_count, post_count=total_posts), 200


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s:%(name)s:%(asctime)s, %(message)s',
        datefmt='%m/%d/%Y, %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.StreamHandler(sys.stderr),
        ]
    )
    app.run(host='0.0.0.0', port='3111')
