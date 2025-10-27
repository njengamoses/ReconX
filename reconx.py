#!/usr/bin/env python3
# reconx.py - top level wrapper for ReconX
import sys, json
from reconx import scanner, report

def main():
    if len(sys.argv) < 2:
        print("Usage: python reconx.py [scan|report] <arg>")
        return

    cmd = sys.argv[1]

    if cmd == "scan":
        if len(sys.argv) < 3:
            print("Usage: python reconx.py scan <target>")
            return
        target = sys.argv[2]
        out = f"examples/{target}_scan.json"
        data = scanner.scan_target(target)
        with open(out, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[+] Scan complete. Saved to {out}")

    elif cmd == "report":
        if len(sys.argv) < 3:
            print("Usage: python reconx.py report <json_file>")
            return
        json_file = sys.argv[2]
        report.generate_html_report(json_file)

    else:
        print("Unknown command. Use 'scan' or 'report'.")

if __name__ == "__main__":
    main()
