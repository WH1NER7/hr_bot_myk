import asyncio
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import database

# Токен вашего бота
API_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp = Dispatcher()


# Определение состояний
class TestStates(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()
    Q6 = State()
    TestQ1 = State()
    TestQ2 = State()
    TestQ3 = State()
    TestQ4 = State()
    TestQ5 = State()
    TestEnd = State()


# Словарь для хранения ответов пользователя
user_data = {}

# Inline-клавиатуры
start_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="О бренде", callback_data="about_brand")]
    ]
)

about_brand_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Условия вакансии", callback_data="job_conditions")]
    ]
)

job_conditions_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Условия работы", callback_data="job_conditions_2")]
    ]
)

job_conditions_2_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Пройти тест", callback_data="start_test")]
    ]
)

# Ответы на тестовые вопросы
correct_answers = {
    '1': '1',
    '2': '2',
    '3': '1',
    '4': '3',
    '5': '3'
}


# Хендлер на команду /start
@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! 👋\n\nМы открываем вакансию на должность <b>менеджера маркетплейсов</b> в команду бренда <b>\"MissYourKiss\"</b>.\n\n"
        "Мы коротко расскажем о компании и предложим наши условия по вакансии.\n"
        "В конце мы подготовили короткий тест, чтобы лучше понять ваши компетенции.\n\n"
        "Нажмите кнопку ниже, чтобы узнать о бренде 👇",
        reply_markup=start_inline_keyboard
    )


# Хендлер для нажатия на кнопку "О бренде"
@dp.callback_query(F.data == "about_brand")
async def about_brand(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "🌟 MissYourKiss - символ женственности в мире нижнего белья.\n"
        "Немного о нас:\n\n"
        "— Мы на рынке уже 5 лет!\n"
        "— Оборот нашей компании от 70 млн руб в месяц,\n"
        "— Мы ТОП-1 в категории нижнего белья на WB\n"
        "— В июне 2024 года Мистелла получила статус резидента Сколково!\n"
        "— Наше белье знают и любят многие, ведь мы задаем тренды и дарим неповторимые эмоции (55.000 заказов в месяц)",
        reply_markup=about_brand_keyboard
    )
    await callback_query.answer()


# Хендлер для нажатия на кнопку "Условия вакансии"
@dp.callback_query(F.data == "job_conditions")
async def job_conditions(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "🌐 Мы работаем на маркетплейсах Ozon и WB, вот примерный список задач которые предстоит выполнять:\n\n"
        "– Выполнение плановых показателей отдела продаж по основным направлениям (объем заказов, маржинальность и ДРР)\n"
        "– Управление рекламным кабинетом на маркетплейсах\n"
        "– Участие в запуске новых SKU\n"
        "– Генерация и тестирование гипотез по привлечению целевого трафика",
        reply_markup=job_conditions_keyboard
    )
    await callback_query.answer()


# Хендлер для нажатия на кнопку "Условия работы"
@dp.callback_query(F.data == "job_conditions_2")
async def job_conditions_2(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "💼 Мы предлагаем:\n\n"
        "— Заработная плата: 100 000 до вычета НДФЛ на период испытательного срока, после прохождения + kpi\n"
        "— Режим работы: 5/2 с 09:00 до 18:00 удаленно\n"
        "— Свобода действий: ты сам выбираешь, как достигнуть результат\n"
        "— Четкая и прозрачная постановка задач без отвлечения от основных приоритетов\n"
        "— Внимательное руководство и коллеги: мы поддержим твои идеи\n"
        "— Карьерное развитие, обучающие курсы и тренинги для повышения квалификации за счет компании\n"
        "— Официальное оформление по ТК РФ\n"
        "— Премии и бонусы за реальный рост показателей!",
        reply_markup=job_conditions_2_keyboard
    )
    await callback_query.answer()


@dp.callback_query(F.data == "start_test")
async def start_test(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if database.user_exists(user_id):
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text="Вы уже проходили тест и отправляли свои данные. Спасибо!"
        )
    else:
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=(
                "📝 Пожалуйста, ответьте на следующие вопросы:\n\n"
                "*Присылайте ответы текстом прямо в бота!*\n\n"
                "1. Ваше имя?"
            )
        )
        await state.set_state(TestStates.Q1)
    await callback_query.answer()



