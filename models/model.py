# from sqlalchemy import (
#     Integer,
#     String,
#     ForeignKey,
#     Table,
#     Column
# )
#
# from sqlalchemy.orm import (
#     DeclarativeBase,
#     mapped_column,
#     relationship,
# )
# from config import engine
#
# class Base(DeclarativeBase):
#     pass
#
#
# class User(Base):
#     __tablename__ = 'user'
#     id = mapped_column(Integer, primary_key=True, autoincrement=True)
#     username = mapped_column(String, nullable=False)
#     email = mapped_column(String, nullable=False)
#
#     def __repr__(self) -> str:
#         return f'{self.username} {self.email}'
#
#
# post_tag_table = Table(
#     'post_tag_table',
#     Base.metadata,
#     Column('post_id', ForeignKey('post.id')),
#     Column('tag_id', ForeignKey('tag.id'))
# )
#
#
# class Post(Base):
#     __tablename__ = 'post'
#     id = mapped_column(Integer, primary_key=True, autoincrement=True)
#     title = mapped_column(String, nullable=False)
#     content = mapped_column(String, nullable=False)
#     user = mapped_column(Integer, ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
#     tags = relationship("Tag", secondary=post_tag_table, backref='posts')
#
#     def __repr__(self) -> str:
#         return f'Title: {self.title}, content: {self.content}'
#
#
# class Tag(Base):
#     __tablename__ = 'tag'
#     id = mapped_column(Integer, primary_key=True, autoincrement=True)
#     title = mapped_column(String, nullable=False)
#     name = mapped_column(String, nullable=False)
#
#     def __repr__(self) -> str:
#         return f'{self.title}'

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from config import engine
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f'{self.username} {self.email}'


post_tag_table = db.Table(
    'post_tag_table',
    db.Model.metadata,
    db.Column('post_id', db.ForeignKey('post.id')),
    db.Column('tag_id', db.ForeignKey('tag.id'))
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    tags = db.relationship("Tag", secondary=post_tag_table, backref='posts')

    def __repr__(self) -> str:
        return f'Title: {self.title}, content: {self.content}'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f'{self.title}'


# Populating database

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


def first_db_init() -> None:
    with Session(engine) as session:
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


def main():
    # db.metadata.create_all(bind=engine)
    # Base.metadata.drop_all(bind=engine)
    # first_db_init()
    pass

if __name__ == "__main__":
    main()
