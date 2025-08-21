import socket,keyboard
import prot

def create_socket(ip,port):
    serv = socket.socket()
    serv.bind((ip, port))
    serv.listen(1)
    cli_sock, cli_addr = serv.accept()
    print(f"Server is connected with {cli_addr}...")
    return serv,cli_sock,cli_addr

def new_key(event):
    if event.event_type == 'down':
        cli_sock.send(prot.create_msg_with_header(event.name).encode())
    

serv,cli_sock,cli_addr=create_socket("0.0.0.0",60123)

keyboard.hook(callback=new_key)
keyboard.wait('shift+esc')
cli_sock.send(prot.create_msg_with_header("EXIT").encode())

cli_sock.close()
serv.close()
print ("Server closed")