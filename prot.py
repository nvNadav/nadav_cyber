import socket
HEADERSIZE = 10
BUFFER_RECIEVE = 16

# add the msg length in front of the msg in fix size (HEADERSIZE)
def create_msg_with_header(simple_msg):
    return f'{len(simple_msg):<{HEADERSIZE}}' + simple_msg

# recieve a message starts with a header
def receive_msg(sock):
    full_msg = ''
    new_msg = True
    while True:
        #header can be received in multiple chunks
        msg = sock.recv(BUFFER_RECIEVE)
        if len(msg) == 0:
            return None
        if new_msg:    # first chunk consists of the header and the first part of the msg
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
        full_msg += msg.decode()

        if len(full_msg) - HEADERSIZE == msglen:
            return full_msg[HEADERSIZE:]