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
    """Создает уникальный хэш для поста по тексту и временной метке."""
    unique_string = f"{post_text}-{timestamp}"
    return hashlib.sha256(unique_string.encode('utf-8')).hexdigest()

# === Функция для анализа тональности текста ===
def get_sentiment(text):
    analysis = TextBlob(text)
    return "Positive" if analysis.sentiment.polarity > 0 else \
           "Negative" if analysis.sentiment.polarity < 0 else "Neutral"

# === Параметры сбора ===
subreddit = reddit.subreddit("all")  # Укажите нужные сабреддиты
time_filter = "all"  # За все время
max_posts = 20000  # Ограничение на общее количество постов
batch_limit = 10000  # Ограничение на одну сессию
output_file = "reddit_posts_all_time.csv"
collected_hashes = set()  # Для хранения хэшей уникальных постов

# === Проверяем, существует ли уже файл и загружаем существующие хэши ===
if os.path.exists(output_file):
    with open(output_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            post_hash = generate_hash(row[0], row[3])
            collected_hashes.add(post_hash)

print(f"Загружено {len(collected_hashes)} уникальных постов из существующего файла.")

# === Сбор данных ===
print("Сбор данных начат...")
data = []  # Временное хранилище для текущей партии данных

while len(data) < batch_limit and len(collected_hashes) < max_posts:
    posts_collected = 0

    # Получаем топ постов
    posts = subreddit.top(time_filter=time_filter, limit=batch_limit)

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
                     "Video" if post.url.endswith(('.mp4', '.mov')) else \
                     "Text"

        # Генерируем хэш для проверки дубликатов
        post_hash = generate_hash(full_text, timestamp)
        if post_hash in collected_hashes:
            continue  # Пропускаем дубликаты

        # Добавляем уникальный пост в список
        data.append([full_text, score, num_comments, timestamp, url, sentiment, day_of_week, time_of_day, media_type])
        collected_hashes.add(post_hash)
        posts_collected += 1

        # Если достигли лимита на сессию, завершить сбор
        if len(data) >= batch_limit:
            print("Достигнуто ограничение в 1000 строк. Остановка.")
            break

    # Сохраняем данные в CSV файл
    if data:
        with open(output_file, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if os.stat(output_file).st_size == 0:
                writer.writerow(["Text", "Score", "Comments", "Timestamp", "URL", "Sentiment",
                                 "Day_of_Week", "Time_of_Day", "Media_Type"])
            writer.writerows(data)
        print(f"Добавлено {len(data)} новых постов в файл.")
        data = []  # Очищаем временное хранилище

    # Промежуточный статус
    print(f"Всего собрано уникальных постов: {len(collected_hashes)}")

    # Если за итерацию ничего не собрано, завершить процесс
    if posts_collected == 0:
        print("Больше нет доступных постов. Завершение.")
        break

    # Задержка для предотвращения превышения лимитов API
    time.sleep(1)

print(f"Сбор завершен: собрано 1000 постов. Для продолжения запустите скрипт заново.")
