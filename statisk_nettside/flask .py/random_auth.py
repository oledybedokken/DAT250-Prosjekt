import random
import flask import Flask

app : Flask = Flask(__name__)

@app.route("/", methods=["GET"])
def myRandom():
    r1 = random.uniform(10000, 9999)
    return r1

if __name__ == "__main__":
    app.run(debug=True)