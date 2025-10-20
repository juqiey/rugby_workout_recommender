# app.py
from flask import Flask, render_template, request
from workout import recommend, goals

app = Flask(__name__)

@app.route("/form", methods=["GET", "POST"])
def index():
    goal_names = goals["goal_name"].tolist()
    selected_goal = None
    recommendations = None

    if request.method == "POST":
        selected_goal = request.form.get("goal_name")
        recommendations = recommend(selected_goal, top_n=5)

    return render_template("index.html",
                           goal_names=goal_names,
                           selected_goal=selected_goal,
                           recommendations=recommendations)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
