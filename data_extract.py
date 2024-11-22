import praw
import csv
import emoji
from textblob import TextBlob
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import os
import time
import calendar

# === Загрузка переменных из .env ===
load_dotenv()

# Настройка API Reddit
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# === Вспомогательные функции ===

# Проверка наличия эмодзи в тексте
def contains_emoji(text):
    return any(emoji.is_emoji(char) for char in text)

# Анализ тональности текста
def get_sentiment(text):
    analysis = TextBlob(text)
    return "Positive" if analysis.sentiment.polarity > 0 else "Negative" if analysis.sentiment.polarity < 0 else "Neutral"

# === Определение временного диапазона ===

# Сегодняшняя дата
today = datetime.now()

# Первый день текущего месяца
first_day_this_month = datetime(today.year, today.month, 1)

# Первый день прошлого месяца
first_day_last_month = first_day_this_month - timedelta(days=1)
first_day_last_month = datetime(first_day_last_month.year, first_day_last_month.month, 1)

# Определение Unix timestamps
start_timestamp = int(first_day_last_month.timestamp())  # Начало прошлого месяца
end_timestamp = int(first_day_this_month.timestamp())    # Начало текущего месяца

# === Сбор данных ===
max_posts = 500  # Цель: 500 строк
data = []

# Выбираем сабреддит
subreddit = reddit.subreddit("all")  # Можешь указать конкретный сабреддит, например, "technology"

# Начальный статус
print("Сбор данных начат...")
current_timestamp = int(time.time())  # Текущее время

while len(data) < max_posts and current_timestamp > start_timestamp:
    for post in subreddit.new(limit=100):  # Получаем новые посты порциями по 100
        if post.created_utc < start_timestamp:  # Игнорируем посты, которые старше нужного диапазона
            current_timestamp = post.created_utc  # Обновляем временной предел
            break

        if post.created_utc >= end_timestamp:  # Пропускаем посты, которые уже из текущего месяца
            continue

        # Извлечение текста
        title = post.title or ""
        selftext = post.selftext or ""
        full_text = f"{title} {selftext}".strip()  # Сочетание заголовка и текста поста

        # Извлечение данных
        score = post.score
        num_comments = post.num_comments
        timestamp = datetime.fromtimestamp(post.created_utc, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        emoji_flag = 1 if contains_emoji(full_text) else 0
        sentiment = get_sentiment(full_text)
        word_count = len(full_text.split())
        media_type = "Image" if post.url.endswith(('.jpg', '.png', '.gif')) else \
                     "Video" if post.url.endswith(('.mp4', '.mov')) else \
                     "Text"

        # Добавление данных в список
        data.append([full_text, score, num_comments, timestamp, emoji_flag, sentiment, word_count, media_type])

    # Промежуточный статус
    print(f"Собрано {len(data)} постов...")

    # Задержка для предотвращения превышения лимитов API
    time.sleep(1)

# === Сохранение данных ===
output_file = "reddit_posts.csv"
print(f"Сохранение данных в {output_file}...")

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Text", "Likes", "Comments", "Timestamp", "Contains_Emoji", "Sentiment", "Word_Count", "Media_Type"])
    writer.writerows(data)

print(f"Сбор завершен: всего {len(data)} постов.")
