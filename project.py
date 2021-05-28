from simpleimage import SimpleImage
import imageio
import random
import os


#This program generates a randomly generated image and uses the rules set out in Conway's game of life to simulate life to how ever many cycles the user wants!
def main():
    print("Welcome to Conway's game of life!")
    print_rules()
    # get user input
    initial_game_state = get_initial_game_state()
    number_of_iterations = check_user_input(input("How many cycles should life run? Please use a positive integer. (if using 'default' use a low number) "))
    if initial_game_state == "Doge":
        bw_game_state = convert_image()
        print("Creating gif.")
        create_gif(bw_game_state, number_of_iterations, initial_game_state)
    elif initial_game_state == "random":
        bw_game_state = generate_random_initial_game_state()
        print("Creating gif.")
        create_gif(bw_game_state, number_of_iterations, initial_game_state)
    print("Gif saved.")
    clean_up(initial_game_state, number_of_iterations)
    print("Done. Find your game_of_life.gif in directory of this program.")


def print_rules():
    print("Rules:")
    print("	1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.")
    print("	2. Any live cell with two or three live neighbours lives on to the next generation.")
    print("	3. Any live cell with more than three live neighbours dies, as if by overpopulation.")
    print("	4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.")
    print("	5. Each pixel is considered a cell, each cell has 8 neighbours.")


def get_initial_game_state():
    # use randomly generated file or use default (pic of dog)
    user_input = input("Use a randomly generated file or use default (picture of a dog)? Please type 'random' or 'default'. ")
    if user_input == "default" or user_input == "":
        return "Doge"
    elif user_input == "random":
        return "random"
    else:
        print("Next time, please type 'random' or 'default'. ")
        exit()


def check_user_input(number_of_iterations):
    # tries to convert user input to an int, if it is not exits the program with message "input is not int"
    try:
        user_input = int(number_of_iterations)
        if user_input > 0:
            return user_input
        else:
            print("Please type in an integer greater than 0.")
            exit()
    except ValueError:
        print("Please type in a valid integer.")
        exit()


def convert_image():
    # takes any image and converts to pure black and white
    game_state = SimpleImage("Doge.png")
    for pixel in game_state:
        average = (pixel.red + pixel.green + pixel.blue) / 3
        if average < 126:
            pixel.red = 0
            pixel.green = 0
            pixel.blue = 0
        else:
            pixel.red = 255
            pixel.green = 255
            pixel.blue = 255
    return game_state


def generate_random_initial_game_state():
    # creates a random image with dimensions 100 by 100 pixels. 80% of the cells/pixels should be dead/black
    random_game_state = SimpleImage.blank(100, 100, back_color="black")
    for pixel in random_game_state:
        random_number = random.randint(0, 9)
        if random_number > 7:
            pixel.red = 255
            pixel.green = 255
            pixel.blue = 255
    return random_game_state


def create_gif(bw_game_state, number_of_iterations, initial_game_state):
    # creates gif by creating a list of images which represent each frame of the gif
    gif_lst = []
    bw_game_state.pil_image.save(f"./temp/{initial_game_state}0.png")
    gif_lst.append(imageio.imread(f"./temp/{initial_game_state}0.png"))
    for iterations in range(number_of_iterations):
        bw_game_state = create_next_state(bw_game_state)
        bw_game_state.pil_image.save(f"./temp/{initial_game_state}{iterations + 1}.png")
    for iterations in range(number_of_iterations):
        gif_lst.append(imageio.imread(f"./temp/{initial_game_state}{iterations + 1}.png"))
    imageio.mimwrite("./game_of_life.gif", gif_lst)


def create_next_state(bw_game_state):
    # creates next cycle in the game of life
    new_state = SimpleImage.blank(bw_game_state.width, bw_game_state.height)
    #copy pastes old state to blank new image
    for pixel in new_state:
        new_state.set_pixel(pixel.x, pixel.y, bw_game_state.get_pixel(pixel.x, pixel.y))
    #applies rule set to determine next game state/cycle
    for x in range(bw_game_state.width):
        for y in range(bw_game_state.height):
            pixel = bw_game_state.get_pixel(x, y)
            # if black pixel / dead cell
            if pixel.red == 0 and pixel.blue == 0 and pixel.green == 0:
                # dead cell
                # check if 3 neighbours are alive
                counter = cell_check(x, y, bw_game_state)
                if counter == 3:
                    # change pixel to white
                    new_state.set_rgb(x, y, 255, 255, 255)
            elif pixel.red == 255 and pixel.blue == 255 and pixel.green == 255:
                # live cell
                # check how many neighbours are alive
                counter = cell_check(x, y, bw_game_state)
                if counter != 2 and counter != 3:
                    # change pixel to black
                    new_state.set_rgb(x, y, 0, 0, 0)
    return new_state


def cell_check(x, y, bw_game_state):
    pixel_lst = []
    counter = 0
    # outside boundary is considered a dead cell
    for i in range(-1, 2):
        for j in range(-1, 2):
            try:
                pixel = bw_game_state.get_pixel(x + i, y + j)
                if not (i == 0 and j == 0):
                    pixel_lst.append(pixel.red)
            except:
                continue
    # checks number of live neighbours
    for colour in pixel_lst:
        if colour == 255:
            counter += 1
    return counter


def clean_up(initial_game_state, number_of_iterations):
    # removes temp files that were used to create gif
    print("Removing temp files.")
    for iterations in range(number_of_iterations + 1):
        os.remove(f"./temp/{initial_game_state}{iterations}.png")


if __name__ == '__main__':
    main()
