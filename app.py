from flask import Flask, render_template, request
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


@app.route("/")
def index():
    body = request.args.to_dict()
    person_profile = dict()
    person_profile["workExperience"] = []
    person_profile["education"] = []

    result = ""

    for key in body:
        if "job" in key:
            jobIndex = int(key.split("-")[0].replace("job", ""))
            jobKey = key.split("-")[1]
            try:
                person_profile["workExperience"][jobIndex - 1][jobKey] = body[key]
            except:
                person_profile["workExperience"].insert(jobIndex, {jobKey: body[key]})

        elif "education" in key:
            jobIndex = int(key.split("-")[0].replace("education", ""))
            jobKey = key.split("-")[1]
            try:
                person_profile["education"][jobIndex - 1][jobKey] = body[key]
            except:
                person_profile["education"].insert(jobIndex, {jobKey: body[key]})

        else:
            person_profile[key] = request.args.getlist(key)

    if len(body.values()) > 0:
        response = openai.Completion.create(
            model="text-curie-001",
            prompt=f"Generate a cover letter for me in first person. Here is some profile information about myself and the company as an object: {person_profile}. Use each value and their respective keys from the provided object as the description for the context of the cover letter.",
            max_tokens=1000,
            temperature=0.75,
        )
        result = response.choices[0].text

    return render_template("index.html", result=result)
