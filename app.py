from flask import Flask, render_template, request
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import User, Post, Tag, db 
from flask_migrate import Migrate

import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLITE_URL
db.init_app(app)
migrate = Migrate(app, db)


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

@app.cli.command('create_db')
def init_db():
    db.metadata.create_all(config.engine)


@app.cli.command('drop_db')
def init_db():
    db.metadata.drop_all(config.engine)


def create_user(session: Session, username: str, email: str) -> User:
    user = User(username=username,
                email=email)
    session.add(user)
    session.commit()

    return user


def create_post_with_tags(session: Session, post: Post, *tags) -> None:
    for tag in tags:
        post.tags.append(tag)

    for tag in tags:
        session.add(tag)

    session.add(post)
    session.commit()


@app.cli.command('fill_db')
def fill_db():
    with Session(config.engine) as session:
        # creating and commiting users

        user1 = create_user(session, 'AmazingSam', 'sam@infobox.co')
        user2 = create_user(session, 'ValueableJohn', 'john@infobox.co')
        user3 = create_user(session, 'CuriousDave', 'dave@infobox.co')
        user4 = create_user(session, 'JellySally', 'sally@infobox.co')
        user5 = create_user(session, 'IncredibleLarry', 'larry@infobox.co')

        # creating tags

        tag1 = Tag(title='genres history',
                   name='История жанров')

        tag2 = Tag(title='why is this so',
                   name='Почему это так')

        tag3 = Tag(title='interesting',
                   name='Интересное')

        tag4 = Tag(title='music theory',
                   name='Музыкальная теория')

        # creating posts

        post1 = Post(title='Истоки джаза',
                     content='Истоки джазаИстоки джазаИстоки джаза',
                     user=user1.id)

        post2 = Post(title='Почему у гитары шесть струн?',
                     content='Почему у гитары шесть струнПочему у гитары шесть струн',
                     user=user1.id)

        post3 = Post(title='Сколько нот на самом деле?',
                     content='Сколько нот на самом делеСколько нот на самом деле',
                     user=user2.id)

        post4 = Post(title='О NWOBHM',
                     content='О NWOBHMО NWOBHMО NWOBHM',
                     user=user2.id)

        post5 = Post(title='Как появился панк рок',
                     content='Как появился панк рокКак появился панк рок',
                     user=user3.id)

        post6 = Post(title='Как появился хард рок',
                     content='Как появился хард рокКак появился хард рок',
                     user=user3.id)

        post7 = Post(title='Классические рок баллады',
                     content='Классические рок балладыКлассические рок баллады',
                     user=user4.id)

        post8 = Post(title='Подробно об музыкальных интервалах',
                     content='Подробно об музыкальных интервалах',
                     user=user4.id)

        post9 = Post(title='Кварто-квинтовый круг для чайников',
                     content='Кварто-квинтовый круг для чайников',
                     user=user5.id)

        post10 = Post(title='Основы теории музыки',
                      content='Основы теории музыкиОсновы теории музыки',
                      user=user5.id)

        # commiting posts with tags

        create_post_with_tags(session, post1, tag1)
        create_post_with_tags(session, post2, tag2)
        create_post_with_tags(session, post3, tag2)
        create_post_with_tags(session, post4, tag1)
        create_post_with_tags(session, post5, tag1)
        create_post_with_tags(session, post6, tag1)
        create_post_with_tags(session, post7, tag3)
        create_post_with_tags(session, post8, tag4)
        create_post_with_tags(session, post9, tag4)
        create_post_with_tags(session, post10, tag4)


if __name__ == '__main__':
    app.run(debug=True)
