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
from dwave.system import EmbeddingComposite, DWaveSampler
from dimod import BinaryQuadraticModel

# ---------------------------- USER SETTINGS FOR MANDALA AESTHETICS ------------------------------------- #
# -- These are user-settings for how the final mandala bmp image will look

# -- The smallest mandala output image allowed is 200 x 200px, im_scale = 1
# -- Image scale multiplies the scale of both x and y to increase the resolution of the resulting mandala.
# -- E.g. im_scale = 10 results in a 2000 x 2000px mandala
im_scale = 5
mandala_outline_color = (255, 255, 255)
symmetry_lines_color = (255, 255, 255)

# -- This parameter allows you to switch between the local solver and the quantum computer
use_QPU = False
# -- This is the user-chosen passphrase to make their mandala unique
passphrase = "Quantum Mandalas Rock :)"

# ---------------------------- Hash the passphrase to a set of numeric values ---------------------------- #

# -- First we prepare the passphrase to make sure it is a fixed length
if len(passphrase) > 23:
    passphrase = passphrase[0:24]
elif len(passphrase) < 23:
    passphrase = passphrase + "3"*(24-len(passphrase))

# - Turn the passphrase into its numeric ascii equivalent
ascii_passphrase = [ord(c) for c in passphrase]

# -------------------------------- TEST SMALL QUBO WITH ENUMERATION SOLVER  ------------------------------ #
if not use_QPU:
    print("Solving QUBO using local enumeration solver...")
    # -- Hash the ascii passphrase into QUBO matrix co-efficients
    # -- The QUBO is a 4x4 matrix like this:
    # -- QUBO = (0 0 0 0)
    # --        (0 0 0 0)
    # --        (0 0 0 0)
    # --        (0 0 0 0)
    # -- This is a very small QUBO for testing purposes

    Q = zeros([4, 4])

    Q[0, 0] = ascii_passphrase[0]
    Q[1, 1] = ascii_passphrase[1]*-1
    Q[2, 2] = ascii_passphrase[2]
    Q[3, 3] = ascii_passphrase[3]*-1
    Q[0, 1] = ascii_passphrase[4]
    Q[0, 2] = ascii_passphrase[5]*-1
    Q[0, 3] = ascii_passphrase[6]
    Q[1, 2] = ascii_passphrase[7]*-1
    Q[1, 3] = ascii_passphrase[8]
    Q[2, 3] = ascii_passphrase[9]*-1

    # -- For very small QUBOs, use enumeration solver:
    qubo_solution_list = enumeration_function(Q)
    qubo_solution = {'A': qubo_solution_list[0],
                     'B': qubo_solution_list[1],
                     'C': qubo_solution_list[2],
                     'D': qubo_solution_list[3]
                     }

# -------------------------------- FULL-SIZE QUBO WITH D-WAVE LEAP BQM SOLVER ---------------------------- #
else:
    print("Solving QUBO using D-Wave QPU...")
    # -- As the QUBOs get bigger, enumeration approach becomes impossible (exponentially many states).
    # -- Here, instead of the enumeration function, we use a call to the quantum hardware using D-Wave's Q_API.

    # -- Hash the ascii passphrase into QUBO matrix co-efficients in a Python dict
    Q = {('A', 'A'): ascii_passphrase[0],
         ('B', 'B'): ascii_passphrase[1]*-1,
         ('C', 'C'): ascii_passphrase[2],
         ('D', 'D'): ascii_passphrase[3]*-1,
         ('A', 'B'): ascii_passphrase[4],
         ('A', 'C'): ascii_passphrase[5]*-1,
         ('A', 'D'): ascii_passphrase[6],
         ('B', 'C'): ascii_passphrase[7]*-1,
         ('B', 'D'): ascii_passphrase[8],
         ('C', 'D'): ascii_passphrase[9]*-1,
         }

    # Convert the problem to a BQM
    bqm = BinaryQuadraticModel.from_qubo(Q)

    # -- Define the sampler that will be used to run the problem
    sampler = EmbeddingComposite(DWaveSampler())

    # Run the problem on the sampler and print the results
    qubo_solution = sampler.sample(bqm, num_reads=1, label='BQM from passphrase')
    qubo_solution = qubo_solution.first.sample

# ---------------- Hash the QUBO solution back to our mandala params ----------------------------------------- #

