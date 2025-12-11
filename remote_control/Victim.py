import socket
import time
import keyboard
import threading
import pyautogui
import io

from pynput.mouse import Controller, Button

import prot


def create_socket (ip,port,*,family=socket.AF_INET, sock_type=socket.SOCK_STREAM):
    cli = socket.socket(family,sock_type)
    cli.connect((ip,port))
    if sock_type==socket.SOCK_DGRAM:
        cli.send(b"Message the server so he'll know my ip addr and port")
    return cli

# --------------------
# Mouse section
# --------------------

def move(list, mouse):
    # list[1] = x
    # list[2] = y
    mouse.position = (int(list[1]),int(list[2]))

def press(list, mouse):
    #list[1] = button.name
    mouse.press(Button[list[1]])

def release(list, mouse):
    #list[1] = button.name
    mouse.release(Button[list[1]])
def scroll(list, mouse):
    #list[1] = dx value
    #list[2] = dy value
    mouse.scroll(int(list[1]),int(list[2]))

def recieve_mouse(end_connection):
    try:
        mouse_socket = create_socket("192.168.1.161",60124)
        print("Mouse is connected...")
        mouse = Controller()
        functions ={"MOVE":move,"PRESS":press,"RELEASE":release,"SCROLL":scroll}
        while not end_connection.is_set():
            list=prot.receive_msg(mouse_socket).split()
            if list[0]=="EXIT":
                end_connection.set()
                break
            functions[list[0]](list,mouse)
    except Exception as error:
        print(str(error))
    finally:
        mouse_socket.close()
        print("Mouse closed...")

# --------------------
# Keyboard section
# --------------------

def recieve_keyboard(end_connection):
    try:
        keyboard_socket = create_socket("192.168.1.161",60123)
        print("Keyboard is connected...")
        while not end_connection.is_set():
            key = prot.receive_msg(keyboard_socket)
            if key =="EXIT":
                end_connection.set()
                break
            keyboard.press_and_release(key)
    except Exception as error:
        print(str(error))
    finally:
        keyboard_socket.close()
        print("Keyboard closed...")

# --------------------
# screen section
# --------------------

def take_screenshot():
    #try:
        screenshot = pyautogui.screenshot()

        buffer = io.BytesIO()
        screenshot.save(buffer, format="JPEG")
        img_bytes = buffer.getvalue()
        return img_bytes
    #except Exception as error:
        #print(str(error))

def send_image(img_bytes,sock):
    #try:
        sock.send(prot.create_msg_with_header(str(img_bytes)).encode())
    #xcept Exception as error:
        #print(str(error))

def image_stream(end_connection):
    #try:
        screen_socket = create_socket("192.168.1.161",60125,sock_type=socket.SOCK_DGRAM)
        while not end_connection.is_set():
            sceenshot_bytes = take_screenshot()
            send_image(sceenshot_bytes,screen_socket)
    #except Exception as error:
        #print(str(error))
    #finally:
        #screen_socket.close()
        #print("screen closed...")


end_connection = threading.Event()

# mouse_thread = threading.Thread(target=recieve_mouse, args=(end_connection, ))
# keyboard_thread = threading.Thread(target=recieve_keyboard, args=(end_connection, ))
screen_thread = threading.Thread(target=image_stream, args=(end_connection, ))
# mouse_thread.start()
# keyboard_thread.start()
screen_thread.start()

# mouse_thread.join()
# keyboard_thread.join()
screen_thread.join()