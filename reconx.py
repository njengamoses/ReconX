# reconx.py
import argparse
from reconx import scanner, report

def main():
    parser = argparse.ArgumentParser(description="ReconX - Simple Network Recon Tool")
    sub = parser.add_subparsers(dest="command", required=True)

    # --- Scan command ---
    scan = sub.add_parser("scan", help="Run network scan")
    scan.add_argument("-t", "--target", required=True, help="Target IP or domain")
    scan.add_argument("-p", "--ports", default="1-1000", help="Port range, e.g., 1-1024")
    scan.add_argument("-o", "--output", default="examples/scan.json", help="Output JSON path")

    # --- Report command ---
    rep = sub.add_parser("report", help="Generate HTML report from scan result")
    rep.add_argument("-i", "--input", required=True, help="Input scan JSON file")
    rep.add_argument("-o", "--output", default="examples/report.html", help="Output HTML report path")

    args = parser.parse_args()

    if args.command == "scan":
        print(f"[+] Scanning {args.target} ports {args.ports}")
        result = scanner.scan_target(args.target, args.ports)
        import json
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"[✓] Scan saved to {args.output}")

    elif args.command == "report":
        print(f"[+] Generating report from {args.input}")
        report.generate_html(args.input, args.output)
        print(f"[✓] Report saved to {args.output}")

if __name__ == "__main__":
    main()

