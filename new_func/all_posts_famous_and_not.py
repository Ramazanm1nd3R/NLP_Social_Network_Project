import praw
import csv
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
import hashlib
import time
from textblob import TextBlob

# === Загрузка переменных из .env ===
load_dotenv()

# Настройка API Reddit
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# === Функция для хэширования постов ===
def generate_hash(post_text, timestamp):
    unique_string = f"{post_text}-{timestamp}"
    return hashlib.sha256(unique_string.encode('utf-8')).hexdigest()

# === Функция для анализа тональности текста ===
def get_sentiment(text):
    analysis = TextBlob(text)
    return "Positive" if analysis.sentiment.polarity > 0 else \
           "Negative" if analysis.sentiment.polarity < 0 else "Neutral"

# === Параметры сбора ===
subreddit = reddit.subreddit("all")
max_posts = 50000  # Общее количество постов
batch_limit = 1000  # Максимум постов за один запрос
output_file = "reddit_posts_popularity_mixed.csv"
collected_hashes = set()

# Проверяем, существует ли уже файл и загружаем существующие хэши
if os.path.exists(output_file):
    with open(output_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            post_hash = generate_hash(row[0], row[3])
            collected_hashes.add(post_hash)

print(f"Загружено {len(collected_hashes)} уникальных постов из существующего файла.")

# === Функция сбора постов ===
def collect_posts(posts, data, method):
    for post in posts:
        title = post.title or ""
        selftext = post.selftext or ""
        full_text = f"{title} {selftext}".strip()
        score = post.score
        num_comments = post.num_comments
        timestamp = datetime.fromtimestamp(post.created_utc, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        url = post.url
        sentiment = get_sentiment(full_text)

        # Вычисляем день недели и время суток
        created_time = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)
        day_of_week = created_time.strftime('%A')
        hour = created_time.hour
        time_of_day = (
            "Night" if 0 <= hour < 6 else
            "Morning" if 6 <= hour < 12 else
            "Afternoon" if 12 <= hour < 18 else "Evening"
        )

        media_type = "Image" if post.url.endswith(('.jpg', '.png', '.gif')) else \
                     "Video" if post.url.endswith(('.mp4', '.mov')) else "Text"

        post_hash = generate_hash(full_text, timestamp)
        if post_hash in collected_hashes:
            continue  # Пропускаем дубликаты

        # Добавляем уникальный пост
        data.append([full_text, score, num_comments, timestamp, url, sentiment,
                     day_of_week, time_of_day, media_type, method])
        collected_hashes.add(post_hash)

# === Основной процесс ===
data = []
methods = ['new', 'top', 'controversial', 'rising']
time_filters = ['day', 'week', 'month', 'year']

print("Сбор данных начат...")
for method in methods:
    for time_filter in time_filters:
        print(f"Сбор данных ({method}, {time_filter})...")
        if method == 'new':
            posts = subreddit.new(limit=batch_limit)
        elif method == 'top':
            posts = subreddit.top(time_filter=time_filter, limit=batch_limit)
        elif method == 'controversial':
            posts = subreddit.controversial(time_filter=time_filter, limit=batch_limit)
        elif method == 'rising':
            posts = subreddit.rising(limit=batch_limit)
        else:
            continue

        collect_posts(posts, data, method)

        # Сохраняем данные в файл каждые 1000 постов
        if len(data) >= batch_limit:
            with open(output_file, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if os.stat(output_file).st_size == 0:
                    writer.writerow(["Text", "Score", "Comments", "Timestamp", "URL", "Sentiment",
                                     "Day_of_Week", "Time_of_Day", "Media_Type", "Method"])
                writer.writerows(data)
            print(f"Добавлено {len(data)} новых постов в файл.")
            data = []  # Очищаем временное хранилище

    # Промежуточный статус
    print(f"Собрано {len(collected_hashes)} уникальных постов.")

    # Если собрано достаточно постов, прерываем процесс
    if len(collected_hashes) >= max_posts:
        print("Достигнуто максимальное количество постов.")
        break

print(f"Сбор завершен: всего {len(collected_hashes)} уникальных постов.")
