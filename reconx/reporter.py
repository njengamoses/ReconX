# reconx/reporter.py
import os
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
os.makedirs(TEMPLATE_DIR, exist_ok=True)

template_file = os.path.join(TEMPLATE_DIR, "report.html.j2")
if not os.path.exists(template_file):
    with open(template_file, "w") as f:
        f.write("""<!doctype html>
<html><head><meta charset="utf-8"><title>ReconX Report</title>
<style>body{background:#0b0b0b;color:#cfeccf;font-family:Arial}h1{color:#00ff00}.container{max-width:900px;margin:20px auto;padding:20px;background:#0f0f0f;border-radius:6px}</style>
</head><body><div class="container"><h1>ReconX Report</h1>
{% for host, info in data.items() %}
  <h2>{{ host }} — {{ info.state }}</h2>
  {% for proto, ports in info.protocols.items() %}
    <h3>{{ proto.upper() }}</h3>
    <table width="100%" cellspacing="0" cellpadding="6">
      <tr><th align="left">Port</th><th align="left">State</th><th align="left">Service</th><th align="left">Product</th></tr>
      {% for p in ports %}
      <tr><td style="font-family:monospace">{{ p.port }}</td><td>{{ p.state }}</td><td>{{ p.name }}</td><td>{{ p.product or '' }} {{ p.version or '' }}</td></tr>
      {% endfor %}
    </table>
  {% endfor %}
{% endfor %}
</div></body></html>""")

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def render_report(data, out_path="report.html"):
    tpl = env.get_template("report.html.j2")
    html = tpl.render(data=data)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path
