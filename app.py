from flask import Flask, render_template, request
import os
import nltk
from nltk.corpus import stopwords
from collections import Counter
import requests
from github import Github
from datetime import datetime, timedelta

app = Flask(__name__)

g = Github(login_or_token=os.getenv("GITHUB_API_KEY"))


@app.route("/commits/<username>/<date>")
def get_commits(username, date):
    user = g.get_user(username)
    repos = user.get_repos()

    date_string = "29-03-2023"
    date_format = "%d-%m-%Y"

    date = datetime.strptime(date_string, date_format).date()

    commit_list = []

    print(
        datetime.combine(date, datetime.min.time()),
        datetime.combine(date + timedelta(days=1), datetime.min.time()),
    )
    for repo in repos:
        try:
            commits = repo.get_commits(
                author=username,
                since=datetime.combine(date, datetime.min.time()),
                until=datetime.combine(date + timedelta(days=1), datetime.min.time()),
            )
            for commit in commits:
                commit_list.append(commit.commit.message)
        except:
            print("An error occured")

    return commit_list
