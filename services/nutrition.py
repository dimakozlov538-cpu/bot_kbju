def calculate_kbju(gender:str, age:int, height:int, weight:float,activity:float, goal:str) -> dict:
    if gender == 'male':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        safe_floor = max(bmr, 1500)
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        safe_floor = max(bmr, 1200)

    tdee = bmr * activity

    if goal == 'loss':
        target_kcal = max(tdee * 0.85, safe_floor)
        protein_g = weight * 2
        fat_g = weight * 0.9
        goal_text = "Плавное снижение калорий"
    elif goal == 'gain':
        target_kcal = tdee * 1.15
        protein_g = weight * 1.8
        fat_g = weight * 1.0
        goal_text = "плавный массонабор"
    else:
        target_kcal = tdee
        protein_g = weight * 1.6
        fat_g = weight * 1.0
        goal_text = "поддержание веса"

    carbs_kcal = target_kcal - (protein_g * 4) - (fat_g * 9)
    carbs_g = max(carbs_kcal / 4 , 50)  

    return {
        "goal_text": goal_text,
        "target_kcal": round(target_kcal),
        "bmr": round(bmr),
        "protein_g": round(protein_g),
        "fat_g": round(fat_g),
        "carbs_g": round(carbs_g),
    }