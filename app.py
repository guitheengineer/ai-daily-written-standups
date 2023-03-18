from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    body = request.args.to_dict()
    person_profile = dict()
    person_profile["work_experience"] = []

    for key in body:
        if "job" in key:
            jobIndex = int(key.split("-")[0].replace("job", ""))
            jobKey = key.split("-")[1]
            person_profile["work_experience"].insert(jobIndex, {jobKey: body[key]})
        else:
            person_profile[key] = body[key]

    print(person_profile)

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
