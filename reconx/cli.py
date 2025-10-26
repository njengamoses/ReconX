# reconx/cli.py
import argparse
from reconx.scanner import scan_target
from reconx.reporter import render_report

def main():
    parser = argparse.ArgumentParser(prog="reconx", description="ReconX CLI")
    parser.add_argument("--target", "-t", required=True, help="Target IP or host")
    parser.add_argument("--ports", "-p", default="1-1024", help="Port range")
    parser.add_argument("--out", "-o", default="report.html", help="Output HTML path")
    args = parser.parse_args()
    data = scan_target(args.target, ports=args.ports)
    out = render_report(data, out_path=args.out)
    print(f"[+] Report generated: {out}")

if __name__ == "__main__":
    main()
