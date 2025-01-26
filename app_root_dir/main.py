from flask import Flask,render_template

app = Flask(__name__)

@app.route("/start_page")
def start_page():
    return render_template('start_page.html')

@app.route("/")
def main_page():
    return render_template('main_page.html')

@app.route("/registration")
def registration_page():
    return render_template("registration_page.html")


if __name__ == "__main__":
    app.run(debug=True)