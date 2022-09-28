from flask import Flask

app = Flask(__name__)

@app.route("/")

def test_func():
	return "<p>This is a new function!</p>"

def hello_world():
    return "<p>This is a Python Flask app running with Gunicorn and Nginx! 🐍+🧪+🦄+🚙 = ⚡️💪🔥</p>"

if __name__ == "__main__":
	app.run(host='0.0.0.0')
