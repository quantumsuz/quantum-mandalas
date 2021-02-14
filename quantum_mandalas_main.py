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

# -- The smallest you can make the mandala output image is 200 x 200px.
# -- Image scale multiplies the scale of both x and y coordinates in the image to
# -- increase the resolution of the resulting mandala.
# -- E.g. image_scale = 10 will result in a 2000 x 2000px mandala
image_scale = 5
im = Image.new('RGB', (200*image_scale, 200*image_scale), (128, 128, 128))
draw = ImageDraw.Draw(im)

# -- These are the user-set options for how the final bmp image will look
mandala_outline_color = (255, 255, 255)
symmetry_lines_color = (255, 255, 255)
# mandala_fill_colors = [(255, 78, 36), (65, 26, 150)]

# -- This is the user-chosen passphrase to make their mandala unique
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
print("Solving QUBO...")
print("qubo solution = ", qubo_solution)
print("...............")

# ---------------- Hash the QUBO solution back to our mandala params ----------------------------------------- #

# - The QUBO solution controls the number of circles and squares that will be generated:
num_central_circles_rand = qubo_solution[0] * 4 + 1  # - 2 options
num_central_squares_rand = qubo_solution[1] * 4 + 1  # - 2 options
num_mirror_circles_rand = qubo_solution[1] * 4 + 1  # - 2 options
num_mirror_squares_rand = qubo_solution[1] * 4 + 1  # - 2 options

num_axis_circles_rand = 1
num_axis_squares_rand = 1

# - OR... set the params randomly if you want to just generate a random mandala
# num_central_circles_rand = random.randint(2, 5)  # - 4 options
# num_central_squares_rand = random.randint(2, 5)  # - 4 options
# num_mirror_circles_rand = random.randint(2, 5)  # - 4 options
# num_mirror_squares_rand = random.randint(2, 5)  # - 4 options

# -------------------------------- Draw the Mandala ---------------------------------------------------------- #

# -- These are the mandala symmetry lines
draw.line((0, 0, 200*image_scale, 200*image_scale), fill=symmetry_lines_color, width=1*image_scale)
draw.line((200*image_scale, 0, 0, 200*image_scale), fill=symmetry_lines_color, width=1*image_scale)
draw.line((100*image_scale, 0, 100*image_scale, 200*image_scale), fill=symmetry_lines_color, width=1*image_scale)
draw.line((0, 100*image_scale, 200*image_scale, 100*image_scale), fill=symmetry_lines_color, width=1*image_scale)

central_circle_sizes = [0]*num_central_circles_rand
central_square_sizes = [0]*num_central_squares_rand

# -- Create the entities that are central circles
for i in range(num_central_circles_rand):
    central_circle_size = random.randint(0, 20)
    central_circle_sizes[i] = central_circle_size # -- Here we add this to a list so we can "redraw" the outline later
    central_circle_fill = random.choice(mandala_fill_colors)
    draw.ellipse((100 * image_scale - central_circle_size * 5 * image_scale,
                  100 * image_scale - central_circle_size * 5 * image_scale,
                  100 * image_scale + central_circle_size * 5 * image_scale,
                  100 * image_scale + central_circle_size * 5 * image_scale),
                 fill=central_circle_fill, outline=mandala_outline_color, width=1 * image_scale)

# -- Create the entities that are central squares
for _ in range(num_central_squares_rand):
    central_square_size = random.randint(0, 20)
    central_square_sizes[i] = central_square_size  # -- Here we add this to a list so we can "redraw" the outline later
    central_square_fill = random.choice(mandala_fill_colors)
    draw.rectangle((100 * image_scale - central_square_size * 5 * image_scale,
                    100 * image_scale - central_square_size * 5 * image_scale,
                    100 * image_scale + central_square_size * 5 * image_scale,
                    100 * image_scale + central_square_size * 5 * image_scale),
                   fill=central_square_fill, outline=mandala_outline_color, width=1 * image_scale)

# - Create the circle entities that are mirrored 8-fold about the mandala symmetry lines
for _ in range(num_mirror_circles_rand):
    mirror_circle_x_coord = random.randint(0, 10)
    mirror_circle_y_coord = random.randint(mirror_circle_x_coord, 10)
    mirror_circle_fill = random.choice(mandala_fill_colors)
    mirror_circle_size = random.randint(2, 4)
    draw.ellipse((mirror_circle_x_coord * 10 * image_scale - mirror_circle_size * 5 * image_scale,
                  mirror_circle_y_coord * 10 * image_scale - mirror_circle_size * 5 * image_scale,
                  mirror_circle_x_coord * 10 * image_scale + mirror_circle_size * 5 * image_scale,
                  mirror_circle_y_coord * 10 * image_scale + mirror_circle_size * 5 * image_scale),
                 fill=mirror_circle_fill, outline=mandala_outline_color, width=1 * image_scale)

