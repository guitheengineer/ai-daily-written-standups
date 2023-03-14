from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    # person_profile = {
    #     name: '',
    #     about: '',
    #     work_experience: [{
    #         year: '',
    #         title: '',
    #         company: '',
    #         description: ''
    #     }],
    #        education: [{
    #         year: '',
    #         course: '',
    #         level: '',
    #         company: '',
    #         description: ''
    #     }], softSkills: [''],
    #     hardSkills: ['']
    # }
    return render_template("index.html")
