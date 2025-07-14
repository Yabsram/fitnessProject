from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("nav.html")

@app.route('/workouts')
def workouts():
    return render_template("workouts.html")

@app.route('/recipes')
def recipes():
    return render_template("recipes.html")


if __name__ == '__main__':
        app.run(debug=True, host="0.0.0.0")