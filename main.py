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


async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
