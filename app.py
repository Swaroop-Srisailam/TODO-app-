
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class TODO(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(200), nullable=False)
    Disc = db.Column(db.String(500), nullable=False)
    Datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.Sno} - {self.Title}"


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        disc = request.form['Disc']
        todo = TODO(Title=title, Disc=disc)
        db.session.add(todo)
        db.session.commit()

    Alltodo = TODO.query.all()
    return render_template('./index.html', alltodo=Alltodo)
    # return "<p>Hello, World!</p>"


@app.route("/update/<int:Sno>", methods=["GET", "POST"])
def update(Sno):
    todo = TODO.query.filter_by(Sno=Sno).first()
    if request.method == "POST":
        title = request.form['title']
        disc = request.form['Disc']
        todo.Title = title
        todo.Disc = disc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    return render_template('./update.html', todo=todo)


@app.route("/delete/<int:Sno>")
def delete(Sno):
    todo = TODO.query.filter_by(Sno=Sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
