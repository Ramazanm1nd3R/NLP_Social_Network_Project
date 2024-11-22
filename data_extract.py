import praw
import csv
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

# === Загрузка переменных из .env ===
load_dotenv()

# Настройка API Reddit
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# Выбираем сабреддит и временной фильтр
subreddit = reddit.subreddit("all")  # Укажи нужный сабреддит
time_filter = "year"  # За последний год
limit = 1000  # Максимальное количество постов за запрос

# Сбор данных
data = []
print("Сбор данных начат...")

for post in subreddit.top(time_filter=time_filter, limit=limit):
    title = post.title or ""
    selftext = post.selftext or ""
    full_text = f"{title} {selftext}".strip()
    score = post.score
    num_comments = post.num_comments
    timestamp = datetime.fromtimestamp(post.created_utc, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    media_type = "Image" if post.url.endswith(('.jpg', '.png', '.gif')) else \
                 "Video" if post.url.endswith(('.mp4', '.mov')) else \
                 "Text"

    # Добавляем данные в список
    data.append([full_text, score, num_comments, timestamp, media_type])

    # Промежуточный статус
    if len(data) % 100 == 0:
        print(f"Собрано {len(data)} постов...")

# === Сохранение данных ===
output_file = "reddit_posts_year.csv"
print(f"Сохранение данных в {output_file}...")

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Text", "Score", "Comments", "Timestamp", "Media_Type"])
    writer.writerows(data)

print(f"Сбор завершен: всего {len(data)} постов.")