print("qubo solution = ", qubo_solution)
print("...............")

# - The QUBO solution controls the number of circles and squares that will be generated:
num_central_circles_rand = qubo_solution['A'] + 2  # - 2 options
num_central_squares_rand = qubo_solution['B'] + 2  # - 2 options
num_mirror_circles_rand = qubo_solution['C'] + 2  # - 2 options
num_mirror_squares_rand = qubo_solution['D'] + 2  # - 2 options

num_axis_circles_rand = 1
num_axis_squares_rand = 1

# - OR... set the params randomly if you want to just generate a random mandala
# num_central_circles_rand = random.randint(2, 5)  # - 4 options
# num_central_squares_rand = random.randint(2, 5)  # - 4 options
# num_mirror_circles_rand = random.randint(2, 5)  # - 4 options
# num_mirror_squares_rand = random.randint(2, 5)  # - 4 options

# -------------------------------- Draw the Mandala ---------------------------------------------------------- #

# - Creates a new blank canvas on which to render the mandala
im = Image.new('RGB', (200 * im_scale, 200 * im_scale), (128, 128, 128))
draw = ImageDraw.Draw(im)

# -- These are the mandala symmetry lines
draw.line((0, 0, 200 * im_scale, 200 * im_scale), fill=symmetry_lines_color, width=1 * im_scale)
draw.line((200 * im_scale, 0, 0, 200 * im_scale), fill=symmetry_lines_color, width=1 * im_scale)
draw.line((100 * im_scale, 0, 100 * im_scale, 200 * im_scale), fill=symmetry_lines_color, width=1 * im_scale)
draw.line((0, 100 * im_scale, 200 * im_scale, 100 * im_scale), fill=symmetry_lines_color, width=1 * im_scale)

# - A couple of lists to store some of the random variables so we can "redraw" the outlines later
central_circle_sizes = [0] * num_central_circles_rand
central_square_sizes = [0] * num_central_squares_rand

# -- Create the entities that are central circles
for i in range(num_central_circles_rand):
    central_circle_size = random.randint(0, 20)
    central_circle_sizes[i] = central_circle_size  # -- Here we add this to a list so we can "redraw" the outline later
    central_circle_fill = random.choice(mandala_fill_colors)
    draw.ellipse((100 * im_scale - central_circle_size * 5 * im_scale,
                  100 * im_scale - central_circle_size * 5 * im_scale,
                  100 * im_scale + central_circle_size * 5 * im_scale,
                  100 * im_scale + central_circle_size * 5 * im_scale),
                 fill=central_circle_fill, outline=mandala_outline_color, width=1 * im_scale)

# -- Create the entities that are central squares
for i in range(num_central_squares_rand):
    central_square_size = random.randint(0, 20)
    central_square_sizes[i] = central_square_size   # -- Here we add this to a list so we can "redraw" the outline later
    central_square_fill = random.choice(mandala_fill_colors)
    draw.rectangle((100 * im_scale - central_square_size * 5 * im_scale,
                    100 * im_scale - central_square_size * 5 * im_scale,
                    100 * im_scale + central_square_size * 5 * im_scale,
                    100 * im_scale + central_square_size * 5 * im_scale),
                   fill=central_square_fill, outline=mandala_outline_color, width=1 * im_scale)

# - Create the circle entities that are mirrored 8-fold about the mandala symmetry lines
for _ in range(num_mirror_circles_rand):
    mirror_circle_x_coord = random.randint(0, 10)
    mirror_circle_y_coord = random.randint(mirror_circle_x_coord, 10)
    mirror_circle_fill = random.choice(mandala_fill_colors)
    mirror_circle_size = random.randint(2, 4)
    draw.ellipse((mirror_circle_x_coord * 10 * im_scale - mirror_circle_size * 5 * im_scale,
                  mirror_circle_y_coord * 10 * im_scale - mirror_circle_size * 5 * im_scale,
                  mirror_circle_x_coord * 10 * im_scale + mirror_circle_size * 5 * im_scale,
                  mirror_circle_y_coord * 10 * im_scale + mirror_circle_size * 5 * im_scale),
                 fill=mirror_circle_fill, outline=mandala_outline_color, width=1 * im_scale)

