#!/usr/bin/env python3
"""
Top-level wrapper so you can run:
  python reconx.py scan 127.0.0.1 --ports 1-1000 --output examples/report.html
"""

import argparse
from reconx.scanner import scan_target
from reconx.reporter import render_report

def cmd_scan(args):
    data = scan_target(target=args.target, ports=args.ports, arguments="-sV")
    out = render_report(data, out_path=args.output)
    print(f"[+] Report generated: {out}")

def main():
    parser = argparse.ArgumentParser(prog="reconx", description="ReconX top-level tool")
    sub = parser.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan", help="Run a recon scan")
    p_scan.add_argument("target", help="Target IP or host")
    p_scan.add_argument("--ports", default="1-1024", help="Port range, e.g. 1-1000")
    p_scan.add_argument("--output", default="report.html", help="Output HTML path")
    p_scan.set_defaults(func=cmd_scan)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
