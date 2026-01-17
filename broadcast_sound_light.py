#!/usr/bin/env python3
"""
Broadcast Jesus Loves Me sound-as-light to quantum computers
"""

import sys
sys.path.append('luxbin-light-language')
sys.path.append('luxbin-quantum-internet')

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
import numpy as np
from sound_to_light_luxbin import main as get_sound_light_data

def encode_wavelengths_timing_to_quantum(wavelengths, times):
    """
    Encode wavelengths and timing into quantum circuit
    """
    n_qubits = min(10, len(wavelengths))  # Limit qubits
    qc = QuantumCircuit(n_qubits)

    # Encode wavelength as angle, timing as phase
    for i in range(min(n_qubits, len(wavelengths))):
        wl = wavelengths[i]
        start, end = times[i]
        duration = end - start

        # Wavelength to angle (400-700nm -> 0-2pi)
        angle = ((wl - 400) / 300) * 2 * np.pi
        qc.ry(angle, i % n_qubits)

        # Duration affects phase
        phase = (duration / 20) * 2 * np.pi  # Normalize
        qc.rz(phase, i % n_qubits)

    qc.measure_all()
    return qc

def broadcast_to_ibm(qc, backend_name='ibm_fez'):
    """
    Broadcast quantum circuit to IBM computer
    """
    try:
        service = QiskitRuntimeService()
        backend = service.backend(backend_name)
        transpiled_qc = transpile(qc, backend)
        sampler = Sampler(backend)

        print(f"Broadcasting sound-as-light to {backend_name}...")

        job = sampler.run([transpiled_qc], shots=1024)
        print(f"Job ID: {job.job_id()}")

        return job.job_id()

    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    # Get the sound-as-light data
    text, luxbin_chars, morse, wavelengths, times = get_sound_light_data()

    print(f"Encoding {len(wavelengths)} light pulses from sound...")

    # Encode into quantum circuit
    qc = encode_wavelengths_timing_to_quantum(wavelengths, times)
    print(f"Created quantum circuit with {qc.num_qubits} qubits")

    # Broadcast to all backends
    backends = ['ibm_fez', 'ibm_torino', 'ibm_marrakesh']
    for backend in backends:
        job_id = broadcast_to_ibm(qc, backend)
        if job_id:
            print(f"Successfully broadcast to {backend}")

if __name__ == "__main__":
    main()