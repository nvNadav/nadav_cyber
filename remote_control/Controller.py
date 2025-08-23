import math
import socket
import threading
import time

import keyboard
from pynput import mouse

import prot

keyboard_port = 60123
mouse_port = 60124

def create_socket(port,*,ip='0.0.0.0',ip_type=socket.AF_INET,protocol_type=socket.SOCK_STREAM):
    serv = socket.socket()
    serv.bind((ip, port))
    serv.listen(1)
    print(f"Server is waiting for connection in port {port}")
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
    try:
        serv,sock_keyboard,cli_addr=create_socket(keyboard_port)

        keyboard.hook(lambda e: new_key(e, sock_keyboard))
        keyboard.wait('shift+esc')
        sock_keyboard.send(prot.create_msg_with_header("EXIT").encode())
    except Exception as error:
        print (str(error))
    finally:
        sock_keyboard.close()
        serv.close()
        print ("keyboard closed...")

# -----------------------------
# mouse section
# -----------------------------

# Throttling variables
last_move_time = 0
last_position = (None, None)
move_interval = 0.05  # 
position_threshold = 3  # Only print if moved at least 3 pixels

def on_move(x, y,sock):
    global last_move_time, last_position
    
    current_time = time.time()
    
    # Time-based throttling
    if current_time - last_move_time < move_interval:
        return
    
    # Position-based throttling
    last_x, last_y = last_position
    if last_x is not None and last_y is not None:
        # Calculate distance moved
        distance = math.sqrt((x - last_x) ** 2 + (y - last_y) ** 2)
        if distance < position_threshold:
            return
    
    # Update tracking variables
    last_move_time = current_time
    last_position = (x, y)
    
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
    try:
        serv,sock_mouse,cli_addr=create_socket(mouse_port)
        print("Starting mouse tracking...")

        with mouse.Listener(on_move=lambda x,y: on_move(x,y,sock_mouse),
                            on_click=lambda x,y,button,pressed:on_click(x,y,button,pressed,sock_mouse),
                            on_scroll=lambda x,y,dx,dy:on_scroll(x,y,dx,dy,sock_mouse)) as listener: 
            listener.join()
        sock_mouse.send(prot.create_msg_with_header("EXIT").encode())
    except Exception as error:
        print (str(error))
    finally:
        sock_mouse.close()
        serv.close()
        print ("mouse closed...")



#keyboard_thread=threading.Thread(target=keyboard_actions)
mouse_thread=threading.Thread(target=mouse_actions)
mouse_thread.start()
#keyboard_thread.start()