# Хендлеры для вопросов о себе
@dp.message(TestStates.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer1 = message.text
    await state.update_data(name=answer1)
    await message.answer("2. С какими маркетплейсами ты работал? Как давно?")
    await state.set_state(TestStates.Q2)


@dp.message(TestStates.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer2 = message.text
    await state.update_data(marketplaces=answer2)
    await message.answer("3. Какой у тебя был максимальный бюджет в управлении в месяц?")
    await state.set_state(TestStates.Q3)


@dp.message(TestStates.Q3)
async def answer_q3(message: types.Message, state: FSMContext):
    answer3 = message.text
    await state.update_data(budget=answer3)
    await message.answer("4. Поделись своими достижениями на маркетплейсах! Напиши ответ в свободной форме")
    await state.set_state(TestStates.Q4)


@dp.message(TestStates.Q4)
async def answer_q4(message: types.Message, state: FSMContext):
    answer4 = message.text
    await state.update_data(achievements=answer4)
    await message.answer("5. Есть ли текущие проекты? Если есть, то какие?")
    await state.set_state(TestStates.Q5)


@dp.message(TestStates.Q5)
async def answer_q5(message: types.Message, state: FSMContext):
    answer5 = message.text
    await state.update_data(current_projects=answer5)
    await message.answer("6. С какими оборотами работал в месяц?")
    await state.set_state(TestStates.Q6)


@dp.message(TestStates.Q6)
async def answer_q6(message: types.Message, state: FSMContext):
    answer6 = message.text
    await state.update_data(monthly_turnover=answer6)
    await message.answer(
        "Спасибо за ваши ответы! Теперь пройдите небольшой тест по базовым компетенциям для работы на маркетплейсах! Он поможет нам лучше понять ваш уровень 🔍"
    )
    await asyncio.sleep(2)
    # Начинаем тестовые вопросы
    await send_test_question1(message, state)


# Функции для отправки тестовых вопросов и обработки ответов
# Вопрос 1
async def send_test_question1(message: types.Message, state: FSMContext):
    question = "1. Что такое биддер?\n\
1️⃣ Система автоматизации ставок\n\
2️⃣ Человек, настраивающий рекламу\n\
3️⃣ Метрика внутренней рекламы WB"
    options = [
        InlineKeyboardButton(text="1️⃣", callback_data="q1_1"),
        InlineKeyboardButton(text="2️⃣", callback_data="q1_2"),
        InlineKeyboardButton(text="3️⃣", callback_data="q1_3")
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[options])
    await message.answer(question, reply_markup=keyboard)
    await state.set_state(TestStates.TestQ1)


@dp.callback_query(TestStates.TestQ1)
async def answer_test_q1(callback_query: types.CallbackQuery, state: FSMContext):
    user_choice = callback_query.data.split('_')[1]
    user_data['q1'] = user_choice
    await callback_query.answer()
    await send_test_question2(callback_query.message, state)


# Вопрос 2
async def send_test_question2(message: types.Message, state: FSMContext):
    question = "2. Какие показатели рекламы говорят о её эффективности?\n\
1️⃣ CTR 6%, ДРР 23%, CPC 61₽\n\
2️ CTR 13%, ДРР 3%, CPC 7₽\n\
3️⃣ CTR 16%, ДРР 10%, CPC 186₽"
    options = [
        InlineKeyboardButton(text="1️⃣", callback_data="q2_1"),
        InlineKeyboardButton(text="2️⃣", callback_data="q2_2"),
        InlineKeyboardButton(text="3️⃣", callback_data="q2_3")
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[options], )
    await message.edit_text(question, reply_markup=keyboard)
    await state.set_state(TestStates.TestQ2)


@dp.callback_query(TestStates.TestQ2)
async def answer_test_q2(callback_query: types.CallbackQuery, state: FSMContext):
    user_choice = callback_query.data.split('_')[1]
    user_data['q2'] = user_choice
    await callback_query.answer()
    await send_test_question3(callback_query.message, state)


# Вопрос 3
async def send_test_question3(message: types.Message, state: FSMContext):
    question = "3. Какие основные отличия у внутренней рекламы в карточке товара?\n\
1️⃣ Нельзя настраивать ключевые запросы\n\
2️⃣ Видно рейтинг товара и количество отзывов\n\
3️⃣ Нельзя устанавливать временные интервалы показов"
    options = [
        InlineKeyboardButton(text="1️⃣", callback_data="q3_1"),
        InlineKeyboardButton(text="2️⃣", callback_data="q3_2"),
        InlineKeyboardButton(text="3️⃣", callback_data="q3_3")
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[options])
    await message.edit_text(question, reply_markup=keyboard)
    await state.set_state(TestStates.TestQ3)


@dp.callback_query(TestStates.TestQ3)
async def answer_test_q3(callback_query: types.CallbackQuery, state: FSMContext):
    user_choice = callback_query.data.split('_')[1]
    user_data['q3'] = user_choice
    await callback_query.answer()
    await send_test_question4(callback_query.message, state)


# Вопрос 4
async def send_test_question4(message: types.Message, state: FSMContext):
    question = "4. Какие факторы влияют на качество рекламы?\n\
1️⃣ Контент, ставки\n\
2️⃣ Ставки, ценовая сегментация\n\
3️⃣ Оба варианта"
    options = [
        InlineKeyboardButton(text="1️⃣", callback_data="q4_1"),
        InlineKeyboardButton(text="2️⃣", callback_data="q4_2"),
        InlineKeyboardButton(text="3️⃣", callback_data="q4_3")
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[options])
    await message.edit_text(question, reply_markup=keyboard)
    await state.set_state(TestStates.TestQ4)


@dp.callback_query(TestStates.TestQ4)
async def answer_test_q4(callback_query: types.CallbackQuery, state: FSMContext):
    user_choice = callback_query.data.split('_')[1]
    user_data['q4'] = user_choice
    await callback_query.answer()
    await send_test_question5(callback_query.message, state)


# Вопрос 5
async def send_test_question5(message: types.Message, state: FSMContext):
    question = "5. Какая метрика рекламы определяет стоимость заказа?\n\
1️⃣ CTR\n\
2️⃣ CPC\n\
3️⃣ CPO\n\
4️⃣ ROI"
    options = [
        InlineKeyboardButton(text="1️⃣", callback_data="q5_1"),
        InlineKeyboardButton(text="2️⃣", callback_data="q5_2"),
        InlineKeyboardButton(text="3️⃣", callback_data="q5_3"),
        InlineKeyboardButton(text="4️⃣", callback_data="q5_4")
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[options])
    await message.edit_text(question, reply_markup=keyboard)
    await state.set_state(TestStates.TestQ5)


@dp.callback_query(TestStates.TestQ5)
async def answer_test_q5(callback_query: types.CallbackQuery, state: FSMContext):
    user_choice = callback_query.data.split('_')[1]
    user_data['q5'] = user_choice
    await callback_query.answer()
    await finish_test(callback_query.message, state)


# Завершение теста и подсчет результатов
async def finish_test(message: types.Message, state: FSMContext):
    # Получаем данные из состояния
    data = await state.get_data()
    # Подсчет правильных ответов
    score = 0
    for i in range(1, 6):
        if user_data.get(f'q{i}') == correct_answers[str(i)]:
            score += 1
    result_text = f"Тест завершен! Вы набрали {score} из 5 баллов.\n\n\
🙏 Спасибо за твое время и интерес к нашему бренду!\n\
Мы свяжемся с тобой в ближайшее время.\n\n\
Если у тебя возникнут дополнительные вопросы, не стесняйся их задавать нашему HR!\n\
\n\
Контакт: @julietteHR"
    await message.edit_text(result_text)
    # Добавляем баллы и информацию о пользователе

    data['test_score'] = score
    data['user_id'] = message.chat.id
    data['username'] = message.chat.username
    data['first_name'] = message.chat.first_name
    # Сохраняем данные в базу данных
    database.save_user_data(data)
    # Очистка состояния
    await state.clear()


# Запуск бота
async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
