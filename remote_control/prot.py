import socket
HEADERSIZE = 10
BUFFER_RECIEVE = 16

# add the msg length in front of the msg in fix size (HEADERSIZE)
def create_msg_with_header(simple_msg):
    return f'{len(simple_msg):<{HEADERSIZE}}' + simple_msg

# recieve a message starts with a header
HEADERSIZE = 10

def receive_msg(sock):
    # First, read exactly the header (10 bytes)
    header = b""
    while len(header) < HEADERSIZE:
        chunk = sock.recv(HEADERSIZE - len(header))
        if not chunk:
            return None  # connection closed
        header += chunk
    
    try:
        msglen = int(header.decode().strip())
    except ValueError:
        return None  # corrupted header
    
    # Now read the full message body
    data = b""
    while len(data) < msglen:
        chunk = sock.recv(msglen - len(data))
        if not chunk:
            return None
        data += chunk
    
    return data.decode()
