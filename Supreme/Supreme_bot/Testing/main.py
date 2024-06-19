import time
from telebot import TeleBot
from telebot import types
import subprocess
import requests
from typing import List, Dict, Any
from threading import Thread
from peewee import Model, SqliteDatabase, CharField, BooleanField, DateTimeField
import json
from datetime import datetime

TOKEN = "6398235699:AAHTqX4ogHVyKaD0lle6ROCOE9Bfaf5QYBI"
bot = TeleBot(TOKEN)
parse_running = True
commands_list = [
    ("/starts", "Начать работу"),
    ("/statistic", "Показать статистику"),
    ("/stop", "Остановить парсинг"),
]
db = SqliteDatabase('posts.db')


class Post(Model):
    channel = CharField()
    content = CharField()
    url = CharField(unique=True)
    published = BooleanField(default=False)

    class Meta:
        database = db


class Message(Model):
    user_id = CharField()
    username = CharField()
    text = CharField()
    date = DateTimeField()

    class Meta:
        database = db


db.create_tables([Post, Message])


def collect_posts(channels: List[str], keywords: List[str]) -> List[Dict]:
    all_posts = []

    for channel in channels:
        with open(f"./tmp/{channel}.txt") as file:
            file_data = file.readlines()

        for line in file_data:
            try:
                post_data = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {str(e)}")
                continue

            links = [link for link in post_data.get('outlinks', []) if channel not in link]
            post_content = f"{post_data.get('content', '')}\n"

            if any(keyword.lower() in post_content.lower() for keyword in keywords):
                post_info = {'channel': channel, 'content': post_content, 'url': post_data.get('url', '')}
                all_posts.append(post_info)
    return all_posts


def upload_posts(num_posts: int, channels: List[str]):
    for channel in channels:
        command = f'snscrape --max-result {num_posts} --jsonl telegram-channel {channel} > ./tmp/{channel}.txt'
        subprocess.run(command, shell=True)


def read_input_file(file_path: str):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = {}
    for line in lines:
        key, value = line.strip().split('=')
        data[key] = value

    channels = data.get('Cannel_group', '').split(',')
    num_posts = int(data.get('nums_posts', '0'))
    keywords = data.get('key_word', '').split(',')
    target_channel = data.get('target_group', '').strip()
    return channels, num_posts, keywords, target_channel


def send_analytics_to_django(channel):
    query = (
        "SELECT COUNT(id) AS message_count "
        "FROM message "
    )
    top_users = Message.raw(query, )
    for i in top_users:
        message_counts = i.message_count

    query = (
        "SELECT COUNT(DISTINCT user_id) AS active_users_count "
        "FROM message "
    )
    result = Message.raw(query, )
    for i in result:
        all_member = i.active_users_count
    data = {
        'channel': channel,
        'messages_count': message_counts,
        'members_count': all_member,
        'keyword_matches': message_counts,
        'relevance': 0
    }

    response = requests.post('http://127.0.0.1:8000/update_analytics/', data=data)

    if response.status_code == 200:
        print('Аналитика успешно отправлена на Django приложение')
    else:
        print(f'Ошибка при отправке аналитики на Django: {response.status_code}')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    for cmd, desc in commands_list:
        markup.add(types.InlineKeyboardButton(desc, callback_data=cmd))
    bot.send_message(message.chat.id, "Доступные команды:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    command = call.data
    if command == '/statistic':
        bot.reply_to(call.message, "http://127.0.0.1:8000/stat")
    elif command == '/stop':
        stop_parse(call.message)


def post_already_exists(url: str) -> bool:
    return Post.select().where(Post.url == url).exists()


def save_post(channel: str, content: str, url: str):
    Post.create(channel=channel, content=content, url=url, published=False)


def publish_post(post_info: Dict[str, Any], target_channel: str):
    reply_message = f"Источник: {post_info['channel']}\n\n{post_info['content'][:90:1]}...\n\n"
    markup = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Перейти на ресурс", url=post_info['url'])
    markup.add(url_button)
    try:
        bot.send_message(target_channel, reply_message, reply_markup=markup)
        Post.update(published=True).where(Post.url == post_info['url']).execute()

        # Отправка данных аналитики на сервер Django
        print(post_info['channel'])
        send_analytics_to_django(post_info['channel'])

    except Exception as e:
        print('Получил пизды за частые запросы, жду 5 сек...',e)
        time.sleep(5)


def parse_channels():
    global parse_running
    while parse_running:
        channels, num_posts, keywords, target_channel = read_input_file('input_file.txt')
        upload_posts(num_posts, channels)
        posts = collect_posts(channels, keywords)

        for post_info in posts:
            if post_already_exists(post_info['url']):
                continue

            save_post(post_info['channel'], post_info['content'], post_info['url'])

            publish_post(post_info, target_channel)

        time.sleep(5)


@bot.message_handler(commands=['statistic'])
def send_welcome(message):
    bot.reply_to(message, "http://127.0.0.1:8000/stat")


@bot.message_handler(content_types=['document'])
def handle_document(message):
    global parse_running
    try:
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open('input_file.txt', 'wb') as new_file:
            new_file.write(downloaded_file)

        Thread(target=parse_channels).start()
        bot.reply_to(message, "Парсинг каналов начат.")

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")


@bot.message_handler(commands=['stop'])
def stop_parse(message):
    global parse_running
    parse_running = False
    bot.reply_to(message, "Парсинг каналов остановлен.")


if __name__ == "__main__":
    bot.delete_webhook()
    bot.set_my_commands(commands_list)
    bot.polling()
