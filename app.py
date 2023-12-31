import os
from flask import Flask, render_template, url_for, flash, redirect, request
from sqlalchemy.orm import Session
from sqlalchemy import select
from model import User, Post, Tag, db 
from flask_migrate import Migrate
from forms import LoginForm, RegistrationForm
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
# from werkzeug.urls import url_parse
import config


app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLITE_URL
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'blahblahqwerty1234'
db.init_app(app)
migrate = Migrate(app, db)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/")
# @login_required
def index():
    with Session(config.engine) as session:
        all_posts = session.scalars(select(Post)).all()

    return render_template('index.html', posts=all_posts)

@app.route('/post/<int:post_id>')
@login_required
def post(post_id):
    print(f'>>> REQUEST: {request}')
    print(f'Post_id = {post_id}')
    with Session(config.engine) as session:
        single_post = session.query(Post).get(post_id)

    return render_template('post.html', post=single_post) 


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
        # next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('index')
        # return redirect(next_page)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.cli.command('create_db')
def init_db():
    # db.metadata.create_all(config.engine)
    db.metadata.create_all(config.engine_postgres)


@app.cli.command('drop_db')
def init_db():
    # db.metadata.drop_all(config.engine)
    db.metadata.drop_all(config.engine_postgres)


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
    # with Session(config.engine) as session:
    with Session(config.engine_postgres) as session:
        # creating and commiting users

        user1 = create_user(session, 'AmazingSam', 'sam@infobox.co')
        user1.set_password('qwer123')
        user2 = create_user(session, 'ValueableJohn', 'john@infobox.co')
        user2.set_password('qwer124')
        user3 = create_user(session, 'CuriousDave', 'dave@infobox.co')
        user3.set_password('qwer125')
        user4 = create_user(session, 'JellySally', 'sally@infobox.co')
        user4.set_password('qwer126')
        user5 = create_user(session, 'IncredibleLarry', 'larry@infobox.co')
        user5.set_password('qwer127')

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
