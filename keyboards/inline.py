from aiogram.utils.keyboard import InlineKeyboardBuilder

ACTIVITY_LEVELS = {
    "1.2": ("минимальная (сидячая работа)", 1.2),
    "1.375": ("легкая (тренировки 1-3 раза в нед.)", 1.375),
    "1.55": ("средняя (тренировки 3-5 раз в нед.)", 1.55),
    "1.725": ("высокая (тяжелые нагрузки 6-7 раз)", 1.725),
}

def get_gender_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Мужской", callback_data="gender_male")
    builder.button(text="Женский", callback_data="gender_female")
    return builder.as_markup()

def get_goal_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Снижение веса", callback_data="goal_loss")
    builder.button(text="Поддержание веса" , callback_data="goal_keep")
    builder.button(text="Набор веса" , callback_data="goal_gain")
    builder.adjust(1)
    return builder.as_markup()

def get_activity_keyboard():
    builder = InlineKeyboardBuilder()
    for key, (label, _) in ACTIVITY_LEVELS.items():
        builder.button(text=label, callback_data=f"act_{key}")
    builder.adjust(1)
    return builder.as_markup()