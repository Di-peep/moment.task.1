import states
from user_object import User


states = {
    'main_menu': states.main_menu,
    'settings_menu': states.settings_menu,
    'change_name': states.change_name,
    'day_slots': states.day_slots,
    'hours_slots': states.hours_slots
}


def get_state_and_process(message, user: User, is_entry=False):
    if user.state in states:
        change_state, state_to_change_name = states[user.state](message, user, is_entry)
    else:
        user.state = 'main_menu'
        change_state, state_to_change_name = states[user.state](message, user, is_entry)
    if change_state:
        go_to_state(message, state_to_change_name, user)


def go_to_state(message, state_name: str, user: User):
    user.state = state_name
    get_state_and_process(message, user, is_entry=True)
