import microbit as mb
import radio
import random

IDS = list('1234567890abcde')
TIME_INCREMENT = 250
RACKET_Y_POS = 4

ids_occupied = []
state = dict(
    racket_x_pos=2,
    ball_pos=(2,0), # None
    ball_vel=(0,1),
    ball_update=0,
    life_count=5,
)

mb.display.show(mb.Image.HEART)
radio.on()


def main():
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

    draw_ball(my_id)
    state["ball_update"] = mb.running_time()

    while True:
        if mb.button_a.was_pressed():
            if state['racket_x_pos'] > 0:
                state['racket_x_pos'] -= 1

        if mb.button_b.was_pressed():
            if state['racket_x_pos'] < 4:
                state['racket_x_pos'] += 1

        draw_racket()

        if should_move_ball():
            move_ball(my_id)
            draw_ball(my_id)

        incoming = radio.receive()
        if incoming is None:
            # shownums(int(my_id), len(ids_occupied))
            continue

        print(incoming)
        if incoming == 'hello':
            radio.send(my_id)
            #mb.display.show(mb.Image.HAPPY)

        elif incoming.startswith('ids:'):
            incoming_ids = incoming[4:]
            ids_occupied[:] = list(incoming_ids)

        elif incoming.startswith('ball:' + my_id):
            x, y, dx, dy = [int(n) for n in incoming[7:].split(';')]
            state['ball_pos'] = (x, y)
            state['ball_vel'] = (dx, dy)
            draw_ball(my_id)

        elif incoming.startswith('crash:'):
            mb.display.show(incoming[-1])

def draw_racket():
    x_pos = state['racket_x_pos']
    x_string = '000696000'[x_pos:x_pos+5]
    for x, val in enumerate(x_string):
        mb.display.set_pixel(4-x, 4, int(val))


def draw_ball(my_id):
    s = (
        ("5" * int(my_id) + "2" * (len(ids_occupied) - int(my_id)) + "00000")[:5] + ":"
        "00000:"
        "00000:"
        "00000:"
    )
    mb.display.show(mb.Image(s))
    if state['ball_pos']:
        x_pos, y_pos = state['ball_pos']
        print(x_pos, y_pos)
        mb.display.set_pixel(x_pos, y_pos, 9)


def should_move_ball():
    now = mb.running_time()
    previous = state["ball_update"]
    delta = now - previous

    if state["ball_pos"] and delta > TIME_INCREMENT:
        state["ball_update"] = now
        return True
    else:
        return False

def move_ball(my_id):
    """
    Handle moving the ball.

    Generally: move it in the velocity direction.
    On bounce with racket:
     - swap velocity y-dir; increment
     - set velocity x-dir depending on hit position.
    On bounce with side wall: swap velocity x-dir
    """
    x1, y1 = state["ball_pos"]
    racket_x_pos = state["racket_x_pos"]
    dx, dy = state["ball_vel"]

    if y1 + 1 is RACKET_Y_POS and dy > 0:
        # Try bouncing the ball
        dx = x1 - racket_x_pos
        if abs(dx) <= 1:
            dy = -dy
        else:
            radio.send('crash:' + my_id)
            mb.display.show(mb.Image.SAD)
            mb.sleep(500)
            state['life_count'] -= 1
            mb.display.show(str(state['life_count']))
            mb.sleep(500)
            state['ball_pos'] = (state['racket_x_pos'], 3)
            state['ball_vel'] = (0, -1)
            return

    x2, y2 = x1+dx, y1+dy

    if x2 < 0 and dx < 0:
        x2 = -x2
        dx = -dx
    elif x2 > 4 and dx > 0:
        x2 = 8 - x2
        dx = -dx

    state["ball_pos"] = x2, y2
    state["ball_vel"] = dx, dy
    print((x1, y1), (dx, dy), (x2, y2))

    if y2 < 0:
        send_ball_to_other(my_id)
        state['ball_pos'] = None
        state['ball_vel'] = None


def send_ball_to_other(my_id):
    other_id = random.choice(list(set(ids_occupied) - set(my_id)))
    ball = ';'.join(str(s) for s in [4 - state['ball_pos'][0], 0,
                                     -state['ball_vel'][0], -state['ball_vel'][1]])
    print(other_id, ball)
    radio.send('ball:{}-{}'.format(other_id, ball))


#
#  AUTOCONNECT
#
def get_next_free_id():
    free_ids = [id for id in IDS if id not in ids_occupied]
    return free_ids[0]

def numline(n):
    return "2" * int(n) + "0" * (5 - int(n))

def shownums(*args):
    s = ":".join(numline(a) for a in args)
    mb.display.show(mb.Image(s))

def get_next_occupied_id(id):
    position = ids_occupied.index(id)
    return ids_occupied[ (position + 1) % len(ids_occupied) ]

if __name__ == '__main__':
    main()
