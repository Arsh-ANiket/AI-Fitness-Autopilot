import streamlit as st
import pandas as pd

from modules.workout_logger import initialize_file, add_workout, get_workouts
from modules.planner import get_suggestion
from modules.progress import get_exercise_progress, get_progress_insight
from modules.calories import calculate_bmr, calculate_maintenance, get_calorie_target
from modules.predictor import predict_fat_loss

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
tab1, tab2, tab3, tab4 = st.tabs(
    ["🏋️ Log Workout", "📊 Progress", "📜 History", "🍽️ Nutrition"]
)

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

# nutrition
with tab4:
    st.header("🍽️ Your Daily Fitness Plan")

    st.write("Fill your details and get a personalized plan 👇")
    use_advanced = st.toggle("Use advanced workout tracking (optional)")
    # --- USER INPUT ---
    col1, col2, col3 = st.columns(3)

    with col1:
        weight = st.number_input("Your Weight (kg)", value=100)

    with col2:
        height = st.number_input("Your Height (cm)", value=180)

    with col3:
        age = st.number_input("Your Age", value=25)

    activity_options = {
        "Mostly Sitting (Office Work)": 1.2,
        "Light Activity (Gym 2-3 days)": 1.375,
        "Moderate (Gym 4-5 days)": 1.55,
        "Very Active (Daily intense training)": 1.725,
    }

    activity_label = st.selectbox(
        "Your Daily Activity Level", list(activity_options.keys())
    )

    activity = activity_options[activity_label]

    goal = st.selectbox("Your Goal", ["Fat Loss", "Maintain Weight", "Muscle Gain"])

    # --- CALCULATIONS ---
    bmr = calculate_bmr(weight, height, age)
    maintenance = calculate_maintenance(bmr, activity)
    if use_advanced:
        st.subheader("Wokrout adjustment")
        workout_calories = st.number_input(
            "Estimated calories burned from workouts (kcal/day)", value=300
        )
        maintenance += workout_calories
    target = get_calorie_target(goal, maintenance)

    # --- RESULTS ---
    st.subheader("📊 Your Plan")

    st.success(f"👉 You should eat around **{int(target)} kcal/day**")

    if goal == "Fat Loss":
        st.info("🔥 This will help you lose ~0.5 kg per week safely")
    elif goal == "Muscle Gain":
        st.info("💪 Eat high protein along with this calorie target")
    else:
        st.info("⚖️ This will help you maintain your current weight")

    # --- EXPANDABLE EXPLANATION ---
    with st.expander("📘 Want to understand how this works?"):
        st.write(
            f"""
        - Your body needs around **{int(maintenance)} kcal/day** to maintain weight  
        - Based on your goal, we adjust calories  
        - Fat loss = eat less  
        - Muscle gain = eat more  
        """
        )

    # =========================
    # 🎯 GOAL PREDICTION
    # =========================
    st.subheader("🎯 Your Goal Timeline")

    target_weight = st.number_input("Target Weight (kg)", value=80)

    result = predict_fat_loss(weight, target_weight, maintenance, target)

    if "weekly_loss" in result:
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Expected Fat Loss", f"{result['weekly_loss']} kg/week")

        with col2:
            st.metric("Time to Goal", f"{result['weeks_needed']} weeks")

        st.success(result["message"])

        # 🔥 SMART INSIGHT
        if result["weeks_needed"] > 40:
            st.warning(
                "⚠️ This is a long timeline. Consider increasing activity or reducing calories slightly."
            )

    else:
        st.warning(result["message"])
