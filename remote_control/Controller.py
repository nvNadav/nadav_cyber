import socket

def create_socket(ip,port):
    serv = socket.socket()
    serv.bind((ip, port))
    serv.listen(1)
    cli_sock, cli_addr = serv.accept()

    return serv,cli_sock,cli_addr

serv,cli_sock,cli_addr=create_socket("0.0.0.0",60123)
