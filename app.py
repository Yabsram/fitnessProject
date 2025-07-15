import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

with app.app_context():
  db.create_all()

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user_exists = User.query.filter_by(username=form.username.data).first()
            email_exists = User.query.filter_by(email=form.email.data).first()
            if user_exists:
                raise ValueError("User already exsists")
            if email_exists:
                raise ValueError("Email already in use")
            user = User(username=form.username.data, email=form.email.data, password=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('workouts'))
        except Exception as e:
            message = f'An error has occured: {e}'
            return render_template("register.html", form=form, message=message)
    return render_template("register.html", form=form)

@app.route('/workouts')
def workouts():
    return render_template("workouts.html")

@app.route('/recipes')
def recipes():
    return render_template("recipes.html")


if __name__ == '__main__':
        app.run(debug=True, host="0.0.0.0")