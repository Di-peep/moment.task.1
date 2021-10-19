from bot_object import bot
from user_object import User

from validator import check_name
from markup import main_menu_markup

from state_handler import get_state_and_process


users = {}


@bot.message_handler(commands=['start'])
def start_registration(message):
    chat_id = message.chat.id

    if chat_id in users:
        bot.send_message(chat_id, "Ви авторизовані\nБажаєте зайняти слот?", reply_markup=main_menu_markup())

    else:
        msg = bot.send_message(chat_id, "Вітаю!\nВведіть ваше ім'я:")
        bot.register_next_step_handler(msg, add_username)


def add_username(message):
    chat_id = message.chat.id

    if check_name(message.text):
        users[chat_id] = User(message.text)
        bot.send_message(chat_id,
                         f"Нове ім'я <b>{users[chat_id].name}</b> зареєстровано!",
                         parse_mode='html',
                         reply_markup=main_menu_markup())
    else:
        msg = bot.send_message(chat_id, "Введено некоректне ім'я.\nСпробуйте ще раз")
        bot.register_next_step_handler(msg, add_username)


@bot.message_handler(content_types=["text"])
def handle_message(message):
    try:
        chat_id = message.chat.id
        user = users[chat_id]

        get_state_and_process(message, user)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    bot.remove_webhook()
    bot.polling(none_stop=True)
