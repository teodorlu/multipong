import microbit as mb
import radio

ME = '1'

mb.display.show('*')
radio.on()

while True:
    if mb.button_a.was_pressed():
        radio.send(ME)

    if mb.button_b.was_pressed():
        radio.send("B")

    incoming = radio.receive()
    if incoming:
        mb.display.show(incoming)
