"""
Чтобы создать форму добавления новых рассказов в проект RandomStory, выполните
следующие задачи:

- Импортируйте необходимые классы для создания формы, полей и валидаторов.
- Опишите класс формы `StoryForm`, с помощью которого можно будет создавать
  объекты модели `Story`.
- В форме реализуйте два поля ввода (`title` и `text`) и кнопку для отправки
  формы; на кнопке должна быть надпись «Опубликовать». Оба поля ввода должны
  быть обязательными для заполнения, а строка в поле `title` не должна быть
  длиннее 128 символов.
- Придумайте и добавьте секретный ключ в словарь `app.config` Flask-приложения.
- Допишите код функции `add_view()`. Она должна:
    - принимать POST-запрос с данными формы;
    - валидировать полученные данные;
    - в случае успешной валидации создавать и сохранять объект модели `Story`;
    - после сохранения нового объекта перенаправлять пользователя на страницу,
      отображающую все рассказы;
    - при получении GET-запроса передавать в шаблон *add.html* объект формы
      `StoryForm` под ключом `form`.
- Настройте вывод формы на страницу по адресу */add*. Шаблон этой страницы
  подготовлен в файле *add.html*, в нём есть и код формы.
"""

from random import randint
from secrets import token_hex

from flask import Flask, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SECRET_KEY"] = token_hex(32)
db = SQLAlchemy(app)


class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, nullable=False)


class StoryForm(FlaskForm):
    title = StringField(
        "Заголовок", validators=[DataRequired(), Length(min=1, max=128)]
    )
    text = TextAreaField("Текст", validators=[DataRequired()])
    submit = SubmitField("Опубликовать")


@app.route("/")
def index_view():
    stories = Story.query.all()
    return render_template("stories.html", stories=stories)


@app.route("/add", methods=["GET", "POST"])
def add_view():
    form = StoryForm()
    if form.validate_on_submit():
        story = Story(title=form.title.data, text=form.text.data)
        db.session.add(story)
        db.session.commit()
        return redirect(url_for("index_view"))

    return render_template("add.html", form=form)


@app.route("/story")
def random_story_view():
    stories_count = Story.query.count()
    random_story = Story.query.get_or_404(randint(1, stories_count))
    return render_template("random.html", story=random_story)
