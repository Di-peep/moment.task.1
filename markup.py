from telebot import types


def main_menu_markup():
    menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    menu_markup.row("Переглянути вільні слоти")
    menu_markup.row("Нагадати мій слот")
    menu_markup.row("Меню змін")
    return menu_markup


def settings_menu_markup():
    menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    menu_markup.row("Відмовитись від слоту")
    menu_markup.row("Редагувати ім'я")
    menu_markup.row("Назад")
    return menu_markup


def change_name_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Назад")
    return markup


def day_slots_markup(voc):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for key in voc:
        markup.row(key)

    markup.row("Назад")
    return markup


def hours_slots_markup(voc):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for key, item in voc.items():
        if item == "":
            markup.row(key)

    markup.row("Назад")
    return markup
