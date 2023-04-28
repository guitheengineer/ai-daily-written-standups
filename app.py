from flask import Flask, request, render_template
import os
from github import Github
from datetime import datetime, timedelta
import os
import openai


app = Flask(__name__)

g = Github(login_or_token=os.getenv("GITHUB_API_KEY"))


@app.route("/")
def index():
    username = request.args.get("username")
    date = request.args.get("date")
    api_key = request.args.get("api-key")
    commit_list = []
    text_result = ""
    if username and date and api_key:
        openai.api_key = api_key
        user = g.get_user(username)
        repos = user.get_repos()

        date_string = date
        date_format = "%Y-%m-%d"

        date = datetime.strptime(date_string, date_format).date()

        for repo in repos:
            try:
                commits = repo.get_commits(
                    author=username,
                    since=datetime.combine(date, datetime.min.time()),
                    until=datetime.combine(
                        date + timedelta(days=1), datetime.min.time()
                    ),
                )

                for commit in commits:
                    commit_list.append(commit.commit.message)
            except:
                print("An error occured")

        if commit_list:
            text_result = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Make a written standup based on these commits: {commit_list}, for this date: {date} \n\My written standup: ",
                temperature=0,
                max_tokens=64,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )["choices"][0]["text"]

    return render_template(
        "index.html",
        text_result=text_result,
        username=username,
        api_key=api_key,
        date=date,
    )