# - Create the square entities that are mirrored 8-fold about the mandala symmetry lines
for _ in range(num_mirror_squares_rand):
    mirror_square_x_coord = random.randint(0, 10)  # - Quantized the space into 10 units
    mirror_square_y_coord = random.randint(mirror_square_x_coord, 10)  # - Quantized the space into 10 units
    mirror_square_fill = random.choice(mandala_fill_colors)
    mirror_square_size = random.randint(2, 4)
    draw.rectangle((mirror_square_x_coord * 10 * im_scale - mirror_square_size * 5 * im_scale,
                    mirror_square_y_coord * 10 * im_scale - mirror_square_size * 5 * im_scale,
                    mirror_square_x_coord * 10 * im_scale + mirror_square_size * 5 * im_scale,
                    mirror_square_y_coord * 10 * im_scale + mirror_square_size * 5 * im_scale),
                   fill=mirror_square_fill, outline=mandala_outline_color, width=1 * im_scale)

# -- Mirror the initial octant of the pattern about the xy line in 4 different ways
im_pixels = list(im.getdata())[0:200 * im_scale * 200 * im_scale]

for x in range(0, 100 * im_scale):
    for y in range(x, 100 * im_scale):
        pixel = im_pixels[x + y * 200 * im_scale]
        im.putpixel((-x, y), pixel)
        im.putpixel((-y, x), pixel)
        im.putpixel((-y, -x), pixel)
        im.putpixel((-x, -y), pixel)

# - Refresh the pixels in this array as they have been written over
im_pixels = list(im.getdata())[0:200 * im_scale * 200 * im_scale]

# - Mirror entire right half of mandala vertically
for x in range(100 * im_scale, 200 * im_scale):
    for y in range(0, 200 * im_scale):
        pixel = im_pixels[x + y * 200 * im_scale]
        im.putpixel((200 * im_scale - x, y), pixel)

# -- Create the entities that are axis circles
for _ in range(num_axis_circles_rand):
    axis_circle_size = random.randint(1, 4)
    axis_circle_offset = random.randint(0, 10)
    axis_circle_fill = random.choice(mandala_fill_colors)
    # Draw the horizontally offset circles on x-axis
    draw.ellipse((100 * im_scale - axis_circle_size * 5 * im_scale + axis_circle_offset * 10 * im_scale,  # X1
                  100 * im_scale - axis_circle_size * 5 * im_scale,  # -- Y1
                  100 * im_scale + axis_circle_size * 5 * im_scale + axis_circle_offset * 10 * im_scale,  # X2
                  100 * im_scale + axis_circle_size * 5 * im_scale),  # - Y2
                 fill=axis_circle_fill, outline=mandala_outline_color, width=1 * im_scale)
    draw.ellipse((100 * im_scale - axis_circle_size * 5 * im_scale - axis_circle_offset * 10 * im_scale,  # X1
                  100 * im_scale - axis_circle_size * 5 * im_scale,  # -- Y1
                  100 * im_scale + axis_circle_size * 5 * im_scale - axis_circle_offset * 10 * im_scale,  # X2
                  100 * im_scale + axis_circle_size * 5 * im_scale),  # - Y2
                 fill=axis_circle_fill, outline=mandala_outline_color, width=1 * im_scale)
    # Draw the vertically offset circles on y-axis
    draw.ellipse((100 * im_scale - axis_circle_size * 5 * im_scale,  # -- X1
                  100 * im_scale - axis_circle_size * 5 * im_scale + axis_circle_offset * 10 * im_scale,  # Y1
                  100 * im_scale + axis_circle_size * 5 * im_scale,  # -- X2
                  100 * im_scale + axis_circle_size * 5 * im_scale + axis_circle_offset * 10 * im_scale),  # Y2
                 fill=axis_circle_fill, outline=mandala_outline_color, width=1 * im_scale)
    draw.ellipse((100 * im_scale - axis_circle_size * 5 * im_scale,  # -- X1
                  100 * im_scale - axis_circle_size * 5 * im_scale - axis_circle_offset * 10 * im_scale,  # Y1
                  100 * im_scale + axis_circle_size * 5 * im_scale,  # -- X2
                  100 * im_scale + axis_circle_size * 5 * im_scale - axis_circle_offset * 10 * im_scale),  # Y2
                 fill=axis_circle_fill, outline=mandala_outline_color, width=1 * im_scale)

