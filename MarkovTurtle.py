"""
Module Docstring
Creator: Andy Stoneman
Class/Section: Computational Creativity (CSCI 3725)
Assignment: M3: A Markov Distinction
Date: 09/14/2022
Description: A class that creates abstract art using a transition matrix and the turtle module. The abstract art
generated is intentionally different every time the program is run.
Bugs: No currently known bugs.
"""
import turtle
import numpy as np
import random


class MarkovTurtle:
    """
    A class that creates a 'MarkovTurtle,' which is a turtle that can draw abstract art using a Markov Chain.
    The class gives the option to provide your own markov chain table or have one randomly generated for you.
    In addition, you can specify the speed that the turtle draws the art, and you can also specify the starting shape.

    Args:
        speed (int): Determines the speed at which the MarkovTurtle will draw. Defaulted to zero.

        transition_matrix (dict): A transition matrix based on markov chains. Used to determine probability of
        particular shapes being drawn. If not specified, one will randomly be generated.

        num_instructions (int): The number of instructions/shapes that the MarkovTurtle should draw. Defaulted to
        10 if not specified.

        start_shape (str): The shape that the transition matrix/drawing will start with. Defaulted to 'circles'
        if not specified.
    """
    def __init__(self, speed=0, transition_matrix=None, num_instructions=10, start_shape="circles"):
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.speed(speed)
        self.turtle.pencolor("white")
        self.turtle.screen.bgcolor('black')
        self.turtle.screen.setup(1800, 1800)
        self.start_shape = start_shape
        self.num_instructions = num_instructions
        if transition_matrix is None:
            self.transition_matrix = {}
            self.options = ['circles', 'squares', 'dots', 'random walk', 'circular helix', 'hexagonal helix', 'flower']
            self.generate_markov_chain()
        else:
            self.transition_matrix = transition_matrix
            self.options = list(transition_matrix.keys())
        self.instructions = self.get_instructions()

    def generate_markov_chain(self):
        """Generates a randomized transition matrix."""
        probabilities = np.random.random(7)
        probabilities /= probabilities.sum()
        for option in self.options:
            temp_dict = {}
            for i in range(len(self.options)):
                temp_dict[self.options[i]] = probabilities[i]
            self.transition_matrix[option] = temp_dict

    def next_instruction(self, current_shape):
        """
        Generates the next instruction/drawing based on the transition matrix. Invoked by get_instructions().

        Args:
            current_shape (str): The shape or piece of art that is currently being chosen from the transition matrix.
            """
        return np.random.choice(
            self.options,
            p=[self.transition_matrix[current_shape][next_option] for next_option in self.options])

    def get_instructions(self):
        """Creates a list of instructions based on the transition matrix and repeatedly calling next_instruction()."""
        instructions = []
        while len(instructions) < self.num_instructions:
            next_instruction = self.next_instruction(self.start_shape)
            instructions.append(next_instruction)
            self.start_shape = next_instruction
        return instructions

    def draw(self):
        """
        Using the instructions from the transition matrix, repeatedly calls create method to draw various art.
        Also prints all instructions to the python shell as they're being drawn.
        """
        for i in range(len(self.instructions)):
            print(str(i) + " " + self.instructions[i])
            self.create(self.instructions[i])

    def create(self, instruction):
        """
        Guiding method to run the drawing process. Calls methods based on instructions given from draw().

        Args:
            instruction (str): The instruction/drawing that create will call next. Passed in by draw().
        """
        self.turtle.penup()
        if instruction == "circles":
            self.random_color_density()
            self.random_location()
            self.circles()
        elif instruction == "squares":
            self.random_color_density()
            self.random_location()
            self.squares()
        elif instruction == "dots":
            self.random_color_density()
            self.random_location()
            self.dots()
        elif instruction == "random walk":
            self.random_color_density()
            self.random_location()
            self.random_walk()
        elif instruction == "circular helix":
            self.random_color_density()
            self.random_location()
            self.circular_helix()
        elif instruction == "hexagonal helix":
            self.hexagonal_helix()
        elif instruction == "flower":
            self.flower()

    def wall_check(self):
        """Ensures that the MarkovTurtle does not draw too closely to the wall such that the art isn't visible."""
        self.turtle.penup()
        if self.turtle.xcor() > 500:
            self.turtle.goto(450, self.turtle.ycor())
        elif self.turtle.xcor() < -500:
            self.turtle.goto(-450, self.turtle.ycor())

        if self.turtle.ycor() < -500:
            self.turtle.goto(self.turtle.xcor(), -450)
        elif self.turtle.ycor() > 500:
            self.turtle.goto(self.turtle.xcor(), 450)
        self.turtle.pendown()

    def random_color_density(self):
        """Randomizes the color of lines and the thickness/width of lines. Used to create variation."""
        colors = ["yellow", "pink", "red", "purple", "light blue"]
        self.turtle.color(random.choice(colors))
        self.turtle.width(random.randint(5, 15))

    def random_location(self):
        """Generates a random location for the MarkovTurtle to move to on the screen."""
        x = random.randint(-600, 600)
        y = random.randint(-400, 400)
        self.turtle.goto(x, y)

    def circles(self):
        """Draws five circles of random size and location."""
        for i in range(5):
            self.random_location()
            radius = random.randint(5, 30)
            self.wall_check()
            self.turtle.pendown()
            self.turtle.circle(radius)

    def squares(self):
        """Draws five squares of random orientation and location."""
        for i in range(5):
            self.random_location()
            self.wall_check()
            self.turtle.pendown()
            for j in range(4):
                self.turtle.right(random.randint(0, 90))
                self.turtle.forward(50)
                self.turtle.right(90)

    def dots(self):
        """Draws ten dots in random locations of random sizes."""
        for i in range(10):
            self.random_location()
            self.wall_check()
            size = random.randint(5, 30)
            self.turtle.pendown()
            self.turtle.dot(size)

    def random_walk(self):
        """Draws a randomly 'walking' line in the drawing."""
        count = 0
        self.turtle.pendown()
        while count < 50:
            self.wall_check()
            self.turtle.forward(random.randint(30, 100))
            self.turtle.right(random.randint(0, 360))
            count += 1

    def circular_helix(self):
        """Draws a circular helix in a random location."""
        self.wall_check()
        self.turtle.pendown()
        for i in range(25):
            self.turtle.speed(0)
            self.turtle.circle(5 * i)
            self.turtle.circle(-5 * i)
            self.turtle.left(i)

    def hexagonal_helix(self):
        """Draws a hexagonal, colored helix in a random location."""
        x = random.randint(-500, 500)
        y = random.randint(-300, 300)
        self.turtle.goto(x, y)
        self.wall_check()
        colors = ['red', 'purple', 'blue', 'green', 'orange', 'yellow']
        for x in range(180):
            self.turtle.pencolor(colors[x % 6])
            self.turtle.width(x // 100 + 1)
            self.turtle.forward(x)
            self.turtle.left(59)

    def flower(self):
        """Draws a flower-like object in different colors in a random location."""
        x = random.randint(-500, 500)
        y = random.randint(-300, 300)
        self.turtle.goto(x, y)
        self.wall_check()
        colors = ["yellow", "pink", "red", "purple", "light blue"]
        for i in range(10):
            for j in range(2):
                self.turtle.forward(100)
                self.turtle.right(60)
                self.turtle.forward(100)
                self.turtle.right(120)
            self.turtle.right(36)
            self.turtle.color(random.choice(colors))


def main():
    # Artist one option using a written transition matrix and an assigned speed
    artist = MarkovTurtle(0, {
        "circles": {"circles": 0.2, "squares": 0.1, "dots": 0.1, "random walk": 0.3, "circular helix": 0.1,
                    "hexagonal helix": 0.1, "flower": 0.1},
        "squares": {"circles": 0.2, "squares": 0.1, "dots": 0.1, "random walk": 0.3, "circular helix": 0.1,
                    "hexagonal helix": 0.1, "flower": 0.1},
        "dots": {"circles": 0.2, "squares": 0.1, "dots": 0.1, "random walk": 0.3, "circular helix": 0.1,
                 "hexagonal helix": 0.1, "flower": 0.1},
        "random walk": {"circles": 0.2, "squares": 0.1, "dots": 0.1, "random walk": 0.3, "circular helix": 0.1,
                        "hexagonal helix": 0.1, "flower": 0.1},
        "circular helix": {"circles": 0.2, "squares": 0.1, "dots": 0.1, "random walk": 0.3, "circular helix": 0.1,
                           "hexagonal helix": 0.1, "flower": 0.1},
        "hexagonal helix": {"circles": 0.2, "squares": 0.1, "dots": 0.1, "random walk": 0.3, "circular helix": 0.1,
                            "hexagonal helix": 0.1, "flower": 0.1},
        "flower": {"circles": 0.2, "squares": 0.1, "dots": 0.1, "random walk": 0.3, "circular helix": 0.1,
                   "hexagonal helix": 0.1, "flower": 0.1}
    })
    # artist.draw() # Temporarily commented out so only one work is drawn.

    # Artist two option that uses all default values.
    artist_two = MarkovTurtle()
    artist_two.draw()

    # Used to keep the picture up after completion of drawing.
    turtle.done()


if __name__ == "__main__":
    main()
