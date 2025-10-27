from flask import Flask, send_file, render_template, redirect, url_for
import os, json, tempfile
from reconx import scanner, report

app = Flask(__name__)
# where to store generated report & JSON
EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "examples")
os.makedirs(EXAMPLES_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate-and-download/<target>")
def generate_and_download(target):
    # safe filenames
    safe_json = os.path.join(EXAMPLES_DIR, f"{target}_scan.json")
    safe_html = os.path.join(EXAMPLES_DIR, f"{target}_report.html")

    # 1) run a short scan (small port range for speed)
    data = scanner.scan_target(target, ports="1-1024", arguments="-sV", timeout=20)
    with open(safe_json, "w") as f:
        json.dump(data, f, indent=2)

    # 2) generate an HTML report from the JSON
    report.generate_html(safe_json, safe_html)

    # 3) send the HTML as a download
    return send_file(safe_html, as_attachment=True)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
