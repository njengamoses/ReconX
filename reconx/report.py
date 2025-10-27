# reconx/report.py
import json, os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
os.makedirs(TEMPLATE_DIR, exist_ok=True)
TEMPLATE = os.path.join(TEMPLATE_DIR, "report.html.j2")

# write a polished template if missing
if not os.path.exists(TEMPLATE):
    with open(TEMPLATE, "w") as f:
        f.write(r'''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>ReconX Report - {{ generated }}</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    :root{--bg:#0b0b0f;--panel:#0f1720;--muted:#9fb7a9;--accent:#00d07a;--mono:#9ae6b4}
    body{background:linear-gradient(180deg,#05060a 0%,var(--bg) 100%);color:#e6f9f0;font-family:Inter,Arial,Helvetica,sans-serif;margin:0;padding:24px}
    .wrap{max-width:1100px;margin:0 auto}
    header{display:flex;justify-content:space-between;align-items:center;gap:16px}
    h1{margin:0;font-size:20px;color:var(--accent)}
    .meta{font-size:13px;color:var(--muted)}
    .panel{background:var(--panel);padding:14px;border-radius:8px;margin-top:18px;box-shadow:0 6px 18px rgba(0,0,0,0.6)}
    table{width:100%;border-collapse:collapse;margin-top:8px}
    th,td{padding:10px;border-bottom:1px solid rgba(255,255,255,0.04);text-align:left;font-size:13px}
    th{color:var(--muted);font-weight:600}
    td.port{font-family:ui-monospace, SFMono-Regular, Menlo, Monaco, "Roboto Mono", monospace}
    .summary{display:flex;gap:12px;flex-wrap:wrap;margin-top:8px}
    .stat{background:rgba(255,255,255,0.02);padding:8px 12px;border-radius:6px}
    .small{font-size:12px;color:var(--muted)}
    a.btn{display:inline-block;padding:8px 12px;background:var(--accent);color:#071218;border-radius:6px;text-decoration:none;font-weight:600}
    footer{margin-top:20px;color:var(--muted);font-size:12px}
    @media (max-width:700px){th,td{padding:8px;font-size:12px}}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <div>
        <h1>ReconX Report</h1>
        <div class="meta">Generated: {{ generated }} — Scanned with ReconX</div>
      </div>
      <div>
        <a class="btn" href="{{ json_link }}">Download JSON</a>
      </div>
    </header>

    <div class="panel">
      <div class="summary">
        <div class="stat"><strong>{{ hosts_count }}</strong><div class="small">hosts</div></div>
        <div class="stat"><strong>{{ open_ports_count }}</strong><div class="small">open ports (total)</div></div>
      </div>

      {% for host, info in data.items() %}
      <section style="margin-top:18px">
        <h3 style="margin:6px 0 8px 0">{{ host }} <span class="small">({{ info.state }})</span></h3>
        {% for proto, ports in info.protocols.items() %}
        <div style="margin-top:6px">
          <div class="small" style="margin-bottom:6px">Protocol: {{ proto|upper }}</div>
          <table>
            <thead><tr><th>Port</th><th>State</th><th>Service</th><th>Product</th><th>Version</th><th>Banner</th></tr></thead>
            <tbody>
            {% for p in ports %}
              <tr>
                <td class="port">{{ p.port }}</td>
                <td>{{ p.state }}</td>
                <td>{{ p.name }}</td>
                <td>{{ p.product or '' }}</td>
                <td>{{ p.version or '' }}</td>
                <td style="font-family:ui-monospace, monospace;max-width:320px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis">{{ p.get('banner','') }}</td>
              </tr>
            {% endfor %}
            </tbody>
          </table>
        </div>
        {% endfor %}
      </section>
      {% endfor %}
    </div>

    <footer>ReconX — built for learning. Do not scan systems without permission.</footer>
  </div>
</body>
</html>
''')
# load template with jinja2
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def render_report_from_data(data, out_path="report.html", json_link=None):
    generated = datetime.utcnow().isoformat() + "Z"
    hosts_count = len(data)
    open_ports_count = sum(len(ports) for h in data.values() for ports in h.get("protocols", {}).values())
    tpl = env.get_template("report.html.j2")
    html = tpl.render(data=data, generated=generated, hosts_count=hosts_count, open_ports_count=open_ports_count, json_link=json_link or "")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path

def generate_html_report(json_file, output_file="report.html"):
    if not os.path.exists(json_file):
        print(f"[ERROR] JSON file '{json_file}' not found.")
        return
    with open(json_file) as f:
        data = json.load(f)
    json_link = os.path.basename(json_file)
    return render_report_from_data(data, out_path=output_file, json_link=json_link)
