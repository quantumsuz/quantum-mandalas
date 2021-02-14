"""This is a script to take a user generated passphrase and turn it into a problem that can be solved
by an annealing-style quantum computer. The solution to the problem is rendered as a mandala pattern and saved as a
bmp. The design can then be hand-painted onto a canvas or coaster to create a unique gift.

Code Copyright Suzanne Gildert 2021

"""

from PIL import Image, ImageDraw
import random
from numpy import zeros
from quantum_mandalas_solver import enumeration_function
from quantum_mandalas_colorschemes import mandala_fill_colors

im = Image.new('RGB', (200, 200), (128, 128, 128))
draw = ImageDraw.Draw(im)

# -- These are the user-set options for how the final bmp image will look
mandala_outline_color = (255, 255, 255)
symmetry_lines_color = (255, 255, 255)
# mandala_fill_colors = [(255, 78, 36), (65, 26, 150)]

# -- This is the user-chosen passphrase to make their mandala unique to them
passphrase = "Quantum Mandalas Rock :)"

# -------------------------------- Hash the passphrase to a QUBO ----------------------------------------- #

# -- First we prepare the passphrase to make sure it is a fixed length
if len(passphrase) > 23:
    passphrase = passphrase[0:24]
elif len(passphrase) < 23:
    passphrase = passphrase + "3"*(24-len(passphrase))

# - Turn the passphrase into its numeric ascii equivalent
ascii_passphrase = [ord(c) for c in passphrase]

# - Hash the ascii passphrase into QUBO matrix co-efficients
# - The QUBO is a 4x4 matrix like this:
# -- Q = (0 0 0 0)
# --     (0 0 0 0)
# --     (0 0 0 0)
# --     (0 0 0 0)

QUBO_to_solve = zeros([4, 4])
Q = ascii_passphrase

QUBO_to_solve[0, 0] = Q[1] - Q[3] + Q[5] - Q[7] + Q[9] - Q[11]
QUBO_to_solve[1, 1] = Q[2] - Q[3] + Q[13] - Q[15] + Q[17] - Q[19]
QUBO_to_solve[2, 2] = Q[6] - Q[7] + Q[14] - Q[15] + Q[21] - Q[23]
QUBO_to_solve[3, 3] = Q[10] - Q[11] + Q[18] - Q[19] + Q[22] - Q[23]
QUBO_to_solve[0, 1] = Q[0] - Q[1] - Q[2] + Q[3]
QUBO_to_solve[0, 2] = Q[4] - Q[5] - Q[6] + Q[7]
QUBO_to_solve[0, 3] = Q[8] - Q[9] - Q[10] + Q[11]
QUBO_to_solve[1, 2] = Q[12] - Q[13] - Q[14] + Q[15]
QUBO_to_solve[1, 3] = Q[16] - Q[17] - Q[18] + Q[19]
QUBO_to_solve[2, 3] = Q[20] - Q[21] - Q[22] + Q[23]

# -------------------------------- Solve the QUBO ------------------------------------------------------------ #

# -- Here, instead of the enumeration function, we could use a call to the quantum hardware
# -- itself using D-Wave's Q_API.
qubo_solution = enumeration_function(QUBO_to_solve)
print("qubo solution = ", qubo_solution)

# ---------------- Hash the QUBO solution back to our mandala params ----------------------------------------- #

# - The QUBO solution controls the number of circles and squares that will be generated:
num_central_circles_rand = qubo_solution[0]*4+1  # - 2 options
num_central_squares_rand = qubo_solution[1]*4+1  # - 2 options
num_mirror_circles_rand = qubo_solution[1]*4+1  # - 2 options
num_mirror_squares_rand = qubo_solution[1]*4+1  # - 2 options

# - OR... set the params randomly if you want to just generate a random mandala
# num_central_circles_rand = random.randint(2, 5)  # - 4 options
# num_central_squares_rand = random.randint(2, 5)  # - 4 options
# num_mirror_circles_rand = random.randint(2, 5)  # - 4 options
# num_mirror_squares_rand = random.randint(2, 5)  # - 4 options

