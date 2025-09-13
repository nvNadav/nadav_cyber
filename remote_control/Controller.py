import math
import socket
import threading
import time
import numpy as np
import keyboard
import numpy as np
import cv2

from pynput import mouse

import prot

keyboard_port = 60123
mouse_port = 60124
screen_port = 60125

def create_socket(port,*, host='0.0.0.0', family=socket.AF_INET, sock_type=socket.SOCK_STREAM):
    serv = socket.socket(family,sock_type)
    serv.bind((host, port))
    if sock_type==socket.SOCK_DGRAM:
        print(f"Server is waiting for connection in port {port}")
        data, cli_addr = serv.recvfrom(1024)
        serv.connect(cli_addr)
        print(f"Server is connected with {cli_addr}")
        return serv
    
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
        serv,keyboard_socket,cli_addr=create_socket(keyboard_port)

        keyboard.hook(lambda e: new_key(e, keyboard_socket))
        keyboard.wait('shift+esc')
        keyboard_socket.send(prot.create_msg_with_header("EXIT").encode())
    except Exception as error:
        print (str(error))
    finally:
        keyboard_socket.close()
        serv.close()
        keyboard.unhook_all()
        print ("keyboard closed...")
# -----------------------------
# mouse section
# -----------------------------

# Throttling variables
last_move_time = 0
last_position = (None, None)
move_interval = 0.05  
position_threshold = 3  # Only send if moved at least 3 pixels

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

    # Send the coordinates
    sock.send(prot.create_msg_with_header(f"MOVE {x} {y}").encode())

def on_click(x, y, button, pressed,sock):
    if pressed:
        if button == mouse.Button.middle and x <= 2 and y <= 2:
            return False 
        sock.send(prot.create_msg_with_header(f"PRESS {button.name}").encode())
    else:
        sock.send(prot.create_msg_with_header(f"RELEASE {button.name}").encode())

def on_scroll(x, y, dx, dy,sock):
    sock.send(prot.create_msg_with_header(f"SCROLL {dx} {dy}").encode())


def mouse_actions():
    try:
        serv,mouse_socket,cli_addr=create_socket(mouse_port)

        with mouse.Listener(on_move=lambda x,y: on_move(x,y,mouse_socket),
                            on_click=lambda x,y,button,pressed:on_click(x,y,button,pressed,mouse_socket),
                            on_scroll=lambda x,y,dx,dy:on_scroll(x,y,dx,dy,mouse_socket)) as listener: 
            listener.join()
        mouse_socket.send(prot.create_msg_with_header("EXIT").encode())
    except Exception as error:
        print (str(error))
    finally:
        mouse_socket.close()
        serv.close()
        print ("Mouse closed...")

# -----------------------------
# screen section
# -----------------------------
def recieve_screenshot():
    try:
        screen_socket=create_socket(screen_port,sock_type=socket.SOCK_DGRAM)
        while True:
            img_bytes=prot.receive_msg(screen_socket)
            display_image(img_bytes)
    except Exception as error:
        print (str(error))

def display_image(img_bytes):
    try:
        nparr = np.frombuffer(img_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imshow("Received Screenshot", image)
        cv2.waitKey(100)
        cv2.destroyAllWindows()
    except Exception as error:
        print (str(error))

# keyboard_thread=threading.Thread(target=keyboard_actions)
# mouse_thread=threading.Thread(target=mouse_actions)
# mouse_thread.start()
# keyboard_thread.start()

screen_thread=threading.Thread(target=recieve_screenshot)
screen_thread.start()
screen_thread.join()