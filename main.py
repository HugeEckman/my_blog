from flask import Flask, render_template, request
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.model import User, Post, Tag

import config

app = Flask(__name__)


@app.route("/")
def index():
    with Session(config.engine) as session:
        all_posts = session.scalars(select(Post)).all()

    for item in all_posts:
        print(item)

    # print('REQUEST')
    # print(request)
    # print(request.headers)
    # print(request.args)
    # print(request.headers['user-agent'])
    return render_template('index.html', posts=all_posts)
    # return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run(debug=True)
