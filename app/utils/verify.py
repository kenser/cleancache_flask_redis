import socket
def verify_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except:
        return False


def verify_domain(domain):
    try:
        socket.getaddrinfo(domain,None)
        return True
    except:
        return False
