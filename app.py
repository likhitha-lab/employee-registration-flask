"""Employee Registration Form - Flask app for Computer Use Agent testing.

No database: the form is handled entirely in the browser and nothing is stored.
"""

import os

from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify(status="ok", application="employee-registration-flask")


if __name__ == "__main__":
    # Local development server. Production platforms run gunicorn instead (see Procfile / README).
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=False)
