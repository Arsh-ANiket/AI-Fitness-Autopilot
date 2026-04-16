def predict_fat_loss(current_weight, target_weight, maintenance, intake):
    daily_deficit = maintenance - intake

    if daily_deficit <= 0:
        return {
            "status": "No deficit",
            "message": "Your current intake does not create a calorie deficit. Please adjust your intake or activity level.",
        }

    weekly_loss = (daily_deficit * 7) / 7700
    total_weight_to_lose = current_weight - target_weight
    weeks_needed = total_weight_to_lose / weekly_loss
    return {
        "weekly_loss": round(weekly_loss, 2),
        "weeks_needed": round(weeks_needed, 2),
        "message": f"At a daily deficit of {daily_deficit} calories, you can expect to lose approximately {weekly_loss} kg per week. It will take around {weeks_needed} weeks to reach your target weight of {target_weight} kg.",
    }
