from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    body = request.args.to_dict()
    person_profile = dict()
    person_profile["work_experience"] = []
    person_profile["education"] = []

    for key in body:
        if "job" in key:
            jobIndex = int(key.split("-")[0].replace("job", ""))
            jobKey = key.split("-")[1]
            try:
                person_profile["work_experience"][jobIndex - 1][jobKey] = body[key]
            except:
                person_profile["work_experience"].insert(jobIndex, {jobKey: body[key]})

        elif "education" in key:
            jobIndex = int(key.split("-")[0].replace("education", ""))
            jobKey = key.split("-")[1]
            try:
                person_profile["education"][jobIndex - 1][jobKey] = body[key]
            except:
                person_profile["education"].insert(jobIndex, {jobKey: body[key]})

        else:
            person_profile[key] = request.args.getlist(key)

    # about: '',
    # work_experience: [{
    #     year: '',
    #     title: '',
    #     company: '',
    #     description: ''
    # }],
    #    education: [{
    #     year: '',
    #     course: '',
    #     level: '',
    #     company: '',
    #     description: ''
    # }], softSkills: [''],
    # hardSkills: ['']

    return render_template("index.html")
