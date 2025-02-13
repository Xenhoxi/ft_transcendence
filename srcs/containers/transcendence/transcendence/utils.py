import socket

def get_server_ip():
    """
    This function returns the server's IP address.
    """
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def generate_csrf_trusted_origins(ports=[8000, 4443]):
    """
    This function returns a CSRF_TRUSTED_ORIGINS list with the server's IP and localhost for given ports.
    """
    ip_address = get_server_ip()
    trusted_origins = []

    # Add localhost and 0.0.0.0 with different ports
    for port in ports:
        trusted_origins.append(f'http://localhost:{port}')
        trusted_origins.append(f'http://0.0.0.0:{port}')
        trusted_origins.append(f'http://127.0.0.1:{port}')
        trusted_origins.append(f'http://k2r3p8:{port}')
        trusted_origins.append(f'http://k2r3p9:{port}')
        trusted_origins.append(f'http://k2r3p10:{port}')
        trusted_origins.append(f'https://localhost:{port}')
        trusted_origins.append(f'https://0.0.0.0:{port}')
        trusted_origins.append(f'https://127.0.0.1:{port}')
        trusted_origins.append(f'https://k2r3p8:{port}')
        trusted_origins.append(f'https://k2r3p9:{port}')
        trusted_origins.append(f'https://k2r3p10:{port}')

    # Add the dynamically determined IP address
    for port in ports:
        trusted_origins.append(f'http://{ip_address}:{port}')
        trusted_origins.append(f'https://{ip_address}:{port}')
    return trusted_origins