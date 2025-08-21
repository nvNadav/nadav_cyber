import keyboard

def new_key(event):
    print(f"Key pressed: {event.name}")
    keyboard.press_and_release(event.name)


keyboard.on_release(callback=new_key)
keyboard.wait('esc')
print ("Exiting...")