# - Create the square entities that are mirrored 8-fold about the mandala symmetry lines
for _ in range(num_mirror_squares_rand):
    mirror_square_x_coord = random.randint(0, 10)  # - Quantized the space into 10 units
    mirror_square_y_coord = random.randint(mirror_square_x_coord, 10)  # - Quantized the space into 10 units
    mirror_square_fill = random.choice(mandala_fill_colors)
    mirror_square_size = random.randint(2, 4)
    draw.rectangle((mirror_square_x_coord * 10 * image_scale - mirror_square_size * 5 * image_scale,
                    mirror_square_y_coord * 10 * image_scale - mirror_square_size * 5 * image_scale,
                    mirror_square_x_coord * 10 * image_scale + mirror_square_size * 5 * image_scale,
                    mirror_square_y_coord * 10 * image_scale + mirror_square_size * 5 * image_scale),
                   fill=mirror_square_fill, outline=mandala_outline_color, width=1 * image_scale)

im_pixels = list(im.getdata())[0:200*image_scale*200*image_scale]

# -- Mirror the initial octant of the pattern about the xy line in 4 different ways
for x in range(0, 100*image_scale):
    for y in range(x, 100*image_scale):
        pixel = im_pixels[x+y*200*image_scale]
        im.putpixel((-x, y), pixel)
        im.putpixel((-y, x), pixel)
        im.putpixel((-y, -x), pixel)
        im.putpixel((-x, -y), pixel)

# - Refresh the pixels in this array as they have been written over
im_pixels = list(im.getdata())[0:200*image_scale*200*image_scale]

# - Mirror entire right half of mandala vertically
for x in range(100*image_scale, 200*image_scale):
    for y in range(0, 200*image_scale):
        pixel = im_pixels[x + y*200*image_scale]
        im.putpixel((200*image_scale-x, y), pixel)

# -- Create the entities that are axis circles
for _ in range(num_axis_circles_rand):
    axis_circle_size = random.randint(1, 4)
    axis_circle_offset = random.randint(0, 10)
    axis_circle_fill = random.choice(mandala_fill_colors)
    # Draw the horizontally offset circles on x-axis
    draw.ellipse((100 * image_scale - axis_circle_size * 5 * image_scale + axis_circle_offset * 10 * image_scale,  # X1
                  100 * image_scale - axis_circle_size * 5 * image_scale,  # -- Y1
                  100 * image_scale + axis_circle_size * 5 * image_scale + axis_circle_offset * 10 * image_scale,  # X2
                  100 * image_scale + axis_circle_size * 5 * image_scale),  # - Y2
                 fill=axis_circle_fill, outline=mandala_outline_color, width=1 * image_scale)
    draw.ellipse((100 * image_scale - axis_circle_size * 5 * image_scale - axis_circle_offset * 10 * image_scale,  # X1
                  100 * image_scale - axis_circle_size * 5 * image_scale,  # -- Y1
                  100 * image_scale + axis_circle_size * 5 * image_scale - axis_circle_offset * 10 * image_scale,  # X2
                  100 * image_scale + axis_circle_size * 5 * image_scale),  # - Y2
                 fill=axis_circle_fill, outline=mandala_outline_color, width=1 * image_scale)
    # Draw the vertically offset circles on y-axis
    draw.ellipse((100 * image_scale - axis_circle_size * 5 * image_scale,  # -- X1
                  100 * image_scale - axis_circle_size * 5 * image_scale + axis_circle_offset * 10 * image_scale,  # Y1
                  100 * image_scale + axis_circle_size * 5 * image_scale,  # -- X2
                  100 * image_scale + axis_circle_size * 5 * image_scale + axis_circle_offset * 10 * image_scale),  # Y2
                 fill=axis_circle_fill, outline=mandala_outline_color, width=1 * image_scale)
    draw.ellipse((100 * image_scale - axis_circle_size * 5 * image_scale,  # -- X1
                  100 * image_scale - axis_circle_size * 5 * image_scale - axis_circle_offset * 10 * image_scale,  # Y1
                  100 * image_scale + axis_circle_size * 5 * image_scale,  # -- X2
                  100 * image_scale + axis_circle_size * 5 * image_scale - axis_circle_offset * 10 * image_scale),  # Y2
                 fill=axis_circle_fill, outline=mandala_outline_color, width=1 * image_scale)

