# reconx/scanner.py
"""
Scanner with banner grabbing integrated.
"""
import logging
import nmap
from reconx.modules.banner_grabber import grab_banner

logger = logging.getLogger("reconx.scanner")
if not logger.handlers:
    import sys
    h = logging.StreamHandler(sys.stdout)
    fmt = logging.Formatter("[%(levelname)s] %(message)s")
    h.setFormatter(fmt)
    logger.addHandler(h)
logger.setLevel(logging.INFO)

def scan_target(target="127.0.0.1", ports="1-1024", arguments="-sV", timeout=30, banner_timeout=0.7):
    nm = nmap.PortScanner()
    full_args = f"{arguments} --host-timeout {int(timeout)}s"
    logger.info("Starting nmap scan: target=%s ports=%s args=%s", target, ports, full_args)
    try:
        nm.scan(hosts=target, ports=ports, arguments=full_args)
    except Exception as e:
        logger.error("Nmap scan failed: %s", e)
        return {}

    output = {}
    for host in nm.all_hosts():
        host_info = {"address": host, "state": nm[host].state(), "protocols": {}}
        for proto in nm[host].all_protocols():
            host_info["protocols"][proto] = []
            for port in nm[host][proto].keys():
                pinfo = nm[host][proto][port]
                # attempt banner grab only for open ports
                banner = None
                try:
                    if pinfo.get("state") == "open":
                        banner = grab_banner(host, port, timeout=banner_timeout)
                except Exception:
                    banner = None
                host_info["protocols"][proto].append({
                    "port": port,
                    "state": pinfo.get("state"),
                    "name": pinfo.get("name"),
                    "product": pinfo.get("product"),
                    "version": pinfo.get("version"),
                    "banner": banner
                })
        output[host] = host_info
    logger.info("Scan complete: found %d hosts", len(output))
    return output

if __name__ == "__main__":
    import json, sys
    tgt = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    print(json.dumps(scan_target(tgt), indent=2))
