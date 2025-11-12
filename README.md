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

- Nielsen, M. A. & Chuang, I. L. *Quantum Computation and Quantum Information*. 10th Anniversary Edition, Cambridge University Press (2011).  
- Shor, P. W. “Algorithms for quantum computation: discrete logarithms and factoring.” *26th Annual Symposium on Foundations of Computer Science (FOCS)*, 124‑134 (1994).  
- Grover, L. K. “A fast quantum mechanical algorithm for database search.” *Proceedings of the 28th Annual ACM Symposium on the Theory of Computing (STOC)*, 212‑219 (1996).  
- IBM Quantum Experience — IBM’s cloud quantum computing platform and documentation. [https://quantum-computing.ibm.com](https://quantum-computing.ibm.com)  
- Qiskit Documentation — The open-source quantum computing SDK from IBM. [https://qiskit.org/documentation](https://qiskit.org/documentation)  
- 3Blue1Brown, *Quantum Computing Series* — A visual introduction to quantum computing concepts. [https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr](https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr)  
- Quantum Country — A mnemonic medium for learning quantum computing and related concepts. [https://quantum.country](https://quantum.country)  

