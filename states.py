from markup import *
from reader import check_user_in_json, write_user_id_to_json, \
                   delete_user_id_from_json, read_json, find_user_slot_in_json

from validator import check_name
from bot_object import bot


TEXT_ERROR = 'Будь ласка, використовуйте кнопки'
LOST_DATA = 'З вашими данними щось трапилось...'


# done
def main_menu(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id,
            "Головне меню:",
            reply_markup=main_menu_markup()
            )
    else:
        if message.text == "Нагадати мій слот":
            if check_user_in_json(message.chat.id):
                day, hour = find_user_slot_in_json(message.chat.id)

                bot.send_message(message.chat.id,
                                 f"<i>Ваш слот зареєстровано на:\n{day} {hour}</i>\n",
                                 parse_mode='html')

            else:
                bot.send_message(message.chat.id, "Ви ще не зайняли слот")

        elif message.text == "Меню змін":
            return True, 'settings_menu'

        elif message.text == "Переглянути вільні слоти":
            return True, 'day_slots'

        else:
            bot.send_message(message.chat.id, TEXT_ERROR)

    return False, ''


# done
def settings_menu(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id,
            "Меню змін:",
            reply_markup=settings_menu_markup()
            )
    else:
        if message.text == "Назад":
            return True, 'main_menu'

        elif message.text == "Відмовитись від слоту":
            if user.day and user.hour:
                delete_user_id_from_json(message.chat.id)

                bot.send_message(message.chat.id,
                                 f"<i>Вашу реєстрацію на слот <i>{user.day} {user.hour}</i> скасовано</i>",
                                 parse_mode='html')
                user.day = None
                user.hour = None

            else:
                bot.send_message(message.chat.id, "Ви не записані на жоден слот")

        elif message.text == "Редагувати ім'я":
            return True, 'change_name'

        else:
            bot.send_message(message.chat.id, TEXT_ERROR)

    return False, ''


# done
def change_name(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id,
            f"Нині ваше ім'я: <i>{user.name}</i>\nНа яке бажаєте змінити ім'я?",
            reply_markup=change_name_markup(),
            parse_mode='html'
            )
    else:
        if message.text == 'Назад':
            return True, 'settings_menu'

        elif check_name(message.text):
            user.name = message.text
            bot.send_message(message.chat.id,
                             f"Збережено нове ім'я: <i>{user.name}</i>",
                             parse_mode='html'
                             )
            return True, 'settings_menu'

        else:
            bot.send_message(message.chat.id, TEXT_ERROR)

    return False, ''


def day_slots(message, user, is_entry=False):
    slots = read_json()
    if is_entry:
        bot.send_message(
            message.chat.id,
            "Який день вас влаштовує?",
            reply_markup=day_slots_markup(slots)
            )
    else:
        if message.text == 'Назад':
            user.day = None
            return True, 'main_menu'

        elif message.text in slots:
            user.day = message.text
            return True, 'hours_slots'

        else:
            bot.send_message(message.chat.id, TEXT_ERROR)

    return False, ''


def hours_slots(message, user, is_entry=False):
    slots = read_json()
    if is_entry:
        bot.send_message(
            message.chat.id,
            "На яку годину вам зручно?",
            reply_markup=hours_slots_markup(slots[user.day])
        )
    else:
        if message.text == 'Назад':
            user.hour = None
            return True, 'day_slots'

        elif message.text in slots[user.day] and slots[user.day][message.text] == "":
            if check_user_in_json(message.chat.id):
                bot.send_message(message.chat.id, "Вашу попередню реєстрацію скасовано")
                delete_user_id_from_json(message.chat.id)

                user.hour = message.text
                write_user_id_to_json(message.chat.id, user.day, user.hour)
                bot.send_message(message.chat.id,
                                 f"<i>Вашу реєстрацію на слот <i>{user.day} {user.hour}</i> збережено</i>",
                                 parse_mode='html')
                return True, 'main_menu'

            else:
                user.hour = message.text
                write_user_id_to_json(message.chat.id, user.day, user.hour)

                bot.send_message(message.chat.id,
                                 f"<i>Вашу реєстрацію на слот <i>{user.day} {user.hour}</i> збережено</i>",
                                 parse_mode='html')
                return True, 'main_menu'

        else:
            bot.send_message(message.chat.id, TEXT_ERROR)

    return False, ''
