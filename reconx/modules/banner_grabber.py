# reconx/modules/banner_grabber.py
import socket

def grab_banner(ip, port, timeout=1.0):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, int(port)))
        try:
            banner = s.recv(1024)
            return banner.decode(errors='ignore').strip()
        finally:
            s.close()
    except Exception:
        return None
