import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

from bot import dp, bot
# Импортируем роутер из файла менеджера
from vacancy.manager import manager_router
from vacancy.accountant import accountant_router

# Стартовая клавиатура
start_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        # [InlineKeyboardButton(text="Менеджер по WB", callback_data="vacancy_manager")],
        [InlineKeyboardButton(text="Заместитель главного бухгалтера", callback_data="vacancy_accountant")]
    ]
)


# Обработчик команды /start
@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! 👋\n\n"
        "Мы ищем сотрудников в команду бренда MissYourKiss\n\n"
        "Выберите вакансию для ознакомления:",
        reply_markup=start_inline_keyboard
    )


# Подключение роутеров
dp.include_router(accountant_router)
dp.include_router(manager_router)


# Список администраторов
ADMIN_IDS = [615742233]


# В обработчике команды /send
@dp.message(Command('send'))
async def send_to_user(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ Недостаточно прав")
        return

    try:
        # Парсим аргументы с учетом экранирования
        args = message.text.split(maxsplit=2)
        user_id = int(args[1])
        raw_text = args[2]

        # Обрабатываем экранирование
        text = raw_text.replace('\\n', '\n').replace('\\t', '\t')

        await bot.send_message(chat_id=user_id, text=text)
        await message.answer(f"✅ Сообщение отправлено пользователю {user_id}")

    except IndexError:
        await message.answer("❌ Неверный формат команды\nПример: /send 123456 Привет\\nКак дела?")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")


# Добавьте вызов в main()
async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
