import os
import sys
import numpy as np
from dotenv import load_dotenv
from qiskit import *
from qiskit.visualization import plot_histogram
from qiskit_aer import *
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import (SamplerV2 as Sampler)
from qiskit.primitives import (BackendSamplerV2)
from requests.packages import target

def initialise(n: int):
    '''
    Initialise the quantum circuit with n qubits in equal superposition
    :param n: number of qubits
    :return: quantum circuit with n-qubits
    '''

    # n-qubit quantum register
    _qr = QuantumRegister(_num_qubits, "qubit")

    qc = QuantumCircuit(_qr)

    # equal superposition
    qc.h(_qr)

    qc.barrier()

    return qc

def flip_state(target: str, qc: QuantumCircuit, state:str = '0'):
    '''
    Flips qubits of target state
    :param target: target state
    :
    '''
    for i, bit in enumerate(target):
        if bit == state: qc.x(i)


def oracle_operator(n: int, targets: list[str]):
    '''
    Oracle function to phase-flip target states
    :param n: number of qubits
    :param targets: list of target states to phase-flip
    :return: oracle circuit
    '''
    # generate circuit
    oracle = QuantumCircuit(_qr, name='Oracle')

    # loop over target states
    for target in targets:

        # flip target state 0 -> 1.
        flip_state(target, oracle)

        # MCZ Gate on n-th qubit
        oracle.h(n-1)
        oracle.mcx(list(range(n-1)), n-1)
        oracle.h(n-1)

        # Undo relevant flips 1 -> 0.
        flip_state(target, oracle)

    return oracle


def diffusion_operator(n: int):
    '''
    Diffusion operator function to reflect in the |00..0> basis.
    :param n: number of qubits
    :return: diffusion operator circuit
    '''

    diffusion = QuantumCircuit(_qr, name='Diffusion Operator')

    # Hadamard and X Gate all states
    diffusion.h(_qr)
    diffusion.x(_qr)

    # MCZ Operator to the target state (|11...1>)
    diffusion.h(n-1)
    diffusion.mcx(list(range(n-1)), n-1)
    diffusion.h(n-1)

    # Reverse Hadamard and X Gates
    diffusion.x(_qr)
    diffusion.h(_qr)

    return diffusion

def grovers_circuit(n, targets):
    '''
    Circuit representing Grover's algorithm
    :param n: number of qubits
    :param targets: list of target states
    :return: circuit containing Grover's algorithm
    '''
    grovers = initialise(n)

    for _ in range(_num_its):
        grovers.barrier()
        oracle = oracle_operator(n, targets)
        grovers.append(oracle,_qr)
        grovers.barrier()
        diff = diffusion_operator(n)
        grovers.append(diff, _qr)

    cr = ClassicalRegister(n)
    grovers.measure_all()
    return grovers

def run_grovers(n: int, targets: list[str], num_shots: int = 1000, on_hardware: bool = False):
    '''
    Function to run Grover's algorithm.
    :param n: number of wubits
    :param targets: list of target integers
    :return: counts
    '''
    # Generate Circuit
    grovers = grovers_circuit(n, targets)

    # Transpile
    backend_target = backend.target
    pm = generate_preset_pass_manager(target=backend_target, optimization_level=3)
    qc_isa = pm.run(grovers)

    if on_hardware:
        # Run Algorithm on Hardware
        sampler = Sampler(mode=backend)
        pubs = [qc_isa]
        job = sampler.run(pubs, shots=num_shots)
        res = job.result()
    else:
        # Run sample on quantum simulator of backend
        backend_sim = AerSimulator.from_backend(backend)
        sampler_sim = BackendSamplerV2(backend=backend_sim)
        job = sampler_sim.run([[qc_isa]], shots=num_shots)
        res = job.result()

    # get data in readable format
    bitstrings = res[0].data.meas.get_counts()
    counts = {int(bitstring, 2): count for bitstring, count in bitstrings.items()}
    plot_histogram(counts)

    return counts


if __name__ == '__main__':
    # Fetch API token and instance CRN. Stored locally in a .env file and not pushed, for obvious reasons.
    load_dotenv()
    API_TOKEN = os.getenv('API_TOKEN')
    CRN = os.getenv('CRN')

    # API_TOKEN = input("Enter your IBM Quantum API Token: ")
    # CRN = input("Enter your IBM Quantum Cloud Instance Number: ")

    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
    from ibmq_connect import ibmq_connect_least_busy

    backend = ibmq_connect_least_busy(API_TOKEN, CRN)

    # integers to search for
    _target_integers: list[int] = []

    repeat = 'y'
    targets = []
    while repeat == 'y':
        a = int(input("What is the target integer?: "))
        _target_integers.append(a)
        repeat = input("Any more targets? (y/n)")

    # find number of qubits required
    _num_qubits = max(_target_integers).bit_length()

    # binary representations of search values in little endian
    _targets: list[str] = [format(num, f'0{_num_qubits}b')[::-1] for num in _target_integers]

    # number of iterations of the algorithm
    _num_its: int = round(np.pi * np.sqrt(2 ** _num_qubits) * 0.25)

    # n-qubit quantum register
    _qr: QuantumRegister = QuantumRegister(_num_qubits, "qubit")

    counts = run_grovers(_num_qubits, _targets, num_shots=1000, on_hardware=False)
    hist = plot_histogram(counts).savefig(f'GroversHistogram{_target_integers}.png')


