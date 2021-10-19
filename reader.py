import json


def read_json():
    with open("slots.json", "r") as read_file:
        data = json.load(read_file)

        return data


def simple_write_json(data):
    with open("slots.json", "w") as write_file:
        json.dump(data, write_file)


def write_user_id_to_json(user_id, day, hour):
    slots = read_json()

    slots[day][hour] = user_id

    simple_write_json(slots)


def delete_user_id_from_json(user_id):
    slots = read_json()

    for key, item in slots.items():
        for key_, item_ in item.items():
            if user_id == item_:
                slots[key][key_] = ""
                simple_write_json(slots)
                return


def check_user_in_json(user_id):
    slots = read_json()

    for key, item in slots.items():
        if user_id in item.values():
            return True

    return False


def find_user_slot_in_json(user_id):
    slots = read_json()

    for key, item in slots.items():
        for key_, item_ in item.items():
            if user_id == item_:
                return key, key_
