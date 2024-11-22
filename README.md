
# 📊 Reddit Post Popularity Dataset (2020–2024)

## 🚀 Overview
This project provides a dataset of Reddit posts collected from **2020 to 2024**. It includes posts from popular subreddits like `news`, `worldnews`, and `technology`, focusing on analyzing and predicting post popularity.

The dataset is designed for tasks like:
- **Predicting post popularity** (e.g., `Score`, `Comments`).
- **Analyzing sentiment** and its relationship with popularity.
- **Exploring trends** in user engagement based on time and content type.

---

## 📝 Dataset Features
The dataset contains **5248 rows** and the following columns:

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

## 📌 Example Row
Here is an example row from the dataset:

| Text                     | Score  | Comments | Timestamp           | URL                  | Sentiment | Day_of_Week | Time_of_Day | Media_Type |  
|--------------------------|--------|----------|---------------------|----------------------|-----------|-------------|-------------|------------|  
| Joe Biden elected...     | 365127 | 28319    | 2020-11-07 16:28:37 | https://example.com  | Neutral   | Saturday    | Afternoon   | Text       |

---

## 📈 Applications
This dataset can be used for:
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

## 📚 How the Data Was Collected
The data was collected using the official Reddit API (`PRAW`) and includes only public posts. Posts were filtered by subreddits:
- `news`
- `worldnews`
- `technology`

All collected data complies with Reddit's API usage policies.

---

## ⚙️ Tools & Technologies
- **Python**:
  - Libraries used: `praw`, `csv`, `datetime`, `textblob`, `emoji`, `hashlib`.
- **Reddit API (PRAW)**:
  - Used to fetch posts and metadata.
- **Natural Language Processing**:
  - `TextBlob` for sentiment analysis.
  - `emoji` for detecting emojis in the text.

---

## 🏗️ Project Structure
```
project/
│
├── reddit_posts_all_time.csv   # Dataset file
├── data_extract.py             # Script for collecting Reddit data
├── README.md                   # Project documentation (this file)
├── requirements.txt            # Python dependencies
└── notebooks/
    └── analysis.ipynb          # Example Jupyter notebook for dataset analysis
```

---

## 🔧 How to Run the Project

1. Clone this repository:

   ```bash
   git clone https://github.com/Ramazanm1nd3R/NLP_Social_Network_Project.git
   cd NLP_Social_Network_Project
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the data extraction script (optional):

   ```bash
   python data_extract.py
   ```

4. Explore the dataset using the provided Jupyter notebook (`analysis.ipynb`).

---

## 🎨 Example Analysis
Here are some ideas for analysis using this dataset:
- **Visualize the distribution of `Score` across different `Time_of_Day`.**
- **Analyze the most common sentiments across `Media_Type`.**
- **Study the effect of `Day_of_Week` on the number of `Comments`.**

---

## 📄 License
This project is licensed under the **Creative Commons Attribution 4.0 (CC BY 4.0)** license. You are free to use, share, and adapt the dataset with proper attribution.

---

## 🙌 Acknowledgements
- **Reddit API (PRAW)**: For providing an easy way to access Reddit data.
- The Kaggle community for inspiring this project.
