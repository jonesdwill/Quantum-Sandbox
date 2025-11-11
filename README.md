# Quantum-Sandbox
This repo is a diary for quantum computing learning and experiments. It contains the following:
 - **Coinflip**: Basic manipulation of qubit and familiarity with IBM backend. 
 - **Random Number Generator**:  What it says on the tin. Can generate large random numbers.
      - **quantum_rng.py**: A more formal Script. Can be used to random integers in some range.
      - Want to add complex, float and string generation, and turn into a package.
 - **Grover's Algorithm**: Can be used to perform a search of an unstructured search space in $O(\sqrt{N})$.
      - **grovers_algorithm.py** Proof of concept set of functions to find target integers in a list.
      - Want to adapt to graph theory to solve other problems such as travelling salesman.
 - **Cryptography**: Implementation of Shor's algorithm to factorise 15 on QC.

## Dependencies
If you want to use any of the Scripts or packages in this repo I reccomend setting up a virtual environment to use as your interpreter. If you don't have it already, install venv:
```
py -m pip install venv
```
Navigate to project directory, or wherever you want to store your virtual environment:
```
cd path\to\project
```
Create virtual environment and install packages:
```
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
You can run the scripts from this virtual environment (when activated), or change the interpreter to use this venv in your IDE. 

## References
