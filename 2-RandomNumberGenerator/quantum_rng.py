import numpy as np
import os
from dotenv import load_dotenv
from qiskit import *
from qiskit_aer import *
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler
import math

def ibmq_connect_least_busy(token, instance):
    '''
    Function to connect to least busy IMB Quantum service.
    :param - token: IBM Quantum token
    :param - instance: IBM Quantum instance
    '''

    # Connect to my runtime service.
    service = QiskitRuntimeService(token=token,instance=instance)

    if not service: raise 'Service failed to connect'

    backend = service.least_busy()

    print(
            f"Name: {backend.name}\n"
            f"Version: {backend.version}\n"
            f"No. of qubits: {backend.num_qubits}\n"
    )

    return backend

def generate_nbit_circuit(n, measure = True):
    '''
    Function to generate a rng circuit with n qubits.
    :param n: number of qubits.
    :param measure: whether to measure or not. Default to True for Sampling.
    :return qr: quantum register
    :return cr: classical register
    :return qc: quantum circuit
    '''
    qr = QuantumRegister(n)
    cr = ClassicalRegister(n)
    qc = QuantumCircuit(qr, cr)
    qc.h(qr) # hadamard gate at each qubit
    if measure: qc.measure_all()
    return qr, cr, qc

def fast_dice_roller(min_inclusive, max_exclusive, bitstream, num_ints):
    '''
    Generate random integer in range given a stream of unbiased bits
    :param min_inclusive: minimal range value
    :param max_exclusive: maximal range value, exclusive
    :param bitstream: stream of randomly generated bits
    :param num_ints: number of integers to generate
    :return integers: list of randomly generated integers
    '''
    integers = []

    max_inclusive = max_exclusive - min_inclusive - 1

    for _ in range(num_ints):
        x = 1
        y = 0

        while True:
            x = x * 2

            # Ensure bitstream still has bits
            if not bitstream:
                raise ValueError("Bitstream ran out of bits!")

            random_bit = bitstream.pop()
            y = (y * 2) + random_bit

            if x > max_inclusive:
                if y <= max_inclusive:
                    integers.append(y + min_inclusive)
                    break
                # Reject and continue using remainder
                x = x - max_inclusive - 1
                y = y - max_inclusive - 1

    return integers

def generate_bitstring(n, num_shots):
    '''
    Generate bitstring of length n using IBM quantum service.
    :param n: number of bits (or qubits)
    :param num_shots: number of shots to generate
    :return bitstring: bitstring of length n
    '''
    # Create circuit
    qr, cr, qc = generate_nbit_circuit(n)

    # Transpile
    target = backend.target
    if n > backend.num_qubits: raise 'Not enough qubits to generate that large a number'
    pm = generate_preset_pass_manager(target=target, optimization_level=3)
    qc_isa = pm.run(qc)

    # Run sample on hardware
    sampler = Sampler(mode=backend)
    pubs = [qc_isa]
    job = sampler.run(pubs, shots=num_shots)
    res = job.result()

    # return bitstring
    bitstrings = res[0].data.meas.get_counts()
    result = []
    for key, count in bitstrings.items():
        result.extend([key] * count)
    bitstream = [int(bit) for bit in ''.join(result)]
    return bitstream

def quantum_random_int(min_val, max_val, num_its=1):
    '''
    Generate random number in range
    :param min_val: minimal range value
    :param max_val: maximal range value, not inclusive
    :param num_its: number of random numbers to generate
    :return:
    '''
    diff = 0
    if min_val < 0:
        diff = min_val
        min_val -= diff
        max_val -= diff

    if not min_val < max_val: raise 'Maximum value must be bigger than minimum value'
    if (not isinstance(min_val, int)) or (not isinstance(max_val, int)) or (not isinstance(num_its, int)): ' Must be integers'

    n = math.ceil(np.log2(max_val-min_val)+2) # estimate how many qubits we will need for one number generation
    total_bits = n * num_its # how many bits we will need in the bitstream in total
    available_qubits = backend.num_qubits
    num_shots = math.ceil(total_bits/available_qubits) # how many times we need to sample from the register
    num_qubits = int(total_bits / num_shots) # more efficient use of the quantum register

    bitstream = generate_bitstring(num_qubits, num_shots) # run quantum circuit to get list of bits
    random_integers = fast_dice_roller(min_val, max_val+1, bitstream, num_its) # run algorithm
    return np.array(random_integers) + diff

if __name__ == "__main__":
    # Fetch API token and instance CRN. Stored locally in a .env file and not pushed, for obvious reasons.
    load_dotenv()
    API_TOKEN = os.getenv('API_TOKEN')
    CRN = os.getenv('CRN')

    # API_TOKEN = input("Enter your IBM Quantum API Token: ")
    # CRN = input("Enter your IBM Quantum Cloud Instance Number: ")

    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
    from ibmq_connect import ibmq_connect_least_busy
    backend = ibmq_connect_least_busy(API_TOKEN, CRN)

    repeat = 'y'
    while repeat == 'y':
        a = int(input("What is your minimum range?: "))
        b = int(input("What is your maximum range?: "))
        m = int(input("How many numbers would you like to generate?: "))
        print('Loading...')
        print(quantum_random_int(a, b, m))
        repeat = input("Would you like to generate more random numbers? (y/n): ")
