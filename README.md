# quantum-mandalas
### Code to create mandala-style art using a quantum computer

The idea of quantum and spirituality have long been linked. 
Now we can generate powerful patterns from the fabric of the multiverse itself. Whether you are a math-loving computer geek, a deeply spiritual soul, or just someone looking for a cool birthday gift idea, mandala art computed from the energies in the quantum multiverse has something to offer you :) 

#### How to use the code

Run <code>quantum_mandalas_main.py</code> and the code will generate a mandala image in bitmap format inside the 
mandala_image_output folder.

#### Making your mandala special

The code includes a variable known as the **"special mandala message"**. This is a word or phrase that is used to construct the computational problem 
that is passed to the quantum computer. The solution returned from the computer is then used to shape the pattern of the mandala. For example, you could set the phrase to be your name, 
your birthday, your own name plus the name of a loved one, a description of your pet, or just simply a meaningful phrase, poem, or song lyric. The ideal length of the message is around 24 characters.


#### The quantum computing part

There are two options for configuring the mandala solver, accessed via setting the <code>use_QPU</code> flag. 
 
If <code>use_QPU = True</code>, the code will run on the D-Wave QPU (default) via the Leap API
If you do not have a D-Wave Leap account you can still run a small version of the problem locally using 
an enumeration solver (brute force method). To run the enumeration solver set <code>use_QPU = False</code>.

#### Examples of Quantum Mandalas generated using this code:

![Alt text](./mandala_image_output/quantum_mandalas_compilation.jpg?raw=true "Quantum Mandala Examples")