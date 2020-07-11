from flask import Flask, render_template, request, flash
from os import urandom
import io
import pandas as pd
from AutoScrips import scripts


app = Flask(__name__)
app.secret_key = urandom(100)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/send', methods=['POST'])
def send():
    if request.method == "POST":
        file = request.files['numbers']
        msg = request.form['msg'].strip()
        numbers = file.read()

        stream = io.StringIO(numbers.decode("utf-8"))
        df = pd.read_csv(stream)
        # print(df.head())
        try:
            data = scripts.run(df, msg)
            flash("Done sending!!\nPlease check the status")
            return render_template("index.html", data=data)
        except:
            return render_template("index.html")


# Handling HTTP errors
@app.errorhandler(400)
def bad_request(error):
    return render_template('errors/400.html', title='Bad Request'), 400


@app.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html', title='Forbidden'), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', title='Page Not Found'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', title='Server Error'), 500


if __name__ == "__main__":
    app.run()
