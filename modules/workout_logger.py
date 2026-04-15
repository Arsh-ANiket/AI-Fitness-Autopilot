import pandas as pd
import os
from datetime import datetime

FILE_PATH = "data/workouts.csv"


def initialize_file():
    if not os.path.exists(FILE_PATH) or os.stat(FILE_PATH).st_size == 0:
        df = pd.DataFrame(
            columns=["date", "exercise", "muscle", "sets", "reps", "weight"]
        )
        df.to_csv(FILE_PATH, index=False)


def add_workout(exercise, muscle, sets, reps, weight):
    df = pd.read_csv(FILE_PATH)

    new_entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "exercise": exercise,
        "muscle": muscle,
        "sets": sets,
        "reps": reps,
        "weight": weight,
    }

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(FILE_PATH, index=False)


def get_workouts():
    return pd.read_csv(FILE_PATH)
