import subprocess
import socket
import csv
from datetime import datetime


def check_ping(ip):
    try:
        result = subprocess.run(
            ["ping", "-c", "4", ip],
            capture_output=True,
            text=True,
            timeout=6
        )

        if result.returncode == 0:
            rtt_line = result.stdout.split("rtt min/avg/max/mdev = ")[1]
            avg_rtt = rtt_line.split("/")[1]

            loss_part = result.stdout.split("packet loss")[0]
            packet_loss = loss_part.split(",")[-1].strip()

            return True, float(avg_rtt), packet_loss

        return False, None, "100%"

    except subprocess.TimeoutExpired:
        return False, None, "100%"


def check_tcp(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)

        result = sock.connect_ex((ip, port))

        sock.close()

        return result == 0

    except socket.error:
        return False


def check_dns(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        return ip

    except socket.gaierror:
        return None


def load_devices():
    devices = []

    with open("devices.txt", "r") as file:
        for line in file:
            line = line.strip()

            name, ip, port = line.split(",")

            devices.append({
                "name": name,
                "ip": ip,
                "port": int(port)
            })

    return devices


def load_domains():
    domains = []

    with open("domains.txt", "r") as file:
        for line in file:
            domain = line.strip()
            domains.append(domain)

    return domains


if __name__ == "__main__":

    devices = load_devices()

    log_file = "network_results.csv"

    with open(log_file, "a", newline="") as file:
        writer = csv.writer(file)

        if file.tell() == 0:
            writer.writerow([
                "timestamp",
                "device",
                "ping_status",
                "rtt_ms",
                "packet_loss",
                "tcp_port",
                "tcp_status"
            ])

    for device in devices:
        ping_success, rtt, packet_loss = check_ping(device["ip"])

        if ping_success:
            ping_status = "UP"
        else:
            ping_status = "DOWN"

        if rtt is None:
            rtt_display = "N/A"
        else:
            rtt_display = str(round(rtt, 2)) + " ms"

        if check_tcp(device["ip"], device["port"]):
            tcp_status = "OPEN"
        else:
            tcp_status = "NOT AVAILABLE"

        print(
            device["name"],
            "| Ping:", ping_status,
            "| RTT:", rtt_display,
            "| Loss:", packet_loss,
            "| TCP", device["port"], ":", tcp_status
        )

        with open(log_file, "a", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                device["name"],
                ping_status,
                rtt if rtt is not None else "",
                packet_loss,
                device["port"],
                tcp_status
            ])

    print("\n--- DNS Checks ---")

    domains = load_domains()

    for domain in domains:
        result = check_dns(domain)

        if result:
            print(domain, "| DNS: OK | IP:", result)
        else:
            print(domain, "| DNS: FAILED")