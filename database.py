# database.py
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['hr_bot']

# Используем общую коллекцию для всех вакансий
collection = db['applicants']  # Новая коллекция


def save_user_data(user_data):
    collection.insert_one(user_data)


def user_exists(user_id, vacancy):
    """Проверяет, проходил ли пользователь конкретную вакансию"""
    return collection.find_one({'user_id': user_id, 'vacancy': vacancy}) is not None
