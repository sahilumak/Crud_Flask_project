from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# import sqlite3
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class Todo(db.Model):
    Srn = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(200),nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()
@app.route("/",methods=["GET","POST"])
def home():
    if request.method=="POST":
        title =  request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    todos = Todo.query.all()
    return render_template("home1.html",todos = todos)

@app.route("/delete/<int:Srn>")
def delete(Srn):
    todo = Todo.query.filter_by(Srn = Srn).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect("/")

@app.route("/update/<int:Srn>",methods = ["GET","POST"])
def update(Srn):
    # todo = Todo.query.filter_by(Srn)
    if request.method=="GET":
        todo = Todo.query.filter_by(Srn = Srn).first()
        return render_template("update.html",todo = todo)
    else:
        title =  request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(Srn = Srn).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()

    return redirect(url_for('home'))



if __name__=="__main__":
    app.run(debug=True)