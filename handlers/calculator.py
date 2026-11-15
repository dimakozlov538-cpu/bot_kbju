from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.inline import (
    ACTIVITY_LEVELS,
    get_gender_keyboard,
    get_activity_keyboard,
    get_goal_keyboard,
)
from services.nutrition import calculate_kbju

router = Router()

class CalcForm(StatesGroup):
    gender = State()
    age = State()
    height = State()
    weight = State()
    activity = State()
    goal = State()

@router.message(Command("start"))
async def cmd_start(message:types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привет! Я помогу рассчитать твою дневную норму калорий и БЖУ.\n"
        "Для начала выбери свой пол:",
        reply_markup=get_gender_keyboard()
    )
    await state.set_state(CalcForm.gender)

@router.callback_query(CalcForm.gender, F.data.startswith("gender_"))
async def process_gender(callback: types.CallbackQuery, state: FSMContext):
    gender = callback.data.split("_")[1]
    await state.update_data(gender=gender)
    await callback.message.edit_text("Сколько тебе полных лет? (Введи число, например: 28)")
    await state.set_state(CalcForm.age)

@router.message(CalcForm.age)
async def process_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or not (18 <= int(message.text) <= 100):
        await message.answer("Пожалуйста, введи корректный возраст для взрослого (от 18 до 100 лет):")
        return
    await state.update_data(age=int(message.text))
    await message.answer("Укажи свой рост в сантиметрах (например: 175):")
    await state.set_state(CalcForm.height)

@router.message(CalcForm.height)
async def process_height(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or not (120 <= int(message.text) <= 250):
        await message.answer("Пожалуйста, введи реальный рост в см (от 120 до 250):")
        return
    await state.update_data(height=int(message.text))
    await message.answer("Укажи свой текущий вес в килограммах (например: 72.5):")
    await state.set_state(CalcForm.weight)

@router.message(CalcForm.weight)
async def process_weight(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text.replace(",", "."))
        if not (35 <= weight <= 300):
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, введи корректный вес в кг (от 35 до 300):")
        return
        
    await state.update_data(weight=weight)
    await message.answer("Выбери свой уровень физической активности:", reply_markup=get_activity_keyboard())
    await state.set_state(CalcForm.activity)

@router.callback_query(CalcForm.activity, F.data.startswith("act_"))
async def process_activity(callback: types.CallbackQuery, state: FSMContext):
    act_key = callback.data.split("_")[1]
    await state.update_data(activity=ACTIVITY_LEVELS[act_key][1])
    await callback.message.edit_text("Какая у тебя главная цель?", reply_markup=get_goal_keyboard())
    await state.set_state(CalcForm.goal)

@router.callback_query(CalcForm.goal, F.data.startswith("goal_"))
async def process_goal(callback: types.CallbackQuery, state: FSMContext):
    # [1] берет второе слово после подчеркивания: "loss", "keep" или "gain"
    goal = callback.data.split("_")[1]
    data = await state.get_data()
    
    res = calculate_kbju(
        gender=data["gender"],
        age=data["age"],
        height=data["height"],
        weight=data["weight"],
        activity=data["activity"],
        goal=goal
    )
    
    result_text = (
        f"📊 <b>Твой персональный расчет готов!</b>\n\n"
        f"🎯 <b>Цель:</b> {res['goal_text']}\n"
        f"🔥 <b>Дневная норма:</b> {res['target_kcal']} ккал\n"
        f"<i>(Базовый обмен в покое: {res['bmr']} ккал)</i>\n\n"
        f"🥩 <b>Белки:</b> {res['protein_g']} г ({res['protein_g'] * 4} ккал)\n"
        f"🥑 <b>Жиры:</b> {res['fat_g']} г ({res['fat_g'] * 9} ккал)\n"
        f"🌾 <b>Углеводы:</b> {res['carbs_g']} г ({res['carbs_g'] * 4} ккал)\n\n"
        f"Чтобы пересчитать данные заново, нажми /start"
    )
    
    await callback.message.edit_text(result_text, parse_mode="HTML")
    await state.clear()
