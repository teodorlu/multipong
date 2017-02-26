# What is this?

This code was created exploring micro:bit's radio; its bluetooth connectivity.

- `multipong.py` is a distributed version of the classic Pong
- `cycle.py` sends a message around a group of micro:bits in a cycle.

Clients autoconnect to an existing message sending a hello-message when the chip
is reset. This hello triggers a reponse from existing clients, resulting in
every client knowing what other clients are present; and thereby being able to
send a ball over to a different, random client.

# Setup

Both applications are standalone programs. I recommend
the [https://codewith.mu/](mu-editor).

1. Open `multipong.py` in Mu
2. Connect your micro:bit, and press "flash"
3. Repeat this for all micro:bits you want to play on.

# Interface

On the top of the screen, there is an indicator of who you are (id from 1 to
number of players), and the number of players.

ØØ**_ (two bright lights, two lesser lights) means:

- I am number 2 (ØØ)
- There are 4 clients (ØØ**)

# Controls

- `A` moves the racket left
- `B` moves the racket right
- `reset` triggers a refresh of the other clients, and adds a ball to the game.
  Use reset on one client after removing a client to get it garbage collected.

# Future

Some things that could be expanded on:

- There is currently one ball. Many balls at the same time could be fun
- Showing a scoreboard

An outline to a [radio_kurs.md](task) based on this code has been made (in
Norwegian).

