#!/usr/bin/env python3
"""
Broadcast video-as-light to quantum computers
"""

import sys
sys.path.append('luxbin-light-language')
sys.path.append('luxbin-quantum-internet')

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
import numpy as np
from video_to_luxbin import main as get_video_data

def encode_wavelengths_to_quantum(wavelengths):
    """Encode wavelengths into quantum circuit"""
    n_qubits = min(10, len(wavelengths))
    qc = QuantumCircuit(n_qubits)

    for i in range(n_qubits):
        wl = wavelengths[i]
        angle = ((wl - 400) / 300) * 2 * np.pi
        qc.ry(angle, i)

    qc.measure_all()
    return qc

def broadcast_to_ibm(qc, backend_name='ibm_fez'):
    """Broadcast to IBM quantum computer"""
    try:
        service = QiskitRuntimeService()
        backend = service.backend(backend_name)
        transpiled_qc = transpile(qc, backend)
        sampler = Sampler(backend)

        print(f"Broadcasting video-as-light to {backend_name}...")

        job = sampler.run([transpiled_qc], shots=1024)
        print(f"Job ID: {job.job_id()}")

        return job.job_id()

    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    # Get video data
    video_frames, binary_data, luxbin_chars, wavelengths = get_video_data()

    print(f"Encoding {len(wavelengths)} light wavelengths from video...")

    # Encode to quantum
    qc = encode_wavelengths_to_quantum(wavelengths)
    print(f"Created quantum circuit with {qc.num_qubits} qubits")

    # Broadcast
    backends = ['ibm_fez', 'ibm_torino', 'ibm_marrakesh']
    for backend in backends:
        job_id = broadcast_to_ibm(qc, backend)
        if job_id:
            print(f"Successfully broadcast video to {backend}")

if __name__ == "__main__":
    main()