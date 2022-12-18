import tkinter
import random
import time

snake_size = 20
max_lenght = 10
canvas_size = 720

red, green, blue, gray = "#e36666", "#76e2af", "#32b1d3", "#282c34"

canvas = tkinter.Canvas(bg=gray, width=canvas_size, height=canvas_size)
canvas.pack()


def move():
    global current_x, current_y, snake_size, score, current_key

    prev_x, prev_y = current_x, current_y

    if current_key == "Left": current_x -= snake_size * 2
    elif current_key == "Right": current_x += snake_size * 2
    elif current_key == "Up": current_y -= snake_size * 2
    elif current_key == "Down": current_y += snake_size * 2

    if (current_x + snake_size * 2) > canvas_size:
        current_x -= snake_size * 2
        return blink(current_x, current_y, score, "You've hit the wall")
    elif (current_x - snake_size * 2) < 0:
        current_x += snake_size * 2
        return blink(current_x, current_y, score, "You've hit the wall")

    elif (current_y + snake_size * 2) > canvas_size:
        current_y -= snake_size * 2
        return blink(current_x, current_y, score, "You've hit the wall")
    elif (current_y - snake_size * 2) < 0:
        current_y += snake_size * 2
        return blink(current_x, current_y, score, "You've hit the wall")

    else:
        square(prev_x, prev_y, blue)

        if [current_x, current_y] in coords:
            if current_key == "Left": current_x += snake_size * 2
            elif current_key == "Right": current_x -= snake_size * 2
            elif current_key == "Up": current_y += snake_size * 2
            elif current_key == "Down": current_y -= snake_size * 2

            if (current_key == "Left" and previous_key == "Right"):
                current_key = "Right"
                return move()
            elif (current_key == "Right" and previous_key == "Left"):
                current_key = "Left"
                return move()
            elif (current_key == "Up" and previous_key == "Down"):
                current_key = "Down"
                return move()
            elif (current_key == "Down" and previous_key == "Up"):
                current_key = "Up"
                return move()
            else:
                return blink(current_x, current_y, score, "You've eaten yourself")
        else:
            coords.append([current_x, current_y])
            square(current_x, current_y, green)

        if current_x == fruit_x and current_y == fruit_y:
            score += 1

            generate_fruit()
            while [fruit_x, fruit_y] in coords:
                generate_fruit()

        if len(coords) > score + 2:
            square(coords[0][0], coords[0][1], gray)
            coords.pop(0)

        print_score(score)

    canvas.after(120, move)


def keypress(event):
    global current_key, previous_key, iteration, menu_text

    if event.keysym == "Left" or event.keysym == "Right" or \
       event.keysym == "Up" or event.keysym == "Down":
        previous_key = current_key
        current_key = event.keysym

        if iteration == 0:
            iteration += 1

            canvas.delete(menu_text)
            move()


def generate_fruit():
    global canvas_size, fruit_x, fruit_y, fruit

    fruit_x = random.randrange(snake_size * 2, canvas_size, snake_size * 2)
    fruit_y = random.randrange(snake_size * 2, canvas_size, snake_size * 2)

    canvas.delete(fruit)
    fruit = circle(fruit_x, fruit_y, red)


def square(_x, _y, fill):
    return canvas.create_rectangle(_x - snake_size, _y - snake_size, _x + snake_size,
                                   _y + snake_size, fill=fill, width=0)


def circle(_x, _y, fill):
    return canvas.create_oval(_x - snake_size, _y - snake_size, _x + snake_size, _y + snake_size,
                              fill=fill, width=0)


def blink(_x, _y, score, text):
    square(_x, _y, red)
    print_score(score)
    canvas.update()

    time.sleep(0.1)

    square(_x, _y, green)
    print_score(score)
    canvas.update()

    print_text(canvas_size / 2, canvas_size / 2, text)
    canvas.update()

    time.sleep(1.5)
    reset()


def print_text(_x, _y, text):
    return canvas.create_text(_x, _y, fill="yellow", text=text,
                              font=("JetBrains Mono", snake_size + 10, "bold"))


def print_score(text):
    global score_element

    canvas.delete(score_element)
    score_element = print_text(canvas_size / 2, snake_size * 2, text)


def reset():
    global current_x, current_y, canvas_size, coords, score, score_element, fruit, iteration, \
           current_key, previous_key, menu_text

    current_x = current_y = canvas_size / 2
    coords = [[current_x, current_y]]
    score = score_element = fruit = iteration = current_key = previous_key = 0

    canvas.delete("all")

    print_score(score)
    generate_fruit()
    square(current_x, current_y, green)
    menu_text = print_text(canvas_size / 2, canvas_size / 2, "Press any arrow key to start playing")


reset()
canvas.bind_all("<Key>", keypress)
canvas.mainloop()
