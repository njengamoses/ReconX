from flask import Flask, send_file, render_template
import os

app = Flask(__name__)
# path to the report to serve
REPORT_PATH = os.path.join(os.path.dirname(__file__), "..", "examples", "final_report.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download")
def download_report():
    if os.path.exists(REPORT_PATH):
        return send_file(REPORT_PATH, as_attachment=True)
    return "Report not found. Generate one first.", 404

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
