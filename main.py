from flask import Flask, render_template, request
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.model import Post

import config

app = Flask(__name__)


@app.route("/")
def index():
    with Session(config.engine) as session:
        all_posts = session.scalars(select(Post)).all()

    return render_template('index.html', posts=all_posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    print(f'Post_id = {post_id}')
    with Session(config.engine) as session:
        single_post = session.query(Post).get(post_id)

    return render_template('post.html', post=single_post) 

if __name__ == '__main__':
    app.run(debug=True)
