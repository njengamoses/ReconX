# reconx/report.py
import json, os

def generate_html_report(json_file, output_file="report.html"):
    if not os.path.exists(json_file):
        print(f"[ERROR] JSON file '{json_file}' not found.")
        return

    with open(json_file) as f:
        data = json.load(f)

    html = [
        "<html><head><title>ReconX Report</title>",
        "<style>body{font-family:Arial;background:#111;color:#eee;padding:20px;}h1{color:#0f0}table{border-collapse:collapse;width:100%;margin-bottom:20px;}th,td{border:1px solid #444;padding:8px;}th{background:#222;}</style>",
        "</head><body>",
        "<h1>ReconX Scan Report</h1>"
    ]

    for host, info in data.items():
        html.append(f"<h2>Host: {host} ({info.get('state')})</h2>")
        for proto, ports in info.get('protocols', {}).items():
            html.append(f"<h3>Protocol: {proto}</h3>")
            html.append('<table><tr><th>Port</th><th>State</th><th>Service</th><th>Product</th><th>Version</th></tr>')
            for p in ports:
                html.append(f"<tr><td>{p.get('port')}</td><td>{p.get('state')}</td><td>{p.get('name')}</td><td>{p.get('product') or ''}</td><td>{p.get('version') or ''}</td></tr>")
            html.append("</table>")

    html.append("</body></html>")

    with open(output_file, "w") as f:
        f.write("\n".join(html))
    print(f"[+] Report generated: {output_file}")
