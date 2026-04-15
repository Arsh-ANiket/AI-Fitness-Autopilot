def get_suggestion(trained_muscles):
    push = {"Chest", "Shoulders", "Triceps"}
    pull = {"Back", "Biceps"}
    legs = {"Legs"}

    trained_set = set(trained_muscles)

    # --- Detect category ---
    trained_push = trained_set & push
    trained_pull = trained_set & pull
    trained_legs = trained_set & legs

    # --- Case 1: Partial PUSH ---
    if trained_push and len(trained_push) < len(push):
        missing = push - trained_push
        return f"👉 You started PUSH workout. Add: {', '.join(missing)}"

    # --- Case 2: Full PUSH done ---
    if trained_push:
        return "👉 PUSH completed. Suggested next: Back + Biceps (Pull Day)"

    # --- Case 3: Partial PULL ---
    if trained_pull and len(trained_pull) < len(pull):
        missing = pull - trained_pull
        return f"👉 You started PULL workout. Add: {', '.join(missing)}"

    # --- Case 4: Full PULL done ---
    if trained_pull:
        return "👉 PULL completed. Suggested next: Legs Day"

    # --- Case 5: Legs ---
    if trained_legs:
        return "👉 LEGS done. Suggested next: Push Day (Chest + Shoulders + Triceps)"

    return "👉 Log more workouts to get better suggestions"
