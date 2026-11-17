"""
Ваша задача — в проекте RandomStory создать модель и вывести объекты этой
модели на главную страницу.

В этой и во всех последующих задачах база данных проекта RandomStory уже
заполнена данными.

**Что и как нужно сделать**

Создайте модель `Story`: она будет описывать объект рассказа, опубликованного в
сервисе.

Поля модели:

- `id` — первичный ключ, целое число;
- `title` — название рассказа, строка с максимальной длиной 128 символов;
- `text` — текст рассказа, текстовое поле без ограничений по длине строки.

В функции `index_view()` получите из базы данных все объекты модели `Story` и
сохраните их в переменную `stories`.

Сформируйте и выведите на главную страницу список словарей со всеми рассказами,
где ключами будут `id` рассказов, а значениями — тексты рассказов из функции
`jsonify`.
"""

from flask import Flask, Response, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.json.ensure_ascii = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
db = SQLAlchemy(app)


class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, nullable=False)


@app.route("/")
def index_view() -> Response:
    stories = Story.query.all()
    return jsonify([{story.id: story.text} for story in stories])


@app.route("/add")
def add_view() -> str:
    return "Это страница для добавления рассказа"


@app.route("/story")
def random_story_view() -> str:
    return "Это страница со случайным рассказом"
