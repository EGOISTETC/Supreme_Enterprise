import time

from pyrogram.types import InputPhoneContact
from pyrogram import Client
import json
import tempfile

api_id = 25676335  # Введите свой api_id
api_hash = "abc57a2568fc8244725b67ee099f416f"  # Введите свой api_hash
app = Client("Scanner", api_id=api_id, api_hash=api_hash)


def get_chat_id(phone_num):
    temp_contact_name = tempfile.NamedTemporaryFile().name.split('\\')[-1]
    good_res = []
    with app:
        app.import_contacts([InputPhoneContact(phone=phone_num, first_name=temp_contact_name)])

        contacts = app.get_contacts()
        for contact in contacts:
            contact_data = json.loads(str(contact))
            if contact_data['first_name'] == temp_contact_name:
                good_res.append(contact_data)
                app.delete_contacts(contact_data['id'])
        time.sleep(1)
    try:
        good_res = good_res[0]['username']
    except Exception:
        good_res = None
    return good_res


def parse_numbers_from_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()


def main():
    numbers_file = "phone.txt"  # Путь к файлу с номерами
    for phone_num in parse_numbers_from_file(numbers_file):
        time.sleep(1)
        chat_id = get_chat_id(phone_num)
        print(f"Phone number: {phone_num}, Chat ID: {chat_id}")


if __name__ == "__main__":
    main()
