import os
from flask import Flask, render_template, redirect, request, Response
from models import User, Education, Contact, db
from werkzeug.utils import secure_filename

secret_key = os.urandom(32)

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = secret_key

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

app = create_app()


@app.route("/create", methods=['GET', 'POST'])
def creates():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        pic = request.files["pic"]
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        user = User(name=name, age=age, city=city, pic=pic.read(), filename=filename, mimetype=mimetype)

        contact = Contact(phone=request.form["phone"],
                          tg=request.form["tg"],
                          user=user)
        user.contact.append(contact)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect("/")
        except Exception as error:
            return f'При добавлении поста произошла ошибка: {error}'
    else:
        return render_template("creates.html")

@app.route("/img/<int:id>")
def get_img(id):
    pic = User.query.filter_by(id=id).first()
    if not pic:
        return 'Нет изображения с таким id', 404

    return Response(pic.pic, mimetype=pic.mimetype)


@app.route("/project/<int:user_id>/img/<int:prj_id>")
def get_img(user_id, prj_id):
    user = User.query.get(user_id)
    pic = user.project.filter_by(id=prj_id)
    if not pic:
        return 'Нет изображения с таким id', 404

    return Response(pic.pic, mimetype=pic.mimetype)

@app.route("/<int:id>")
def profile(id):
    user = User.query.get(id)
    users = User.query.all()
    educations = user.education.all() if user else None
    contact = user.contact.all() if user else None
    project = user.project.all()
    return render_template('index.html', users=users, user=user, educations=educations, contact=contact, project=project)


@app.route("/")
def index():
    user = User.query.first()
    users = User.query.all()
    educations = user.education.all() if user else None
    contact = user.contact.all() if user else None
    project = user.project.all()
    return render_template('index.html', users=users, user=user, educations=educations, contact=contact, project=project)

@app.route("/<int:id>/education", methods=["GET", "POST"])
def add_education(id):
    user = User.query.get(id)
    if request.method == "POST":
        education = Education(education_institution=request.form['education_institution'],
                              graduation_year=request.form['graduation_year'],
                              link=request.form['link'],
                              user=user)
        try:
            db.session.add(education)
            db.session.commit()
            return redirect("/")
        except Exception as error:
            return  f'При добавлении поста произошла ошибка: {error}'
    else:
        return render_template("education.html")


@app.route("/<int:id>/project", methods=["GET", "POST"])
def add_project(id):
    user = User.query.get(id)
    if request.method == "POST":
        project = Education(name=request.form['name'],
                              description=request.form['description'],
                              link=request.form['link'],
                              pic=pic.read(),
                              mimetype=pic.mimetype,
                              filename=secure_filename(pic.filename),
                              user=user)
        try:
            db.session.add(project)
            db.session.commit()
            return redirect("/")
        except Exception as error:
            return  f'При добавлении поста произошла ошибка: {error}'
    else:
        return render_template("education.html")

if __name__ == "__main__":
    app.run(debug=True)
