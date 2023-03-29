from flask import Flask, render_template, request
import os
import nltk
from nltk.corpus import stopwords
from collections import Counter
import requests

app = Flask(__name__)


@app.route("/commits/<username>/<date>")
def get_commits(username, date):
    url = f"https://api.github.com/search/commits?q=author:{username}&sort=author-date&order=desc&page=1"
    params = {"since": date, "until": date}
    response = requests.get(
        url,
        params=params,
        headers={"Authorization": f"Bearer {os.getenv('GITHUB_API_KEY')}"},
    )
    if response.ok:
        commits = response.json()
        print(commits)
        # messages = [commit["commit"]["message"] for commit in commits]
        # stop_words = set(stopwords.words("english"))
        # words = [
        #     word
        #     for message in messages
        #     for word in message.split()
        #     if word.lower() not in stop_words
        # ]
        # word_counts = Counter(words)
        # most_common = word_counts.most_common(10)
        # summary = ", ".join([f"{word}: {count}" for word, count in most_common])
        # return summary
    else:
        return "Error retrieving commits"
