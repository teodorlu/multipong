import microbit as mb
import radio

IDS = list('1234567890abcde')
ids_occupied = []

mb.display.show(mb.Image.HEART)
radio.on()

def image_id(id):
    return mb.Image('9' * int(my_id) + '0' * (25 - int(my_id)))

def get_next_free_id():
    free_ids = [id for id in IDS if id not in ids_occupied]
    return free_ids[0]

def shownum(n):
    mb.display.show(image_id(n))

def numline(n):
    return "9" * int(n) + "0" * (5 - int(n))

def numlines(*args):
    return ":".join(numline(a) for a in args)

def shownums(*args):
    s = numlines(*args)
    mb.display.show(mb.Image(s))

def get_next_occupied_id(id):
    position = ids_occupied.index(id)
    return ids_occupied[ (position + 1) % len(ids_occupied) ]

def find_my_id():
    ids_occupied.clear()
    radio.send("hello")
    mb.sleep(1000)
    while True:
        incoming = radio.receive()
        if incoming and incoming not in ids_occupied and incoming in IDS:
            ids_occupied.append(incoming)
        else:
            break
    my_id = get_next_free_id()
    ids_occupied.append(my_id)
    ids_occupied.sort()
    radio.send('ids:{}'.format(''.join(ids_occupied)))
    return my_id

my_id = find_my_id()
mb.display.show(image_id(my_id))

while True:
    if mb.button_a.was_pressed():
        radio.send(get_next_occupied_id(my_id))
        continue
    
    if mb.button_b.was_pressed():
        radio.send("reset")
        continue
    
    incoming = radio.receive()
    if incoming is None:
        shownums(int(my_id), len(ids_occupied))
        continue

    if incoming == 'hello':
        radio.send(my_id)
        mb.display.show(mb.Image.HAPPY)

    elif incoming == 'reset':
        ids_occupied = [my_id]
        mb.sleep(50)
        radio.send(my_id)

    elif incoming.startswith('ids:'):
        incoming_ids = incoming[4:]
        ids_occupied[:] = list(incoming_ids)

    elif incoming == my_id:
        mb.display.show(my_id)
        mb.sleep(500)
        next_id = get_next_occupied_id(my_id)
        radio.send(next_id)
