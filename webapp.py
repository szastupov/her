from her import Her

from flask import Flask
from flask import render_template, request

app = Flask(__name__)
her = Her()

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/say", methods=["POST"])
def say():
	msg = str(request.get_data(), "utf-8")
	return her.tell(msg)

if __name__ == "__main__":
    app.run(debug=True)