# -------------------------------- Draw the Mandala ---------------------------------------------------------- #

# -- These are the mandala symmetry lines
draw.line((0, 0, 200, 200), fill=symmetry_lines_color, width=1)
draw.line((200, 0, 0, 200), fill=symmetry_lines_color, width=1)
draw.line((100, 0, 100, 200), fill=symmetry_lines_color, width=1)
draw.line((0, 100, 200, 100), fill=symmetry_lines_color, width=1)

# -- Create the entities that are central circles
for _ in range(num_central_circles_rand):
    radius_rand_central_circles = random.randint(0, 20)
    rand_fill_central_circles = random.choice(mandala_fill_colors)
    draw.ellipse((100-radius_rand_central_circles*5,
                  100-radius_rand_central_circles*5,
                  100+radius_rand_central_circles*5,
                  100+radius_rand_central_circles*5),
                 fill=rand_fill_central_circles, outline=mandala_outline_color, width=1)

# -- Create the entities that are central squares
for _ in range(num_central_squares_rand):
    radius_rand_central_squares = random.randint(0, 20)
    rand_fill_central_squares = random.choice(mandala_fill_colors)
    draw.rectangle((100-radius_rand_central_squares*5,
                    100-radius_rand_central_squares*5,
                    100+radius_rand_central_squares*5,
                    100+radius_rand_central_squares*5),
                   fill=rand_fill_central_squares, outline=mandala_outline_color, width=1)

# - Create the circle entities that are mirrored 8-fold about the mandala symmetry lines
for _ in range(num_mirror_circles_rand):
    x_rand_mirror_circles = random.randint(0, 10)
    print(x_rand_mirror_circles)
    y_rand_mirror_circles = random.randint(x_rand_mirror_circles, 10)
    print(y_rand_mirror_circles)
    rand_fill_mirror_circles = random.choice(mandala_fill_colors)
    radius_rand_mirror_circles = random.randint(2, 4)
    draw.ellipse((x_rand_mirror_circles*10-radius_rand_mirror_circles*5,
                  y_rand_mirror_circles*10-radius_rand_mirror_circles*5,
                  x_rand_mirror_circles*10+radius_rand_mirror_circles*5,
                  y_rand_mirror_circles*10+radius_rand_mirror_circles*5),
                 fill=rand_fill_mirror_circles, outline=mandala_outline_color, width=1)

# - Create the square entities that are mirrored 8-fold about the mandala symmetry lines
for _ in range(num_mirror_squares_rand):
    x_rand_mirror_squares = random.randint(0, 10)  # - Quantized the space into 10 units
    y_rand_mirror_squares = random.randint(x_rand_mirror_squares, 10)  # - Quantized the space into 10 units
    rand_fill_mirror_squares = random.choice(mandala_fill_colors)
    radius_rand_mirror_squares = random.randint(2, 4)
    draw.rectangle((x_rand_mirror_squares*10-radius_rand_mirror_squares*5,
                    y_rand_mirror_squares*10-radius_rand_mirror_squares*5,
                    x_rand_mirror_squares*10+radius_rand_mirror_squares*5,
                    y_rand_mirror_squares*10+radius_rand_mirror_squares*5),
                   fill=rand_fill_mirror_squares, outline=mandala_outline_color, width=1)

im_pixels = list(im.getdata())[0:200*200]

# -- Mirror the initial octant of the pattern about the xy line in 4 different ways
for x in range(0, 100):
    for y in range(x, 100):
        pixel = im_pixels[x+y*200]
        im.putpixel((-x, y), pixel)
        im.putpixel((-y, x), pixel)
        im.putpixel((-y, -x), pixel)
        im.putpixel((-x, -y), pixel)

# - Refresh the pixels in this array as they have been written over
im_pixels = list(im.getdata())[0:200*200]

# - Mirror entire right half of mandala vertically
for x in range(100, 200):
    for y in range(0, 200):
        pixel = im_pixels[x + y*200]
        im.putpixel((200-x, y), pixel)

im.save('mandala_image_output/quantum_mandala_example.bmp')
