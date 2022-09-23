from flask import Flask, render_template, url_for

app = Flask(__name__)


if __name__ == "__main__":
    app.run(debug=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signInPage')
def signInPage():
    return render_template('signInPage.html')


@app.route('/userIndex', methods=['GET'])
def userIndex():
    return render_template("userIndex.html")
