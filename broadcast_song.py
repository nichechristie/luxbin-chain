#!/usr/bin/env python3
"""
Broadcast the translated song in Luxbin light language to IBM quantum computers
"""

import sys
sys.path.append('luxbin-light-language')
sys.path.append('luxbin-quantum-internet')

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
import numpy as np
from translate_song import main as get_translation

def encode_wavelengths_to_quantum(wavelengths):
    """
    Encode light wavelengths into quantum states
    """
    n_qubits = int(np.ceil(np.log2(len(wavelengths))))
    qc = QuantumCircuit(n_qubits)

    # Normalize wavelengths to angles (0 to 2pi)
    min_wl, max_wl = 400, 700
    angles = [(wl - min_wl) / (max_wl - min_wl) * 2 * np.pi for wl in wavelengths]

    # Encode as RY rotations
    for i, angle in enumerate(angles[:n_qubits]):
        qc.ry(angle, i)

    # Add measurements
    qc.measure_all()

    return qc

def broadcast_to_ibm(qc, backend_name='ibm_fez'):
    """
    Send the quantum circuit to IBM quantum computer
    """
    try:
        service = QiskitRuntimeService()
        backend = service.backend(backend_name)

        # Transpile the circuit
        transpiled_qc = transpile(qc, backend)

        # Use Sampler primitive
        sampler = Sampler(backend)

        print(f"Broadcasting to {backend_name}...")

        # Run the job
        job = sampler.run([transpiled_qc], shots=1024)

        print(f"Job ID: {job.job_id()}")

        # Wait for result
        result = job.result()
        counts = result[0].data
        print(f"Measurement results: {counts}")

        return job.job_id()

    except Exception as e:
        print(f"Error broadcasting: {e}")
        print("Running in simulation mode...")
        # Fallback to simulator
        from qiskit_aer import AerSimulator
        simulator = AerSimulator()
        sampler = Sampler(simulator)
        job = sampler.run([qc], shots=1024)
        result = job.result()
        counts = result[0].data
        print(f"Simulation results: {counts}")
        return "simulation"

def main():
    # Get the translated song data
    luxbin_chars, colors, wavelengths = get_translation()

    print(f"Translating song with {len(wavelengths)} wavelengths...")

    # Encode wavelengths into quantum circuit
    qc = encode_wavelengths_to_quantum(wavelengths)

    print(f"Created quantum circuit with {qc.num_qubits} qubits")

    # Broadcast to multiple IBM backends
    backends = ['ibm_fez', 'ibm_torino', 'ibm_marrakesh']

    for backend in backends:
        print(f"\nBroadcasting to {backend}...")
        job_id = broadcast_to_ibm(qc, backend)
        print(f"Job submitted: {job_id}")

if __name__ == "__main__":
    main()