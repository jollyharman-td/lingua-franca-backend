from flask import Flask
from flask import render_template, request, redirect, session, g, Response, flash

from apis.translating import translate_api

app = Flask(__name__)

app.register_blueprint(translate_api)


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("public/index.html")

@app.route("/translate", methods=["GET", "POST"])
def translate():
    return render_template("public/translate.html")

if __name__ == "__main__":
    app.run(debug=True, port = 7000)