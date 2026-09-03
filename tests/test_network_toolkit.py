from network_toolkit import load_devices, load_domains,  check_dns


def test_load_devices():
    devices = load_devices()

    assert isinstance(devices, list)
    assert len(devices) > 0

def test_load_domains():
    domains = load_domains()

    assert isinstance(domains, list)
    assert len(domains) > 0
    assert "google.com" in domains    

def test_check_dns():
    result = check_dns("google.com")

    assert result is not None    

def test_check_dns_invalid():
    result = check_dns("this-domain-does-not-exist-12345.com")

    assert result is None    