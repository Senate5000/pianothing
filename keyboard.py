import pygame
import pygame.midi
import sys
import random

pygame.init()
pygame.midi.init()

draw_keys = False
keyboard_enabled = True


# key for black vs white notes.  0 = white, 1 = black
white_keys = [1, 3, 4, 6, 8, 9, 11, 13, 15, 16, 18, 20, 21, 23, 25, 27, 28, 30, 32, 33, 35, 37, 39,
              40, 42, 44, 45, 47, 49, 51, 52, 54, 56, 57, 59, 61, 63, 64, 66, 68, 69, 71, 73, 75, 76,
              78, 80, 81, 83, 85, 87, 88]
black_keys = [2, 5, 7, 10, 12, 14, 17, 19, 22, 24, 26, 29, 31, 34, 36, 38, 41, 43, 46, 48, 50, 53, 55,
              58, 60, 62, 65, 67, 70, 72, 74, 77, 79, 82, 84, 86]
black_keys_right = [2, 7, 14, 19, 24, ]
black_keys_left = [5, 10, 12, 17, 22, ]
black_right = [1, 4, 7, 8, 11, 14, 15, 18, 21, 22, 25, 28, 29, 32, 35, 36, 39, 42, 43, 46, 49, 50]
black_left = [3, 6, 10, 13, 17, 20, 24, 27, 31, 34, 38, 41, 45, 48]
keys_down = []
first_guess = True
global attempts
attempts = 0
global correct
correct = 0

# initially set to true so that it runs in the first loop
chord_guessed = True

# set inversion globally so that it can accessed in loop and function
inversion = ""

notes = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
chords = ["major", "minor", "diminished", "augmented"]

if keyboard_enabled:
    my_input = pygame.midi.Input(0)


def number_to_note(number):
    return notes[number % 12]


def print_devices():
    for n in range(pygame.midi.get_count()):
        print (n, pygame.midi.get_device_info(n))


def get_interval(num, steps):
    return_note = num + steps
    if return_note >= 12:
        return_note -= 12
    print(return_note)
    return notes[return_note]


def create_chord():
    chord_type = random.choice(chords)
    chord_root = random.choice(notes)
    root_num = notes.index(chord_root)
    chord_notes = [chord_root]
    inversion = random.choice(["first", "second", "third"])
    if chord_type == "major":
        chord_notes.append(get_interval(root_num, 4))
        chord_notes.append(get_interval(root_num, 7))
    if chord_type == "minor":
        chord_notes.append(get_interval(root_num, 3))
        chord_notes.append(get_interval(root_num, 7))
    if chord_type == "augmented":
        chord_notes.append(get_interval(root_num, 4))
        chord_notes.append(get_interval(root_num, 8))
    if chord_type == "diminished":
        chord_notes.append(get_interval(root_num, 3))
        chord_notes.append(get_interval(root_num, 6))
    return_notes = []
    if inversion == "first":
        return_notes = chord_notes
    if inversion == "second":
        return_notes.append(chord_notes[1])
        return_notes.append(chord_notes[2])
        return_notes.append(chord_notes[0])
    if inversion == "third":
        return_notes.append(chord_notes[2])
        return_notes.append(chord_notes[0])
        return_notes.append(chord_notes[1])
    print("Chord - {0} {1} {2} inversion".format(chord_root, chord_type, inversion))
    # print("Notes - {0}".format(return_notes))
    return return_notes


print_devices()


def update_keys():
    event = my_input.read(1)[0]
    data = event[0]
    timestamp = event[1]
    note_number = data[1]
    velocity = data[2]
    if velocity > 0 and note_number not in keys_down:
        keys_down.append(note_number)
    elif velocity == 0 and note_number in keys_down:
        key_index = keys_down.index(note_number)
        del keys_down[key_index]
    # print (number_to_note(note_number), velocity)


