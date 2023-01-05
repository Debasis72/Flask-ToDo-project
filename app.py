from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ToDo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    slno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.slno} - {self.title}"

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo= ToDo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    alltodo=ToDo.query.all()

    return render_template('index.html',alltodo=alltodo)

@app.route('/show')
def product():
    alltodo=ToDo.query.all()
    print(alltodo)
    return 'WellCome to my product page'

@app.route('/update/<int:slno>', methods=['GET', 'POST'])
def update(slno):
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo=ToDo.query.filter_by(slno=slno).first()
        todo.titile=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo=ToDo.query.filter_by(slno=slno).first()
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:slno>')
def delete(slno):
    todo=ToDo.query.filter_by(slno=slno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)