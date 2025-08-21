import keyboard
from pynput import mouse

def on_move(x, y):
    print(f'Mouse moved to ({x}, {y})')

def on_click(x, y, button, pressed):
    if pressed:
        print(f'Mouse clicked at ({x}, {y}) with {button}')
    else:
        print(f'Mouse released at ({x}, {y}) with {button}')

def on_scroll(x, y, dx, dy):
    print(f'Mouse scrolled at ({x}, {y}) - dx: {dx}, dy: {dy}')

# Start the listener
print("Starting mouse tracking... Press Ctrl+C to stop")
with mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll) as listener:
    listener.join()


# def new_key(event):
#     if event.event_type == 'down':
#         print (event.name)
#         print (type(event.name))


# keyboard.hook(callback=new_key)

# keyboard.wait('shift+esc')

# print ("Exiting...")