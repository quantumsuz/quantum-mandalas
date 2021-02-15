# quantum-mandalas
Code to create mandala art using a quantum computer

Run quantum_mandalas_main.py and the code will generate a mandala image in bitmap format inside the 
mandala_image_output folder.

There are two options for configuring the mandala solver, accessed via setting the <code>use_QPU</code> flag. 
 
If <code>use_QPU = True</code>, the code will run on the D-Wave QPU (default) via the Leap API
If you do not have a D-Wave Leap account you can still run a small version of the problem locally using 
an enumeration solver (brute force method). To run the enumeration solver set <code>use_QPU = False</code>.