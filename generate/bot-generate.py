import random
import string
import telebot
import os

bot=telebot.TeleBot(os.environ.get('generate_bot'))

def escape_markdown(text):
    """
    Функция для экранирования специальных символов в тексте для форматирования MarkdownV2.
    """
    escape_chars = r'_*[]()~`>#+-=|{}.!' # Список символов, которые необходимо экранировать
    return ''.join('\\' + char if char in escape_chars else char for char in text)

@bot.message_handler(commands=['start'])
def start(message):
    """
    Обработчик команды /start. Отправляет пользователю приветственное сообщение и информацию о боте.
    """
    bot.send_message(message.chat.id, 'Hello! I am a bot that can generate random names and passwords. Use the /generate_nickname command to generate a name or the /generate_password command to generate a password.')

@bot.message_handler(commands=['generate_nickname'])
def generate_nickname(message):
    """
    Обработчик команды /generate_nickname. Генерирует случайное имя и отправляет его пользователю.
    """
    adjectives = ['adorable', 'adventurous', 'amazing', 'ambitious', 'amusing', 'awesome', 'brave', 'bright', 'calm', 'charming', 'cheerful', 'clever', 'confident', 'creative', 'daring', 'delightful', 'determined', 'eager', 'energetic', 'enthusiastic']
    animals = ['alligator', 'antelope', 'armadillo', 'baboon', 'badger', 'bat', 'bear', 'beaver', 'bee', 'bison', 'boar', 'buffalo', 'butterfly', 'camel', 'cat', 'cheetah', 'chicken', 'chimpanzee', 'cow', 'coyote']
    adjective = random.choice(adjectives)
    animal = random.choice(animals)
    nickname = f'{adjective}_{animal}'
    bot.send_message(message.chat.id, f'Your nickname:\n```\n{nickname}\n```', parse_mode='MarkdownV2')

@bot.message_handler(commands=['generate_password'])
def generate_password(message):
    """
    Обработчик команды /generate_password. Генерирует случайный пароль из 18 символов и отправляет его пользователю.
    """
    password_characters = string.ascii_letters + string.digits + string.punctuation # Символы, из которых может состоять пароль
    password = ''.join(random.choice(password_characters) for i in range(18)) # Генерация случайного пароля
    escaped_password = escape_markdown(password) # Экранирование специальных символов в пароле
    bot.send_message(message.chat.id, f'Your password:\n```\n{escaped_password}\n```', parse_mode='MarkdownV2') # Отправка пароля пользователю в формате monospace

@bot.message_handler(commands=['generate_port_number'])
def generate_port_number(message):
    """
    Обработчик команды /generate_port_number. Генерирует случайный пароль логический порт для TCP/UPD.
    """
    port = random.randint(49152, 65535)
    bot.send_message(message.chat.id, f'Random port number:\n```\n{port}\n```', parse_mode='MarkdownV2')

if os.environ.get('CI'):
    exit(0)

bot.polling() # Запуск бота