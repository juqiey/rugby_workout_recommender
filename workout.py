# workout.py
import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# === Load saved files ===
exercises = pd.read_csv("exercises.csv")
goals = pd.read_csv("goals.csv")

vectorizer = joblib.load("tfidf_vectorizer.joblib")
exercise_matrix = joblib.load("exercise_matrix.joblib")
goal_matrix = joblib.load("goal_matrix.joblib")

# === Recommender Function ===
def recommend(goal_name, top_n=6):
    if goal_name not in goals["goal_name"].values:
        return pd.DataFrame()  # empty if goal not found

    idx = goals[goals["goal_name"] == goal_name].index[0]
    sims = cosine_similarity(goal_matrix[idx:idx + 1], exercise_matrix)[0]
    top_idx = sims.argsort()[-top_n:][::-1]

    recs = exercises.loc[top_idx, [
        "exercise_name",
        "type",
        "target_muscles",
        "primary_attributes",
        "intensity_level",
        "equipment_needed",
        "category"
    ]].copy()

    recs["score"] = sims[top_idx]
    return recs.reset_index(drop=True)
