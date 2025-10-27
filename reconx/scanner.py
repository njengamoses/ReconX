# reconx/scanner.py
import nmap, json, sys

def scan_target(target="127.0.0.1", ports="1-1024", arguments="-sV"):
    nm = nmap.PortScanner()
    nm.scan(hosts=target, ports=ports, arguments=arguments)
    output = {}
    for host in nm.all_hosts():
        host_info = {"address": host, "state": nm[host].state(), "protocols": {}}
        for proto in nm[host].all_protocols():
            host_info["protocols"][proto] = []
            for port in nm[host][proto].keys():
                p = nm[host][proto][port]
                host_info["protocols"][proto].append({
                    "port": port,
                    "state": p.get("state"),
                    "name": p.get("name"),
                    "product": p.get("product"),
                    "version": p.get("version")
                })
        output[host] = host_info
    return output

if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    print(json.dumps(scan_target(tgt), indent=2))