# -- Create the entities that are axis squares
for _ in range(num_axis_squares_rand):
    axis_square_size = random.randint(1, 4)
    axis_square_offset = random.randint(0, 10)
    axis_square_fill = random.choice(mandala_fill_colors)
    # Draw the horizontally offset squares on x-axis
    draw.rectangle((100 * im_scale - axis_square_size * 5 * im_scale + axis_square_offset * 10 * im_scale,  # X1
                    100 * im_scale - axis_square_size * 5 * im_scale,  # -- Y1
                    100 * im_scale + axis_square_size * 5 * im_scale + axis_square_offset * 10 * im_scale,  # X2
                    100 * im_scale + axis_square_size * 5 * im_scale),  # - Y2
                   fill=axis_square_fill, outline=mandala_outline_color, width=1 * im_scale)
    draw.rectangle((100 * im_scale - axis_square_size * 5 * im_scale - axis_square_offset * 10 * im_scale,  # X1
                    100 * im_scale - axis_square_size * 5 * im_scale,  # -- Y1
                    100 * im_scale + axis_square_size * 5 * im_scale - axis_square_offset * 10 * im_scale,  # X2
                    100 * im_scale + axis_square_size * 5 * im_scale),  # - Y2
                   fill=axis_square_fill, outline=mandala_outline_color, width=1 * im_scale)
    # Draw the vertically offset squares on y-axis
    draw.rectangle((100 * im_scale - axis_square_size * 5 * im_scale,  # -- X1
                    100 * im_scale - axis_square_size * 5 * im_scale + axis_square_offset * 10 * im_scale,  # Y1
                    100 * im_scale + axis_square_size * 5 * im_scale,  # -- X2
                    100 * im_scale + axis_square_size * 5 * im_scale + axis_square_offset * 10 * im_scale),  # Y2
                   fill=axis_square_fill, outline=mandala_outline_color, width=1 * im_scale)
    draw.rectangle((100 * im_scale - axis_square_size * 5 * im_scale,  # -- X1
                    100 * im_scale - axis_square_size * 5 * im_scale - axis_square_offset * 10 * im_scale,  # Y1
                    100 * im_scale + axis_square_size * 5 * im_scale,  # -- X2
                    100 * im_scale + axis_square_size * 5 * im_scale - axis_square_offset * 10 * im_scale),  # Y2
                   fill=axis_square_fill, outline=mandala_outline_color, width=1 * im_scale)

# -- OPTIONAL REDRAW OF OUTLINES OF CENTRAL CIRCLES
for i in range(num_central_circles_rand):
    central_circle_size = central_circle_sizes[i]
    draw.ellipse((100 * im_scale - central_circle_size * 5 * im_scale,
                  100 * im_scale - central_circle_size * 5 * im_scale,
                  100 * im_scale + central_circle_size * 5 * im_scale,
                  100 * im_scale + central_circle_size * 5 * im_scale),
                 fill=None, outline=mandala_outline_color, width=1 * im_scale)

# -- OPTIONAL REDRAW OF OUTLINES OF CENTRAL SQUARES
for i in range(num_central_squares_rand):
    central_square_size = central_square_sizes[i]
    draw.rectangle((100 * im_scale - central_square_size * 5 * im_scale,
                    100 * im_scale - central_square_size * 5 * im_scale,
                    100 * im_scale + central_square_size * 5 * im_scale,
                    100 * im_scale + central_square_size * 5 * im_scale),
                   fill=None, outline=mandala_outline_color, width=1 * im_scale)

# -- OPTIONAL REDRAW OF OUTLINES OF SYMMETRY LINES
draw.line((0, 0, 200 * im_scale, 200 * im_scale), fill=symmetry_lines_color, width=1 * im_scale)
draw.line((200 * im_scale, 0, 0, 200 * im_scale), fill=symmetry_lines_color, width=1 * im_scale)
draw.line((100 * im_scale, 0, 100 * im_scale, 200 * im_scale), fill=symmetry_lines_color, width=1 * im_scale)
draw.line((0, 100 * im_scale, 200 * im_scale, 100 * im_scale), fill=symmetry_lines_color, width=1 * im_scale)

print("Saving mandala output image...")
print("..............................")
im.save('mandala_image_output/quantum_mandala_example.bmp')
