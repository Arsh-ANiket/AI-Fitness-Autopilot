import pandas as pd


def get_exercise_progress(df, exercise_name):
    exercise_df = df[df["exercise"] == exercise_name]

    if exercise_df.empty:
        return None

    exercise_df["date"] = pd.to_datetime(exercise_df["date"])

    # volume per set
    exercise_df["volume"] = exercise_df["reps"] * exercise_df["weight"]

    # group by date (clean graph)
    grouped = (
        exercise_df.groupby("date")
        .agg({"weight": "mean", "volume": "sum"})
        .reset_index()
    )

    return grouped


def get_progress_insight(df, exercise_name):
    exercise_df = df[df["exercise"] == exercise_name]

    if len(exercise_df) < 2:
        return "👉 Not enough data for insights"

    exercise_df["date"] = pd.to_datetime(exercise_df["date"])
    exercise_df = exercise_df.sort_values("date")

    first = exercise_df.iloc[0]["weight"]
    last = exercise_df.iloc[-1]["weight"]

    if last > first:
        return f"📈 Progressing! Increased from {first}kg to {last}kg"
    elif last < first:
        return f"📉 Strength decreased from {first}kg to {last}kg"
    else:
        return "⚖️ No change in strength"
