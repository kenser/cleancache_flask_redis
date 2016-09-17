import socket
def verify_ip(address):
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((address,80))
        s.close()
        #socket.inet_aton(address)
        return True
    except:
        return False


def verify_domain(domain):
    try:
        socket.getaddrinfo(domain,None)
        return True
    except:
        return False
