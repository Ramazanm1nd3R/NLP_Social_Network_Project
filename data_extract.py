import praw
import csv
import emoji
from textblob import TextBlob
from datetime import datetime
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

# === Вспомогательные функции ===

# Проверка наличия эмодзи в тексте
def contains_emoji(text):
    return any(char in emoji.UNICODE_EMOJI['en'] for char in text)

# Анализ тональности текста
def get_sentiment(text):
    analysis = TextBlob(text)
    return "Positive" if analysis.sentiment.polarity > 0 else "Negative" if analysis.sentiment.polarity < 0 else "Neutral"

# === Сбор данных ===

# Выбираем сабреддит и лимит данных
subreddit = reddit.subreddit("all")  # Можешь указать конкретный сабреддит, например, "technology"
max_posts = 50000  # Цель: 50,000 строк
data = []

# Сбор постов
print("Сбор данных начат...")
for post in subreddit.new(limit=max_posts):  # Получаем новые посты
    # Извлечение текста
    title = post.title
    selftext = post.selftext
    full_text = f"{title} {selftext}"  # Сочетание заголовка и текста поста

    # Извлечение данных
    score = post.score
    num_comments = post.num_comments
    timestamp = datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S')
    emoji_flag = 1 if contains_emoji(full_text) else 0
    sentiment = get_sentiment(full_text)
    word_count = len(full_text.split())
    media_type = "Image" if post.url.endswith(('.jpg', '.png', '.gif')) else \
                 "Video" if post.url.endswith(('.mp4', '.mov')) else \
                 "Text"

    # Добавление данных в список
    data.append([full_text, score, num_comments, timestamp, emoji_flag, sentiment, word_count, media_type])

    # Промежуточный статус
    if len(data) % 1000 == 0:
        print(f"Собрано {len(data)} постов...")

# === Сохранение данных ===
output_file = "reddit_posts.csv"
print(f"Сохранение данных в {output_file}...")

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Text", "Likes", "Comments", "Timestamp", "Contains_Emoji", "Sentiment", "Word_Count", "Media_Type"])
    writer.writerows(data)

print(f"Сбор завершен: всего {len(data)} постов.")
