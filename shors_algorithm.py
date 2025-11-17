import os
import sys
import numpy as np
import math
from fractions import Fraction
from dotenv import load_dotenv
from qiskit import *
from qiskit.visualization import plot_histogram
from qiskit_aer import *
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import (SamplerV2 as Sampler)
from qiskit.primitives import (BackendSamplerV2)
from requests.packages import target
import random
from qiskit.circuit.library import UnitaryGate
from qft import *

def shors_circuit(a, N, num_qubits, num_counting_qubits):
    """
    Builds a quantum circuit for the quantum part of Shor's algorithm.

    Parameters
    ----------
    a : int
        An integer coprime to N, for which we want to find the period of a^x mod N.
    N : int
        The integer to be factorized.
    num_qubits : int
        Number of qubits in the target register (used to store |1> initially).
    num_counting_qubits : int
        Number of qubits in the counting register (used to estimate the period).

    Returns
    -------
    QuantumCircuit
        A Qiskit QuantumCircuit object for Shor's algorithm.
    """

    # ------ Build Register ------
    qr_counting = QuantumRegister(num_counting_qubits, 'count_qubit') # register for counting
    qr_target = QuantumRegister(num_qubits, 'qubit') # register for target state
    cr = ClassicalRegister(num_counting_qubits, 'cr') # classical register for measuring counting qubits
    qc = QuantumCircuit(qr_counting, qr_target, cr)

    # set counting register into superposition
    qc.h(range(num_counting_qubits))

    # set target register to |1>
    qc.x(num_counting_qubits)

    qc.barrier()


    # ------ Build unitary matrix. ------
    dim = 2**num_qubits
    U = np.zeros((dim, dim), dtype=complex)

    # U acts as |x> -> |a*x mod N> for 0 <= x < 2^n.
    for x in range(dim):
        if x < N:
            u = (a * x) % N
        else:
            # for states outside [0,N-1],leave them unchanged
            u = x
        U[u, x] = 1.0


    # ------ Apply all Unitary Gates to each counting qubit ------
    for j in range(num_counting_qubits):
        # set power, so that we have U^0, U^1, U^2, U^4,... applied to each counting qubit.
        power = 2**j

        U_power = np.linalg.matrix_power(U, power) # calculate U^x
        U_gate = UnitaryGate(U_power, label=f"U^{power}") # build Unitary Gate from U^x
        controlled_U_gate = U_gate.control()  # controlled on 1 qubit

        # add gate to circuit: counting qubit j acts as the control qubit, while the gate acts on the target qubits
        qc.append(controlled_U_gate, [j] + [num_counting_qubits + i for i in range(num_qubits)])

    qc.barrier()


    # ------ Apply inverse QFT on counting register ------
    inv_qft = QuantumCircuit(qr_counting, name='iqft')
    inv_qft = qft(inv_qft, num_counting_qubits, inverse=True, swap_endian=True)
    qc.append(inv_qft, list(range(num_counting_qubits)))
    qc.barrier()


    # ------ Measure Counting Qubits -------
    for i in range(num_counting_qubits):
        qc.measure(i, i)

    return qc

def find_r(_x, m):
    """ Find period by continued fractions """
    frac = Fraction(_x, 2**m).limit_denominator() # find the simplest fraction closest to C/2^m
    r = frac.denominator
    return r

def get_period(counts, a, N, num_counting_qubits):
    """ Get period from set of phase estimations """

    # -- convert measurements to integers __
    vals = []
    for bitstring, _ in counts.items():
        x = int(bitstring, 2)
        if x != 0: vals.append(x)

    # -- get candidate periods --
    r_candidates = [find_r(_x, num_counting_qubits) for _x in vals]

    # -- generate periods and check against algorithm constraints. --
    r_vals = [r for r in r_candidates if (pow(a, r, N) == 1) and (r%2 == 0) and (pow(a, int(r/2), N) != 1)]
    period = min(r_vals)

    print("Raw x values:", vals)
    print("Candidate r:", r_candidates)
    print("Valid r:", r_vals)
    print("Period:", period)

    return period

def get_factors(a, r, N):
    """ Get factors from a, r and N """
    f1 = math.gcd(pow(a, r//2, N) + 1, N)
    f2 = math.gcd(pow(a, r//2, N) - 1, N)
    return f1, f2

import random

def run_shors(N, num_shots: int = 1000, on_hardware: bool = False, a_list: list[int] = []):
    """
    Run Shor's algorithm to factor an integer N.

    Parameters
    ----------
    N : int. Integer to factor.
    num_shots : int, optional. Measurement shots per circuit execution. Default is 1000.
    on_hardware : bool, optional. If True, run on a quantum device; otherwise use a simulator.
    a_list : list[int], optional. Candidate bases ``a``. If empty, defaults to ``range(2, N)``.

    Returns
    -------
    f1 : int. First factor of N.
    f2 : int. Second factor of N.
    counts : dict. Measurement counts from the successful order-finding run. Empty if N is prime.
    """

    if not a_list: a_list = list(range(2, N)) # generate list of candidate values for a if non supplied
    num_qubits: int = N.bit_length() # (n) number of qubits to represent N
    num_counting_qubits: int = 2*num_qubits   # counting register. Used to store phase information encoding r.

    while True:
        # run out of candidate a's, break from loop
        if len(a_list) == 0: break

        # get random candidate a from list
        a = a_list.pop(random.randint(0, len(a_list) - 1))
        print('Trying a := ', a)

        # check if a coprime to N. If not, try new a.
        if math.gcd(a, N) == 1:

            # Generate Circuit
            circuit = shors_circuit(a, N, num_qubits, num_counting_qubits)

            # Transpile
            backend_target = backend.target
            pm = generate_preset_pass_manager(target=backend_target, optimization_level=3)
            qc_isa = pm.run(circuit)

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

            # # get data in readable format
            counts = res[0].data.cr.get_counts()

            # get period
            period = get_period(counts, a, N, num_counting_qubits)

            if pow(a, period//2, N) != -1:
                print('a: ', a)
                f1, f2 = get_factors(a, period, N)
                print('Factors:', f1, f2)
                return f1, f2, counts

        else: print(f'{a} not coprime to {N}')

    print('N has no coprime integers, therefore N is prime')
    return N, 1, {}