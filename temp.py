import keyboard

def new_key(event):
    if event.event_type == 'down':
        print (event.name)
        print (type(event.name))


keyboard.hook(callback=new_key)

keyboard.wait('shift+esc')

print ("Exiting...")