# -- Create the entities that are axis squares
for _ in range(num_axis_squares_rand):
    axis_square_size = random.randint(1, 4)
    axis_square_offset = random.randint(0, 10)
    axis_square_fill = random.choice(mandala_fill_colors)
    # Draw the horizontally offset squares on x-axis
    draw.rectangle((100 * image_scale - axis_square_size * 5 * image_scale + axis_square_offset * 10 * image_scale,  # X1
                  100 * image_scale - axis_square_size * 5 * image_scale,  # -- Y1
                  100 * image_scale + axis_square_size * 5 * image_scale + axis_square_offset * 10 * image_scale,  # X2
                  100 * image_scale + axis_square_size * 5 * image_scale),  # - Y2
                 fill=axis_square_fill, outline=mandala_outline_color, width=1 * image_scale)
    draw.rectangle((100 * image_scale - axis_square_size * 5 * image_scale - axis_square_offset * 10 * image_scale,  # X1
                  100 * image_scale - axis_square_size * 5 * image_scale,  # -- Y1
                  100 * image_scale + axis_square_size * 5 * image_scale - axis_square_offset * 10 * image_scale,  # X2
                  100 * image_scale + axis_square_size * 5 * image_scale),  # - Y2
                 fill=axis_square_fill, outline=mandala_outline_color, width=1 * image_scale)
    # Draw the vertically offset squares on y-axis
    draw.rectangle((100 * image_scale - axis_square_size * 5 * image_scale,  # -- X1
                  100 * image_scale - axis_square_size * 5 * image_scale + axis_square_offset * 10 * image_scale,  # Y1
                  100 * image_scale + axis_square_size * 5 * image_scale,  # -- X2
                  100 * image_scale + axis_square_size * 5 * image_scale + axis_square_offset * 10 * image_scale),  # Y2
                 fill=axis_square_fill, outline=mandala_outline_color, width=1 * image_scale)
    draw.rectangle((100 * image_scale - axis_square_size * 5 * image_scale,  # -- X1
                  100 * image_scale - axis_square_size * 5 * image_scale - axis_square_offset * 10 * image_scale,  # Y1
                  100 * image_scale + axis_square_size * 5 * image_scale,  # -- X2
                  100 * image_scale + axis_square_size * 5 * image_scale - axis_square_offset * 10 * image_scale),  # Y2
                 fill=axis_square_fill, outline=mandala_outline_color, width=1 * image_scale)

# -- OPTIONAL REDRAW OF OUTLINES OF CENTRAL CIRCLES
for i in range(num_central_circles_rand):
    central_circle_size = central_circle_sizes[i]
    draw.ellipse((100 * image_scale - central_circle_size * 5 * image_scale,
                  100 * image_scale - central_circle_size * 5 * image_scale,
                  100 * image_scale + central_circle_size * 5 * image_scale,
                  100 * image_scale + central_circle_size * 5 * image_scale),
                 fill=None, outline=mandala_outline_color, width=1 * image_scale)

# -- OPTIONAL REDRAW OF OUTLINES OF CENTRAL SQUARES
for _ in range(num_central_squares_rand):
    central_square_size = central_square_sizes[i]
    draw.rectangle((100 * image_scale - central_square_size * 5 * image_scale,
                    100 * image_scale - central_square_size * 5 * image_scale,
                    100 * image_scale + central_square_size * 5 * image_scale,
                    100 * image_scale + central_square_size * 5 * image_scale),
                   fill=None, outline=mandala_outline_color, width=1 * image_scale)

# -- OPTIONAL REDRAW OF OUTLINES OF SYMMETRY LINES
draw.line((0, 0, 200*image_scale, 200*image_scale), fill=symmetry_lines_color, width=1*image_scale)
draw.line((200*image_scale, 0, 0, 200*image_scale), fill=symmetry_lines_color, width=1*image_scale)
draw.line((100*image_scale, 0, 100*image_scale, 200*image_scale), fill=symmetry_lines_color, width=1*image_scale)
draw.line((0, 100*image_scale, 200*image_scale, 100*image_scale), fill=symmetry_lines_color, width=1*image_scale)

print("Saving mandala output image...")
print("..............................")
im.save('mandala_image_output/quantum_mandala_example.bmp')
