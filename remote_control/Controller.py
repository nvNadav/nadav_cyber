import socket,keyboard,prot,threading,time
from pynput import mouse

ip="0.0.0.0"
port=60123


def create_socket(ip,port):
    serv = socket.socket()
    serv.bind((ip, port))
    serv.listen(1)
    print ("Server is waiting for connection...")
    cli_sock, cli_addr = serv.accept()
    print(f"Server is connected with {cli_addr}")
    return serv,cli_sock,cli_addr

# -----------------------------
# keyboard section
# -----------------------------
def new_key(event,sock):
    if event.event_type == 'down':
        sock.send(prot.create_msg_with_header(event.name).encode())
    
def keyboard_actions():
    serv,cli_sock_keyboard,cli_addr=create_socket(ip,port)

    keyboard.hook(lambda e: new_key(e, cli_sock_keyboard))
    keyboard.wait('shift+esc')
    cli_sock_keyboard.send(prot.create_msg_with_header("EXIT").encode())

    cli_sock_keyboard.close()
    serv.close()
    print ("Server closed")

# -----------------------------
# mouse section
# -----------------------------

def on_move(x, y):
    
    print(f'Mouse moved to ({x}, {y})')

def on_click(x, y, button, pressed):
    if pressed:
        print(f'Mouse clicked at ({x}, {y}) with {button}')
        if button == mouse.Button.middle and x <= 2 and y <= 2:
            return False
    else:
        print(f'Mouse released at ({x}, {y}) with {button}')

def on_scroll(x, y, dx, dy):
    print(f'Mouse scrolled at ({x}, {y}) - dx: {dx}, dy: {dy}')



def mouse_actions():
    print("Starting mouse tracking... Press Ctrl+C to stop")

    with mouse.Listener(on_move=on_move,on_click=on_click,on_scroll=on_scroll) as listener: 
        listener.join()


keyboard_thread=threading.Thread(target=keyboard_actions)
mouse_thread=threading.Thread(target=mouse_actions)
mouse_thread.start()
#keyboard_thread.start()