import telebot
from config import TOKEN

bot = telebot.TeleBot(7397871713:AAHi28Ocb2a4pDjW1S_97VHfBgYJ6gMzEkU)


@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup()
    button_save = telebot.types.InlineKeyboardButton(
        text="Написать в поддержку")
    keyboard.add(button_save)
    bot.send_message(chat_id,
                     'Добро пожаловать в бота сбора обратной связи',
                     reply_markup=keyboard)
    with open('feedback.jpeg', 'rb') as file:
        photo = file.read()
    bot.send_photo(chat_id, photo)


@bot.message_handler(
    func=lambda message: message.text == 'Написать в поддержку')
def write_to_support(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Введите своё имя')
    users[chat_id] = {}
    bot.register_next_step_handler(message, save_username)


def save_username(message):
    chat_id = message.chat.id
    name = message.text
    users[chat_id]['name'] = name
    bot.send_message(chat_id, f'Отлично, {name}. Теперь укажи свою фамилию')
    bot.register_next_step_handler(message, save_surname)


def save_surname(message):
    chat_id = message.chat.id
    surname = message.text
    users[chat_id]['surname'] = surname
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_save = telebot.types.InlineKeyboardButton(text="Сохранить",
                                                     callback_data='save_data')
    button_change = telebot.types.InlineKeyboardButton(text="Изменить",
                                                     callback_data='change_data')
    keyboard.add(button_save, button_change)

    bot.send_message(chat_id, f'Сохранить данные?', reply_markup=keyboard)


@bot.message_handler(commands=['who_i'])
def who_i(message):
    chat_id = message.chat.id
    name = users[chat_id]['name']
    surname = users[chat_id]['surname']
    bot.send_message(chat_id, f'Вы: {name} {surname}')


@bot.callback_query_handler(func=lambda call: call.data == 'save_data')
def save_btn(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.answer_callback_query(call.id, text="Данные сохранены")
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    bot.send_message(chat_id, 'Введите текст отзыва: ')
    bot.register_next_step_handler(message, send_feedback_administrators)


def send_feedback_administrators(message):
    feedback = message.text
    user = users[message.chat.id]
    name = user['name']
    surname = user['surname']
    for admin_chat_id in administrators:
        bot.send_message(admin_chat_id,
                         f'{surname} {name} оставил отзыв: {feedback}')


@bot.callback_query_handler(func=lambda call: call.data == 'change_data')
def save_btn(call):
 message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text='Изменение данных!')
    write_to_support(message)


if __name__ == '__main__':
    print('Бот запущен!')
    bot.infinity_polling()
