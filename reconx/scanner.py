# reconx/scanner.py
"""
Scanner: runs Nmap via python-nmap and returns a structured Python dict.

Usage:
    from reconx.scanner import scan_target
    data = scan_target("127.0.0.1", ports="1-1024", timeout=30)
"""
import logging
import nmap

# Configure module-level logger
logger = logging.getLogger("reconx.scanner")
if not logger.handlers:
    h = logging.StreamHandler()
    fmt = logging.Formatter("[%(levelname)s] %(message)s")
    h.setFormatter(fmt)
    logger.addHandler(h)
logger.setLevel(logging.INFO)

def scan_target(target="127.0.0.1", ports="1-1024", arguments="-sV", timeout=30):
    """
    Run an nmap scan and return dict:
    { host: { address, state, protocols: { tcp: [ {port,state,name,product,version,banner}, ... ] } } }
    - timeout: seconds per-host (enforced via nmap --host-timeout)
    """
    nm = nmap.PortScanner()
    # ensure nmap won't hang per-host; append host-timeout to arguments
    full_args = f"{arguments} --host-timeout {int(timeout)}s"
    logger.info("Starting nmap scan: target=%s ports=%s args=%s", target, ports, full_args)
    try:
        nm.scan(hosts=target, ports=ports, arguments=full_args)
    except Exception as e:
        logger.error("Nmap scan failed: %s", e)
        # Return an empty result so callers can handle gracefully
        return {}

    output = {}
    for host in nm.all_hosts():
        try:
            host_info = {"address": host, "state": nm[host].state(), "protocols": {}}
            for proto in nm[host].all_protocols():
                host_info["protocols"][proto] = []
                for port in nm[host][proto].keys():
                    pinfo = nm[host][proto][port]
                    host_info["protocols"][proto].append({
                        "port": port,
                        "state": pinfo.get("state"),
                        "name": pinfo.get("name"),
                        "product": pinfo.get("product"),
                        "version": pinfo.get("version")
                    })
            output[host] = host_info
        except Exception as e:
            # protect per-host parsing so a weird nmap output doesn't crash the whole run
            logger.warning("Failed to parse host %s: %s", host, e)
            continue
    logger.info("Scan complete: found %d hosts", len(output))
    return output

if __name__ == "__main__":
    import json, sys
    tgt = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    print(json.dumps(scan_target(tgt), indent=2))
