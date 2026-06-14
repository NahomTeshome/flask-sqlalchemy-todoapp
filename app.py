from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    
    todos = db.relationship('Todo', backref='owner', lazy=True)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(200), nullable=False)
    is_complete = db.Column(db.Boolean,default = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['POST'])
def login():

    current_user_name = request.form.get("username")

    user = User.query.filter_by(username = current_user_name).first()

    if not user:
        user = User(username = current_user_name)
        db.session.add(user)
        db.session.commit()
    return f"Hello {current_user_name} you have logged in succesfully"






if __name__ == "__main__":
    app.run(debug=True,port= 8500)
