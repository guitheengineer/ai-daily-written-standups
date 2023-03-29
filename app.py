from flask import Flask, render_template, request
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


@app.route("/")
def index():
    article_content = ""

    result = ""

    if article_content:
        response = openai.Completion.create(
            model="text-curie-001",
            prompt=f"Write a keyword for the following article:",
            max_tokens=1000,
            temperature=0.75,
        )
        result = response.choices[0].text

    return render_template("index.html", result=result)
