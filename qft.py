import numpy as np
from qiskit import QuantumCircuit

def qft_rotate(circuit: QuantumCircuit, i: int, _n: int, barriers:bool=True):
    """
    Apply the QFT subroutine to qubit i.

    Parameters
    ----------
    circuit : QuantumCircuit, required. The circuit to modify.
    i : int, required. Index of the qubit being transformed.
    _n : int, required. Total number of qubits.
    barriers : bool, optional. If True, insert visual barriers.

    Returns
    -------
    QuantumCircuit. The modified circuit.
    """
    if barriers:
        circuit.barrier()

    # Apply Hadamard to start the QFT on qubit i
    circuit.h(i)

    # Final qubit receives no controlled rotations
    if i == _n - 1:
        return circuit

    # Controlled phase rotations with decreasing powers
    for j in range(1, _n - i):
        theta = 2 * np.pi / (2 ** (j + 1))
        circuit.cp(theta, i + j, i)

    return circuit


def qft_circuit(circuit: QuantumCircuit, _n: int, barriers:bool=True):
    """
    Apply the full Quantum Fourier Transform (QFT).

    Parameters
    ----------
    circuit : QuantumCircuit, required. The circuit to modify.
    _n : int, required. Total number of qubits.
    barriers : bool, optional. If True, insert visual barriers.

    Returns
    -------
    QuantumCircuit. The modified circuit.
    """
    for i in range(_n):
        qft_rotate(circuit, i, _n, barriers)

    return circuit


def swap_registers(circuit: QuantumCircuit, _n: int, barriers:bool=True):
    """
    Reverse the order of qubits to correct endian layout.

    Parameters
    ----------
    circuit : QuantumCircuit, required. The circuit to modify.
    _n : int, required. Number of qubits.
    barriers : bool, optional. If True, insert visual barriers.

    Returns
    -------
    QuantumCircuit. The circuit with swapped qubits.
    """
    if barriers:
        circuit.barrier()

    for qubit in range(_n // 2):
        circuit.swap(qubit, _n - qubit - 1)

    return circuit


def iqft_rotate(circuit: QuantumCircuit, i: int, _n: int, barriers:bool=True):
    """
    Apply the inverse QFT subroutine to qubit i.

    Parameters
    ----------
    circuit : QuantumCircuit, required. The circuit to modify.
    i : int, required. Index of the qubit being transformed.
    _n : int, required. Total number of qubits.
    barriers : bool, optional. If True, insert visual barriers.

    Returns
    -------
    QuantumCircuit. The modified circuit.
    """
    if barriers:
        circuit.barrier()

    # Controlled-phase gates, reversed order, negative angle
    for j in reversed(range(1, _n - i)):
        theta = -2 * np.pi / (2 ** (j + 1))
        circuit.cp(theta, i + j, i)

    # Hadamard is its own inverse
    circuit.h(i)

    return circuit


def iqft_circuit(circuit: QuantumCircuit, _n: int, barriers:bool=True):
    """
    Apply the full inverse Quantum Fourier Transform (IQFT).

    Parameters
    ----------
    circuit : QuantumCircuit, required . The circuit to modify.
    _n : int, required . Number of qubits.
    barriers : bool, optional . If True, insert visual barriers.

    Returns
    -------
    QuantumCircuit
        The circuit with IQFT applied.
    """
    for i in reversed(range(_n)):
        iqft_rotate(circuit, i, _n, barriers)

    return circuit


def qft(circuit: QuantumCircuit, _n: int, inverse:bool=False, swap_endian:bool=False, barriers:bool=False):
    """
    Apply the Quantum Fourier Transform or its inverse.

    Parameters
    ----------
    circuit : QuantumCircuit, required. The circuit to modify.
    _n : int, required. Number of qubits.
    inverse : bool, optional. If True, apply the inverse QFT instead of the forward QFT.
    swap_endian : bool, optional. If True, swap qubits to correct endian order.
    barriers : bool, optional. If True, insert visual barriers.

    Returns
    -------
    QuantumCircuit
        The modified circuit.
    """
    if inverse:
        circuit = iqft_circuit(circuit, _n, barriers)
    else:
        circuit = qft_circuit(circuit, _n, barriers)

    if swap_endian:
        circuit = swap_registers(circuit, _n, barriers)

    return circuit
