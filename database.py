# database.py

from pymongo import MongoClient

# Установите соединение с MongoDB
client = MongoClient('localhost', 27017)

# Доступ к базе данных 'hr_bot'
db = client['hr_bot']

# Доступ к коллекции 'manager_mp'
collection = db['manager_mp']


def save_user_data(user_data):
    """Сохраняет данные пользователя в коллекцию MongoDB."""
    collection.insert_one(user_data)


def user_exists(user_id):
    """Проверяет, есть ли пользователь в базе данных."""
    return collection.find_one({'user_id': user_id}) is not None
