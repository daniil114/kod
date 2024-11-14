import random

from flask import Flask, render_template

app = Flask(__name__)

def random_dice():
    return str(random.randint(1, 6))

@app.route("/")
def index():
    return render_template("index.html", dice=random_dice())




if __name__ == "__main__":
    app.run(debug=True, port=5003)