def check_cord(chord):
    # print("Chord - {0}".format(chord))
    # print("Keys Down - {0}".format(keys_down))
    keys_down_notes = [number_to_note(note) for note in keys_down]
    # chord_length = len(chord)
    note_check_list = []
    keys_down_dict = {}
    inversion_check = False
    for note in keys_down:
        keys_down_dict[number_to_note(note)] = note
    # print(keys_down_dict)
    if len(keys_down) == len(chord):
        print("checking chord")
        global attempts
        attempts += 1
        for note in keys_down_notes:
            if note in chord:
                note_check_list.append(True)
            else:
                note_check_list.append(False)
        try:
            if keys_down_dict[chord[0]] < keys_down_dict[chord[1]] and keys_down_dict[chord[0]] < keys_down_dict[chord[2]] and keys_down_dict[chord[1]] < keys_down_dict[chord[2]]:
                inversion_check = True
            else:
                inversion_check = False
        except:
            # wrong notes selected
            pass
        # if inversion == "first":
        #     if keys_down_dict[chord[0]] < keys_down_dict[chord[1]] and keys_down_dict[chord[0]] < keys_down_dict[chord[2]] and keys_down_dict[chord[1]] < keys_down_dict[chord[2]]:
        #         inversion_check = True
        #     else:
        #         inversion_check = False
        # if inversion == "second":
        #     if keys_down_dict[chord[0]] < keys_down_dict[chord[1]] and keys_down_dict[chord[0]] < keys_down_dict[chord[2]] and keys_down_dict[chord[1]] < keys_down_dict[chord[2]]:
        #         inversion_check = True
        #     else:
        #         inversion_check = False
        # if inversion == "third":
        #     if keys_down_dict[chord[0]] < keys_down_dict[chord[1]] and keys_down_dict[chord[0]] < keys_down_dict[chord[2]] and keys_down_dict[chord[1]] < keys_down_dict[chord[2]]:
        #         inversion_check = True
        #     else:
        #         inversion_check = False
        if not False in note_check_list and len(note_check_list) == len(chord) and inversion_check:
            global correct
            correct += 1
            print("Correct! ({0} / {1} {2}%".format(correct, attempts, float(correct / attempts)))
            return True
        else:
            return False

while True:
    if chord_guessed:
        # if not first_guess:
        #     print("Correct! ({0} / {1} {2}%".format(correct, attempts, float(correct / attempts)))
        # first_guess = False
        chord_to_guess = create_chord()
    chord_guessed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
    if draw_keys:
        black = 0, 0, 0
        white = 255, 255, 255
        red = 255, 0, 0
        size = width, height = 0, 0

        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        screen_info = pygame.display.Info()
        screen_h = screen_info.current_h
        screen_w = screen_info.current_w
        print("Width = {0}".format(screen_w))
        key_width = screen_w / 52.0
        black_width = key_width * .75
        black_left_pos = key_width * .65
        black_right_pos = key_width * .75
        print("Key Width - {0}".format(key_width))

        for x in range(52):
            print(x * key_width)

        screen.fill(black)
        pygame.draw.rect(screen, white, (0, 700, screen_w, 200), 0)
        for x in range(52):
            # pygame.draw.rect(screen, black, (x * key_width, 700, key_width, 200), 1)
            pygame.draw.line(screen, black, (x * key_width, 700), (x * key_width, screen_h), 1)
            if (x + 1) in black_right:
                pygame.draw.rect(screen, black, (x * key_width + black_right_pos, 700, black_width, 100), 0)
            if (x + 1) in black_left:
                pygame.draw.rect(screen, black, (x * key_width + black_left_pos, 700, black_width, 100), 0)

        pygame.display.flip()

    if keyboard_enabled:
        if my_input.poll():
            update_keys()

        chord_guessed = check_cord(chord_to_guess)

        if draw_keys:
            for key in keys_down:
                num = key
                print("highlighting key {0}".format(num))
                actual_key = num - 20
                key_loc = actual_key * key_width
                if actual_key in white_keys:
                    print("{0} in white keys".format(actual_key))
                    white_key_loc = white_keys.index(actual_key)
                    print("White key loc = {0}".format(white_key_loc))
                    pygame.draw.rect(screen, red, (white_key_loc * key_width, 700, key_width, 200), 0)
                elif actual_key in black_keys:
                    black_key_loc = black_keys.index(actual_key)
                    if actual_key in black_right:
                        pygame.draw.rect(screen, black, (black_key_loc * key_width + black_right_pos, 700, black_width, 100), 0)
                    if actual_key in black_left:
                        pygame.draw.rect(screen, black, (black_key_loc * key_width + black_left_pos, 700, black_width, 100), 0)
