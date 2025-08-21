import socket,keyboard
import prot

def create_socket(ip,port):
    serv = socket.socket()
    serv.bind((ip, port))
    serv.listen(1)
    cli_sock, cli_addr = serv.accept()

    return serv,cli_sock,cli_addr

serv,cli_sock,cli_addr=create_socket("0.0.0.0",60123)
while True:
    x=prot.receive_msg(cli_sock)
    print(x)