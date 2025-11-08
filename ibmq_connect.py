#%%
from qiskit_ibm_runtime import QiskitRuntimeService, IBMBackend

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