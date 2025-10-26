# reconx/scanner.py
import nmap

def scan_target(target="127.0.0.1", ports="1-1024", arguments="-sV"):
    """
    Run nmap scan and return structured dict:
    { host: { address, state, protocols: { tcp: [ {port,state,name,product,version}, ... ] } } }
    """
    nm = nmap.PortScanner()
    try:
        # python-nmap expects the keyword 'hosts' not 'targets'
        nm.scan(hosts=target, ports=ports, arguments=arguments)
    except Exception as e:
        # raise a clearer error if nmap fails
        raise RuntimeError(f"Nmap scan failed: {e}")

    output = {}
    for host in nm.all_hosts():
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
    return output

if __name__ == "__main__":
    import json, sys
    tgt = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    print(json.dumps(scan_target(tgt), indent=2))
