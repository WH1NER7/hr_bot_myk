import asyncio
from datetime import datetime

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram import F, types

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import database

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from aiogram import Router
accountant_router = Router()


# Определение состояний
class AccountantStates(StatesGroup):
    Vacancy = State()
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()
    Q6 = State()
    Q7 = State()
    GET_CONTACT = State()
    TestQ1 = State()
    TestQ2 = State()
    TestQ3 = State()
    TestQ4 = State()
    TestEnd = State()


# Словарь для хранения ответов пользователя
user_data = {}


about_brand_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Условия вакансии", callback_data="job_conditions_acc")]
    ]
)

job_conditions_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Условия работы", callback_data="job_conditions_2_acc")]
    ]
)

job_conditions_2_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Пройти тест", callback_data="start_test_acc")]
    ]
)

# Ответы на тестовые вопросы
correct_answers = {
    '1': '3',
    '2': '1',
    '3': '3',
    '4': '2'
}


# Хендлер для нажатия на кнопку "О бренде"
@accountant_router.callback_query(F.data == "vacancy_accountant")
async def about_brand(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "<b>Мы Мистелла</b> — крупная, развивающаяся компания по производству нижнего белья, представленная на Wildberries, Ozon под брендом <a href='https://www.wildberries.ru/catalog/0/search.aspx?search=missyourkiss'>МissYourKiss</a>.\n\
    \n \
<b>Немного о нас:</b>\n\
✓ На рынке 5 лет, команда 50+ чел\n\
✓ Выручка от 500 млн руб / год, более 1 млн проданных товаров\n\
✓ ТОП-3 в категории комплектов нижнего белья на WB и Ozon\n\
✓ Резидент Сколково\n\
✓ Наш бренд многие знают и любят",

        reply_markup=about_brand_keyboard
    )
    await callback_query.answer()


# Хендлер для нажатия на кнопку "Условия вакансии"
@accountant_router.callback_query(F.data == "job_conditions_acc")
async def job_conditions(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "Мы предлагаем:\n\
• График 5/2 с 9.00-18.00 в офисе | гибрид\n\
• ЗП от 100.000 р на руки (по договорённости)\n\
• Комфортабельный офис на Сибгата Хакима, 3. Г. Казань, с большим паркингом\n\
• Возможность развиваться профессионально, материально и интеллектуально",
        reply_markup=job_conditions_keyboard
    )
    await callback_query.answer()


# Хендлер для нажатия на кнопку "Условия работы"
@accountant_router.callback_query(F.data == "job_conditions_2_acc")
async def job_conditions_2(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "Задачи: \n\
• Подготовка первичной документации, налоговой и бухгалтерской отчётности\n\
• Подготовка ответов на камеральные запросы совместно с юристами\n\
• Расчет ЗП, налогов, взносов, больничных, компенсаций\n\
• Подготовка базы 1С к закрытию месяца\n\
    \n\
Нам важно:\n\
• Опыт работы в 1С УНФ, БП, ЗУП\n\
• Опыт работы по ОСНО\n\
• Подготовка налоговой и бухгалтерской отчётности\n\
• Опыт работы на участке заработной платы",
        reply_markup=job_conditions_2_keyboard
    )
    await callback_query.answer()


