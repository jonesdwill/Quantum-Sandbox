# Quantum-Sandbox
This repo is a personal diary for learning and experimenting with quantum computing. I have written it to be presented as a way of consolidating my knowledge and to refer back to. 

- **`1-CoinFlip.ipynb`**: A basic qubit manipulation experiment to gain familiarity with IBM Quantum backends.  


- **`2-RandomNumberGenerator.ipynb`**: Generates quantum random numbers.  
  - **`quantum_rng.py`**: A more formal script for generating random integers within a specified range.  
  - Future plans: extend to generate complex numbers, floats, and strings, and eventually package as a reusable library.  


- **`3-GroversAlgorithm.ipynb`**: Demonstrates a quantum search over an unstructured space in $O(\sqrt{N})$.  
  - **`grovers_algorithm.py`**: Proof-of-concept functions to find target integers in a list.  
  - Future plans: adapt for graph-theory problems, such as the Travelling Salesman Problem.  


- **`4-QFT.ipynb`**: Implementation of Quantum Fourier Transform.
  - **`qft.py`**: Script containing qft functionality for later use.


- **`5-ShorsAlgorithm.ipynb`**: Implementation of Shor's algorithm to factorize 15 on a quantum computer.
  - **`shors_algorithm.py`**: Script containing shors functionality.


- **`ibmq_connect.py`**: Connects to IBM runtime service.

## Dependencies
If you want to use any of the Scripts in this repo I reccomend setting up a virtual environment to use as your interpreter. If you don't have it already, install venv:
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
You can run the scripts from this virtual environment (when activated), or change the interpreter in your IDE. 

## References

- Nielsen, M. A. & Chuang, I. L. *Quantum Computation and Quantum Information*. 10th Anniversary Edition, Cambridge University Press (2011).  
- Shor, P. W. “Algorithms for quantum computation: discrete logarithms and factoring.” *26th Annual Symposium on Foundations of Computer Science (FOCS)*, 124‑134 (1994).  
- Grover, L. K. “A fast quantum mechanical algorithm for database search.” *Proceedings of the 28th Annual ACM Symposium on the Theory of Computing (STOC)*, 212‑219 (1996).  
- IBM Quantum Experience — IBM’s cloud quantum computing platform and documentation. [https://quantum-computing.ibm.com](https://quantum-computing.ibm.com)  
- Qiskit Documentation — The open-source quantum computing SDK from IBM. [https://qiskit.org/documentation](https://qiskit.org/documentation)  
- 3Blue1Brown, *Quantum Computing Series* — A visual introduction to quantum computing concepts. [https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr](https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr)  
- Quantum Country — A mnemonic medium for learning quantum computing and related concepts. [https://quantum.country](https://quantum.country)
- Mastriani, M. Quantum Fourier transform is the building block for creating entanglement. PMC Article (2021). Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC8593191/
- PennyLane Team. Intro to Quantum Fourier Transform. Tutorial (2024). Link: https://pennylane.ai/qml/demos/tutorial_qft
