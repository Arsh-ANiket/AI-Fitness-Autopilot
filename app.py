import streamlit as st
import pandas as pd

from modules.workout_logger import initialize_file, add_workout, get_workouts
from modules.planner import get_suggestion
from modules.progress import get_exercise_progress, get_progress_insight

# --- INIT ---
initialize_file()

# --- Exercise Mapping ---
EXERCISE_MAP = {
    "Bench Press": "Chest",
    "Inclined Bench Press": "Chest",
    "Chest Fly": "Chest",
    "Cable Fly Crossover": "Chest",
    "Shoulder Press": "Shoulders",
    "Tricep Pushdown": "Triceps",
    "Tricep Rope Pushdown": "Triceps",
    "Push Ups": "Chest",
    "Pull Ups": "Back",
    "Bicep Curl": "Biceps",
    "Lat Pulldown": "Back",
    "Seated Cable Row": "Back",
    "Hammer Curl": "Biceps",
    "Lateral Raise": "Shoulders",
    "Face Pull": "Shoulders",
    "Barbell Row": "Back",
    "Shrug": "Shoulders",
    "Squats": "Legs",
    "Seated Leg Curl": "Legs",
    "Leg Extension": "Legs",
    "Leg Press": "Legs",
}

st.title("💪 AI Fitness Autopilot")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["🏋️ Log Workout", "📊 Progress", "📜 History"])

# =========================
# 🏋️ TAB 1 — WORKOUT LOG
# =========================
with tab1:
    st.header("Log Workout")

    col1, col2 = st.columns(2)

    with col1:
        exercise = st.selectbox("Exercise", list(EXERCISE_MAP.keys()))

    with col2:
        muscle = EXERCISE_MAP[exercise]
        st.success(f"🎯 {muscle}")

    # --- Table Input for Sets ---
    st.subheader("Sets")

    default_data = pd.DataFrame({"Reps": [10, 10, 10], "Weight": [40, 40, 40]})

    edited_df = st.data_editor(default_data, num_rows="dynamic")

    # --- Save ---
    if st.button("Add Workout"):
        for _, row in edited_df.iterrows():
            add_workout(exercise, muscle, 1, int(row["Reps"]), int(row["Weight"]))
        st.success("Workout Added!")

    # --- Suggestion ---
    st.subheader("💡 Workout Suggestion")

    df = get_workouts()

    if not df.empty:
        today = df[df["date"] == df["date"].max()]
        muscles_trained = today["muscle"].tolist()

        suggestion = get_suggestion(muscles_trained)
        st.info(suggestion)
    else:
        st.warning("No workout data yet")

# =========================
# 📊 TAB 2 — PROGRESS
# =========================
with tab2:
    st.header("Progress Tracker")

    df = get_workouts()

    if not df.empty:
        exercise_list = df["exercise"].unique()
        selected_exercise = st.selectbox("Select Exercise", exercise_list)

        progress_df = get_exercise_progress(df, selected_exercise)

        if progress_df is not None:
            st.line_chart(progress_df.set_index("date"))

            insight = get_progress_insight(df, selected_exercise)
            st.info(insight)
    else:
        st.warning("No data available")

# =========================
# 📜 TAB 3 — HISTORY
# =========================
with tab3:
    st.header("Workout History")

    df = get_workouts()
    st.dataframe(df)