@accountant_router.callback_query(F.data == "start_test_acc")
async def start_test(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if database.user_exists(user_id, 'accountant'):
        await callback_query.message.answer(
            "Вы уже проходили тест и отправляли свои данные. Спасибо!"
        )
    else:
        await callback_query.message.answer(
            "📝 Пожалуйста, ответьте на следующие вопросы:\n\n"
            "*Присылайте ответы текстом прямо в бота!*\n\n"
            "1. Ваше имя?"
        )
        await state.update_data(vacancy="accountant")  # Сохраняем тип вакансии
        await state.set_state(AccountantStates.Q1)
    await callback_query.answer()


# Хендлеры для вопросов о себе
@accountant_router.message(AccountantStates.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer1 = message.text
    await state.update_data(name=answer1)
    await message.answer("2. Есть ли у Вас опыт работы в 1С УНФ?")
    await state.set_state(AccountantStates.Q2)


@accountant_router.message(AccountantStates.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer2 = message.text
    await state.update_data(unf_1c=answer2)
    await message.answer("3. Работали ли Вы в 1С ЗУП?")
    await state.set_state(AccountantStates.Q3)


@accountant_router.message(AccountantStates.Q3)
async def answer_q3(message: types.Message, state: FSMContext):
    answer3 = message.text
    await state.update_data(zup_1c=answer3)
    await message.answer("4. Есть ли у Вас опыт работы в 1С БП?")
    await state.set_state(AccountantStates.Q4)


@accountant_router.message(AccountantStates.Q4)
async def answer_q4(message: types.Message, state: FSMContext):
    answer4 = message.text
    await state.update_data(bp_1c=answer4)
    await message.answer("5. Имеется ли у Вас опыт работы на участке заработной платы? Сколько человек рассчитывали?")
    await state.set_state(AccountantStates.Q5)


@accountant_router.message(AccountantStates.Q5)
async def answer_q5(message: types.Message, state: FSMContext):
    answer5 = message.text
    await state.update_data(work_payments=answer5)
    await message.answer("6. Есть ли у Вас опыт работы по ОСНО?")
    await state.set_state(AccountantStates.Q6)


@accountant_router.message(AccountantStates.Q6)
async def answer_q5(message: types.Message, state: FSMContext):
    answer5 = message.text
    await state.update_data(osno_exp=answer5)
    await message.answer("7. Есть ли у Вас опыт подготовки налоговой и бухгалтерской отчётности?")
    await state.set_state(AccountantStates.Q7)


@accountant_router.message(AccountantStates.Q7)
async def answer_q7(message: types.Message, state: FSMContext):
    answer7 = message.text
    await state.update_data(buh_otchet=answer7)

    await message.answer(
        "Спасибо за ваши ответы!\nТеперь пройдите небольшой тест по базовым компетенциям для работы.\n"
        "Он поможет нам лучше понять ваш уровень 🔍",
    )
    await asyncio.sleep(2)
    await send_test_question1(message, state)  # Начинаем тест


# Функции для отправки тестовых вопросов и обработки ответов
# Вопрос 1
async def send_test_question1(message: types.Message, state: FSMContext):
    question = "1. Представим, что Ваш коллега уходит в отпуск. Когда Вы должны выплатить ему отпускные?\n\n\
1️⃣ День в день\n\
2️⃣ Минимум за 1 день до отпуска\n\
3️⃣ Минимум за 3 дня до отпуска"
    options = [
        InlineKeyboardButton(text="1️⃣", callback_data="q1_1"),
        InlineKeyboardButton(text="2️⃣", callback_data="q1_2"),
        InlineKeyboardButton(text="3️⃣", callback_data="q1_3")
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[options])
    await message.answer(question, reply_markup=keyboard)
    await state.set_state(AccountantStates.TestQ1)


@accountant_router.callback_query(AccountantStates.TestQ1)
async def answer_test_q1(callback_query: types.CallbackQuery, state: FSMContext):
    user_choice = callback_query.data.split('_')[1]
    user_data['q1'] = user_choice
    await callback_query.answer()
    await send_test_question2(callback_query.message, state)


# Вопрос 2
async def send_test_question2(message: types.Message, state: FSMContext):
    question = "2. ООО «Огонь» из Москвы продало товары ООО «Ласточка» из Владивостока. По договору право собственности переходит покупателю, когда товары поступают на его склад. Какую дату считать днем отгрузки? ООО «Ласточка» находится на УСН и попадает под освобождение по НДС.\n\n\
1️⃣ Дату когда ООО «Огонь» отгрузил товары в ООО «Ласточка»\n\
2️⃣ Дату когда ООО «Ласточка» принял товары себе на склад\n\
3️⃣ Дату когда ООО «Ласточка» оплатил товары, купленные у ООО «Огонь»"
    options = [
        InlineKeyboardButton(text="1️⃣", callback_data="q2_1"),
        InlineKeyboardButton(text="2️⃣", callback_data="q2_2"),
        InlineKeyboardButton(text="3️⃣", callback_data="q2_3")
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[options], )
    await message.edit_text(question, reply_markup=keyboard)
    await state.set_state(AccountantStates.TestQ2)


@accountant_router.callback_query(AccountantStates.TestQ2)
async def answer_test_q2(callback_query: types.CallbackQuery, state: FSMContext):
    user_choice = callback_query.data.split('_')[1]
    user_data['q2'] = user_choice
    await callback_query.answer()
    await send_test_question3(callback_query.message, state)


# Вопрос 3
async def send_test_question3(message: types.Message, state: FSMContext):
    question = "3. Чтобы предоставлять сотрудникам детские вычеты, как часто с них нужно брать соответствующие заявления?\n\n\
1️⃣ Ежегодно\n\
2️⃣ Один раз за все время работы\n\
3️⃣ Такие заявления не нужны"
    options = [
        InlineKeyboardButton(text="1️⃣", callback_data="q3_1"),
        InlineKeyboardButton(text="2️⃣", callback_data="q3_2"),
        InlineKeyboardButton(text="3️⃣", callback_data="q3_3")
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[options])
    await message.edit_text(question, reply_markup=keyboard)
    await state.set_state(AccountantStates.TestQ3)


@accountant_router.callback_query(AccountantStates.TestQ3)
async def answer_test_q4(callback_query: types.CallbackQuery, state: FSMContext):
    user_choice = callback_query.data.split('_')[1]
    user_data['q3'] = user_choice
    await callback_query.answer()
    await send_test_question4(callback_query.message, state)


# Вопрос 4
async def send_test_question4(message: types.Message, state: FSMContext):
    question = "4. Как часто компании нужно проводить обязательную инвентаризацию по требованиям ФСБУ 28?\n\n\
1️⃣ Один раз в три года\n\
2️⃣ Не реже 1 раза в год\n\
3️⃣ По распоряжению руководителя"
    options = [
        InlineKeyboardButton(text="1️⃣", callback_data="q4_1"),
        InlineKeyboardButton(text="2️⃣", callback_data="q4_2"),
        InlineKeyboardButton(text="3️⃣", callback_data="q4_3")
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[options])
    await message.edit_text(question, reply_markup=keyboard)
    await state.set_state(AccountantStates.TestQ4)


@accountant_router.callback_query(AccountantStates.TestQ4)
async def answer_test_q5(callback_query: types.CallbackQuery, state: FSMContext):
    user_choice = callback_query.data.split('_')[1]
    user_data['q4'] = user_choice
    await state.update_data(q4=user_choice)
    await callback_query.answer()
    await finish_test(callback_query.message, state)


# Завершение теста и подсчет результатов
async def finish_test(message: types.Message, state: FSMContext):
    data = await state.get_data()

    # Подсчет результатов
    score = 0
    for i in range(1, 5):
        if user_data.get(f'q{i}') == correct_answers[str(i)]:
            score += 1

        # Создаем клавиатуру с кнопкой запроса контакта
    contact_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Поделиться контактом ✅", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    # Формируем результат с инлайн-кнопкой
    result_text = (
        f"Тест завершен! Вы набрали {score} из 4 баллов.\n\n"
        "🙏 Спасибо за твое время и интерес к нашему бренду!\n"
        "Пожалуйста оставьте свои контактные данные нажав на кнопку \"Поделиться контактом\" и мы свяжемся с тобой в ближайшее время.\n\n"
        "Если у тебя возникнут дополнительные вопросы, не стесняйся их задавать нашему HR!\n\n"
        "Контакт: @polyyybbr"
    )

    # Отправляем сообщение с результатом и кнопкой
    await message.answer(
        result_text,
        reply_markup=contact_keyboard
    )

    # Устанавливаем состояние для ожидания контакта
    await state.set_state(AccountantStates.GET_CONTACT)
    await state.update_data(test_score=score)


@accountant_router.message(AccountantStates.GET_CONTACT, F.contact)
async def get_contact_after_test(message: types.Message, state: FSMContext):
    contact = message.contact
    data = await state.get_data()

    # Сохраняем все данные в БД
    database.save_user_data({
        **data,
        'phone_number': contact.phone_number,
        'telegram_user_id': contact.user_id,
        'first_name': contact.first_name,
        'last_name': contact.last_name,
        'chat_id': message.chat.id,
        'username': message.chat.username,
        'completed_at': datetime.now().isoformat()
    })

    await message.answer(
        "✅ Спасибо! Все данные успешно сохранены.\n"
        "Мы свяжемся с вами в ближайшее время!",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()


@accountant_router.message(AccountantStates.GET_CONTACT)
async def contact_not_provided(message: types.Message):
    await message.answer(
        "❌ Необходимо поделиться контактом для завершения процесса",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Поделиться контактом ✅", request_contact=True)]],
            resize_keyboard=True
        )
    )