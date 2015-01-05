# import pygame
# import pygame.midi
# pygame.init()
# pygame.midi.init()

# print(pygame.midi.get_default_input_id())
# while 1:
#     print(pygame.midi.Input(0, 3))

import pygame.midi

keys_down = []

def print_devices():
    for n in range(pygame.midi.get_count()):
        print (n, pygame.midi.get_device_info(n))


def readInput(input_device):
    while True:
        if input_device.poll():
            event = input_device.read(1)[0]
            print(event)
            data = event[0]
            timestamp = event[1]
            note_number = data[1]
            velocity = data[2]
            if velocity > 0 and note_number not in keys_down:
                keys_down.append(note_number)
            elif velocity == 0 and note_number in keys_down:
                key_index = keys_down.index(note_number)
                del keys_down[key_index]
            print(keys_down)
            print (number_to_note(note_number), velocity)


def number_to_note(number):
    print("Converting {0}".format(number))
    notes = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
    return notes[number % 12]

if __name__ == '__main__':
    pygame.midi.init()
    print_devices()
    my_input = pygame.midi.Input(0)  # only in my case the id is 2
    readInput(my_input)
