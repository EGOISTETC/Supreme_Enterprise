import time
from telebot import TeleBot
import telebot
import json
import subprocess
import requests
from typing import List, Dict, Any
from threading import Thread
from time import sleep
from peewee import Model, SqliteDatabase, CharField, BooleanField, DateTimeField,fn
from telebot import types
from datetime import datetime



TOKEN = "7072077123:AAHt9Y4ECIO0dRIjeLE0K9Hbn2KYboTlsjI"
bot = TeleBot(TOKEN)
parse_running = True
commands_list = [
    ("/start", "Начать работу"),
]
db = SqliteDatabase('message.db')


class Message(Model):
    user_id = CharField()
    username = CharField()
    text = CharField()
    date = DateTimeField()

    class Meta:
        database = db

db.create_tables([Message])



@bot.message_handler(commands=['topMessage'])
def top_message_handler(message):
    top_message(message)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def save_message(message):
    try:
        Message.create(
            user_id=message.from_user.id,
            username=message.from_user.username,
            text=message.text,
            date=datetime.fromtimestamp(message.date)
        )
        print(Message)
    except Exception as e:
        print(f"Error saving message: {e}")




@bot.message_handler(commands=['topMessage'])
def top_message(message):
    try:
        # Extract start date, end date, and target user from the command
        chat_id = message.chat.id
        print(chat_id)
        command_parts = message.text.split()
        start_date = datetime.strptime(command_parts[1] + ' ' + command_parts[2], '%Y.%m.%d %H:%M')
        end_date = datetime.strptime(command_parts[3] + ' ' + command_parts[4], '%Y.%m.%d %H:%M')
        # Execute SQL query
        query = (
            "SELECT username, COUNT(id) AS message_count "
            "FROM message "
            "WHERE date BETWEEN ? AND ? "
            "GROUP BY user_id "
            "ORDER BY message_count DESC "
            "LIMIT 10"
        )
        top_users = Message.raw(query, start_date, end_date)

        # Prepare response message
        response_message = "Top message senders:\n"
        for user in top_users:
            response_message += f"User: @{user.username}, Message Count: {user.message_count}\n"

        bot.reply_to(message, response_message)

    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")


if __name__ == "__main__":
    bot.delete_webhook()
    bot.set_my_commands(commands_list)
    bot.polling()