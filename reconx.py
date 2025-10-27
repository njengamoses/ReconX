#!/usr/bin/env python3
"""
ReconX wrapper — supports:
  python reconx.py scan <target>
  python reconx.py report <json_file>

Also supports shorthand:
  python reconx.py --target <target>   (runs a scan)
  python reconx.py --report <json_file> (generates a report)
"""
import sys, json, argparse
from reconx import scanner, report

def do_scan(target, out=None):
    out = out or f"examples/{target}_scan.json"
    data = scanner.scan_target(target)
    with open(out, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[+] Scan complete. Saved to {out}")
    return out

def do_report(json_file):
    report.generate_html_report(json_file)
    return None

def main():
    # Top-level parser that also accepts shorthand flags
    parser = argparse.ArgumentParser(prog="reconx", description="ReconX top-level tool")
    parser.add_argument("--target", help="Quick scan: target IP or domain (shorthand)")
    parser.add_argument("--scan-out", help="Output JSON file for shorthand --target")
    parser.add_argument("--report", help="Quick report generation from JSON file (shorthand)")

    sub = parser.add_subparsers(dest="command")
    p_scan = sub.add_parser("scan", help="Run a recon scan")
    p_scan.add_argument("target", help="Target IP or host")
    p_scan.add_argument("--out", default=None, help="Output JSON path (optional)")

    p_report = sub.add_parser("report", help="Generate HTML report from JSON")
    p_report.add_argument("json_file", help="Path to JSON file")

    args = parser.parse_args()

    # Shorthand handling
    if args.target:
        out = args.scan_out or f"examples/{args.target}_scan.json"
        do_scan(args.target, out=out)
        return

    # Subcommand handling
    if args.command == "scan":
        out = args.out or f"examples/{args.target}_scan.json"
        do_scan(args.target, out=out)
        return
    if args.command == "report":
        do_report(args.json_file)
        return

    parser.print_help()

if __name__ == "__main__":
    main()
