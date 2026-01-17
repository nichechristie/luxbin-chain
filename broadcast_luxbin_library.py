#!/usr/bin/env python3
"""
Broadcast the entire Luxbin library to IBM quantum computers
"""

import os
import sys
sys.path.append('luxbin-light-language')
sys.path.append('luxbin-quantum-internet')

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
import numpy as np

def encode_data_to_quantum(data_bytes):
    """
    Encode binary data into quantum circuit
    """
    n_qubits = min(int(np.ceil(np.log2(len(data_bytes) * 8))), 10)  # Limit to 10 qubits for practicality
    qc = QuantumCircuit(n_qubits)

    # Simple encoding: use data as angles for RY gates
    angles = []
    for byte in data_bytes[:2**n_qubits]:  # Limit data size
        angles.append((byte / 255) * 2 * np.pi)

    for i, angle in enumerate(angles):
        qubit = i % n_qubits
        qc.ry(angle, qubit)

    qc.measure_all()
    return qc

def broadcast_file_to_ibm(file_path, backend_name='ibm_fez'):
    """
    Read file and broadcast its content as quantum states
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        print(f"Encoding {file_path} ({len(data)} bytes)...")

        qc = encode_data_to_quantum(data)

        service = QiskitRuntimeService()
        backend = service.backend(backend_name)
        transpiled_qc = transpile(qc, backend)
        sampler = Sampler(backend)

        job = sampler.run([transpiled_qc], shots=1024)
        print(f"Broadcast {file_path} to {backend_name}, Job ID: {job.job_id()}")

        return job.job_id()

    except Exception as e:
        print(f"Error broadcasting {file_path}: {e}")
        return None

def main():
    # Key Luxbin library files
    luxbin_files = [
        'luxbin-light-language/README.md',
        'luxbin-light-language/luxbin_light_converter.py',
        'luxbin-light-language/luxbin_code_translator.py',
        'luxbin-light-language/luxbin_morse_light.py',
        'luxbin-quantum-internet/README.md',
        'luxbin-quantum-internet/quantum_wifi_simple.py',
        'luxbin-chain/README.md',
        'luxbin-chain/luxbin-paper.tex',
        'luxbin-chain/luxbin_autonomous_deployer.py'
    ]

    backends = ['ibm_fez', 'ibm_torino', 'ibm_marrakesh']

    for backend in backends:
        print(f"\nBroadcasting to {backend}...")
        for file_path in luxbin_files:
            if os.path.exists(file_path):
                broadcast_file_to_ibm(file_path, backend)
            else:
                print(f"File not found: {file_path}")

if __name__ == "__main__":
    main()