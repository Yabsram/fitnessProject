import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm
from werkzeug.security import generate_password_hash
from apis import genai_fitness_plan
from forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (LoginManager, UserMixin, login_user, logout_user, login_required, current_user)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_KEY")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

with app.app_context():
  db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", status="Login", page="/login")

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            password = form.password.data
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('workouts'))
            else:
                raise ValueError("Invalid Email/Password")
        except Exception as e:
            return render_template('login.html', form=form, message=e, status="Login", page="/login")
    return render_template('login.html', form=form, status="Login", page="/login")


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
            return redirect(url_for('login'))
        except Exception as e:
            message = f'An error has occured: {e}'
            return render_template("register.html", form=form, message=message, status="Login", page="/login")
    return render_template("register.html", form=form, status="Login", page="/login")

@app.route('/workouts', methods=['GET', 'POST'])
@login_required
def workouts():
    workout_plan = None        
    if request.method == "POST":

        height = request.form['height']
        weight = request.form['weight']
        goal   = request.form['goal']
        age    = request.form.get('age')
        gender = request.form.get('gender')

        workout_plan = genai_fitness_plan(height, weight, goal, age, gender)

    return render_template("workouts.html", workout_plan=workout_plan, status="Logout", page="/logout")

@app.route('/recipes')
@login_required
def recipes():
    return render_template("recipes.html", status="Logout", page="/logout")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
        app.run(debug=True, host="0.0.0.0",port=5001)