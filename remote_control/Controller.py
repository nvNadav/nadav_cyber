import socket,keyboard,prot,mouse,threading
ip="0.0.0.0"
port=60123


def create_socket(ip,port):
    serv = socket.socket()
    serv.bind((ip, port))
    serv.listen(1)
    cli_sock, cli_addr = serv.accept()
    print(f"Server is connected with {cli_addr}...")
    return serv,cli_sock,cli_addr

def new_key(event,sock):
    if event.event_type == 'down':
        sock.send(prot.create_msg_with_header(event.name).encode())
    
def keyboard_actions():
    serv,cli_sock,cli_addr=create_socket(ip,port)

    keyboard.hook(lambda e: new_key(e, cli_sock))
    keyboard.wait('shift+esc')
    cli_sock.send(prot.create_msg_with_header("EXIT").encode())

    cli_sock.close()
    serv.close()
    print ("Server closed")
keyboard_actions()