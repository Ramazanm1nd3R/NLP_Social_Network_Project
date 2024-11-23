
# 📊 Reddit Data Collection and Analysis Project

Link to kaggle - https://www.kaggle.com/datasets/ramazanospan/analysis-of-popular-reddit-posts-20202024

This project provides tools, scripts, and datasets to analyze Reddit posts from various time periods and subreddits. It is designed for tasks such as predicting post popularity, analyzing sentiment, and exploring engagement patterns across Reddit.

---

## 🚀 Overview
This project offers:
- **Scripts** to collect data from Reddit using the Reddit API (PRAW).
- **Multiple datasets** containing both popular and non-popular posts, enabling diverse analysis.
- **Tools for analysis**, including sentiment detection, engagement trends, and visualization.

---

## 📝 Datasets
The project includes datasets collected with various methods:
1. **All posts**: A comprehensive dataset containing a mix of popular and less popular posts.
2. **Popular posts**: Focused on posts with high engagement (e.g., high scores or comments).
3. **Custom datasets**: Created based on specific criteria (e.g., by subreddit, time period, or content type).

Each dataset includes the following columns:

| Column Name     | Description                                      |  
|------------------|--------------------------------------------------|  
| `Text`          | Full text of the Reddit post (title + content).  |  
| `Score`         | Total upvotes (likes) the post received.         |  
| `Comments`      | Number of comments on the post.                  |  
| `Timestamp`     | Date and time the post was published.            |  
| `URL`           | The link to the original post or media.          |  
| `Sentiment`     | Sentiment of the text (`Positive`, `Neutral`, `Negative`). |  
| `Day_of_Week`   | Day of the week the post was published.          |  
| `Time_of_Day`   | Time of day the post was published (`Morning`, `Afternoon`, `Evening`, `Night`). |  
| `Media_Type`    | Type of post content (`Text`, `Image`, `Video`). |

---

## 📈 Applications
This project can be used for:
1. **Machine Learning**:
   - Predict `Score` or `Comments` using features like `Text`, `Sentiment`, and `Time_of_Day`.
   - Classify posts based on sentiment or content type (`Media_Type`).
2. **Data Analysis**:
   - Study patterns of user engagement across different times and days.
   - Explore the impact of `Sentiment` on post popularity.
3. **NLP (Natural Language Processing)**:
   - Perform sentiment analysis.
   - Analyze trends in text data from Reddit.

---

## 🏗️ Project Structure
```
NLP_Social_Network_Project/
│
├── datasets/
│   ├── reddit_posts_all_time.csv                
│   ├── reddit_posts_popularity_mixed.csv        
│   └── reddit_posts_all_time_with_crossposts.csv
│
├── new_func/
│   ├── add_retweets.py                 # Script to process retweet data
│   └── all_posts_famous_and_new.py     # Script to combine different data sources
│
├── notebooks/
│   └── analysis.ipynb                  # Jupyter or other notebook for data analysis
│
├── .env                                # Environment variables
├── data_extract.py                     # Main data extraction script
├── README.md                           # Project documentation
├── requirements.txt                    # Python dependencies
└── project.pdf                         # Project report
```

---

## ⚙️ How to Use

1. Clone the repository:

   ```bash
   git clone https://github.com/Ramazanm1nd3R/NLP_Social_Network_Project.git
   cd NLP_Social_Network_Project
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure the `.env` file with your Reddit API credentials:
   ```plaintext
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USER_AGENT=your_user_agent
   ```

4. Collect data using the `data_extract.py` script:
   ```bash
   python data_extract.py
   ```

5. Explore the datasets using the provided Jupyter notebooks.

---

## 🎨 Example Analysis
Here are some ideas for analysis using the datasets:
- **Predict post engagement**: Use machine learning to predict `Score` or `Comments`.
- **Time-based trends**: Explore how engagement varies by `Day_of_Week` and `Time_of_Day`.
- **Sentiment analysis**: Study the relationship between `Sentiment` and post popularity.
- **Content type impact**: Investigate how `Media_Type` influences engagement.

---

## 📄 License
This project is licensed under the **Creative Commons Attribution 4.0 (CC BY 4.0)** license. You are free to use, share, and adapt the datasets and code with proper attribution.

---

## 🙌 Acknowledgements
- **Reddit API (PRAW)**: For providing easy access to Reddit data.
- The Kaggle and GitHub communities for inspiring this project.