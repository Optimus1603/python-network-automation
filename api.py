from fastapi import FastAPI
from network_toolkit import check_ping, check_tcp, check_dns, load_devices, load_domains


app = FastAPI()


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/devices")
def get_devices():
    results = []

    devices = load_devices()

    for device in devices:
        ping_success, rtt, packet_loss = check_ping(device["ip"])
        tcp_success = check_tcp(device["ip"], device["port"])

        results.append({
            "name": device["name"],
            "ip": device["ip"],
            "ping": "UP" if ping_success else "DOWN",
            "rtt_ms": rtt,
            "packet_loss": packet_loss,
            "tcp_port": device["port"],
            "tcp_status": "OPEN" if tcp_success else "NOT AVAILABLE"
        })

    return results

@app.get("/dns")
def get_dns_results():
    results = []

    domains = load_domains()

    for domain in domains:
        ip = check_dns(domain)

        results.append({
            "domain": domain,
            "status": "OK" if ip else "FAILED",
            "ip": ip
        })

    return results