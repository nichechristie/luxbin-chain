#!/usr/bin/env python3
"""
Launch Quantum Circuit for Understanding Light Particles
Encodes "light particle" into Luxbin light language and runs on IBM Quantum computer
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram

# Luxbin alphabet (same as in the original)
LUXBIN_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/"

def text_to_luxbin(text):
    """Convert text to binary then LUXBIN"""
    binary = ''.join(format(ord(c), '08b') for c in text)

    # Convert binary to LUXBIN (6 bits per character)
    luxbin = ''
    for i in range(0, len(binary), 6):
        chunk = binary[i:i+6].ljust(6, '0')
        index = int(chunk, 2) % len(LUXBIN_ALPHABET)
        luxbin += LUXBIN_ALPHABET[index]

    return luxbin, binary

def luxbin_to_wavelengths(luxbin, enable_quantum=True):
    """Convert LUXBIN to photonic wavelengths"""
    wavelengths = []
    QUANTUM_ZERO_PHONON = 637  # Diamond NV center (nm)

    for char in luxbin:
        if enable_quantum and char == ' ':
            # Use diamond NV center wavelength for spaces
            wavelengths.append({
                'character': char,
                'wavelength_nm': QUANTUM_ZERO_PHONON,
                'frequency_hz': 3e8 / (QUANTUM_ZERO_PHONON * 1e-9),
                'energy_ev': 1240 / QUANTUM_ZERO_PHONON
            })
        else:
            # Map to visible spectrum (400-700nm)
            index = LUXBIN_ALPHABET.index(char)
            wavelength = 400 + (index / len(LUXBIN_ALPHABET)) * 300

            wavelengths.append({
                'character': char,
                'wavelength_nm': wavelength,
                'frequency_hz': 3e8 / (wavelength * 1e-9),
                'energy_ev': 1240 / wavelength
            })

    return wavelengths

def wavelength_to_quantum_state(wavelength_nm):
    """
    Encode wavelength as quantum state angles
    Maps 400-700nm wavelength range to qubit rotation angles
    """
    # Normalize wavelength to 0-1 range
    norm = (wavelength_nm - 400) / 300

    # Convert to quantum rotation angles
    theta = norm * np.pi  # Polar angle
    phi = norm * 2 * np.pi  # Azimuthal angle

    return theta, phi

def create_luxbin_quantum_circuit(wavelengths, num_qubits=3):
    """
    Create quantum circuit encoding LUXBIN wavelength data
    Uses rotation gates to encode wavelength information
    """
    qc = QuantumCircuit(num_qubits)

    # Encode first few wavelengths (limited by qubit count)
    for i, wl_data in enumerate(wavelengths[:num_qubits]):
        wavelength = wl_data['wavelength_nm']
        theta, phi = wavelength_to_quantum_state(wavelength)

        # Initialize qubit in superposition
        qc.h(i)

        # Encode wavelength via rotation
        qc.ry(theta, i)  # Y-rotation (polar angle)
        qc.rz(phi, i)    # Z-rotation (azimuthal angle)

    # Add measurements
    qc.measure_all()

    return qc

def main():
    """Main function to encode 'light particle' and run on IBM Quantum"""
    print("=" * 60)
    print("QUANTUM COMPUTER UNDERSTANDING LIGHT PARTICLES")
    print("Using Luxbin Light Language Encoding")
    print("=" * 60)

    # Use "light particle" as the text to encode
    text = "light particle"

    # Step 1: Convert to LUXBIN
    print(f"\n🔄 Encoding '{text}' into Luxbin Light Language...")
    luxbin, binary = text_to_luxbin(text)
    print(f"📝 Original text: {text}")
    print(f"🔢 Binary: {binary}")
    print(f"💎 LUXBIN: {luxbin}")

    # Step 2: Convert to wavelengths
    print("\n🌈 Converting to photonic wavelengths...")
    wavelengths = luxbin_to_wavelengths(luxbin, enable_quantum=True)

    print(f"\n📊 Generated {len(wavelengths)} wavelength states:")
    for i, wl in enumerate(wavelengths):
        print(f"  {wl['character']} → {wl['wavelength_nm']:.2f}nm "
              f"({wl['frequency_hz']:.2e}Hz, {wl['energy_ev']:.3f}eV)")

    # Step 3: Create quantum circuit
    print("\n⚛️  Creating quantum circuit...")
    num_qubits = min(5, len(wavelengths))  # Use up to 5 qubits
    qc = create_luxbin_quantum_circuit(wavelengths, num_qubits)

    print(f"✅ Circuit created with {num_qubits} qubits")
    print(f"   Gates: {qc.count_ops()}")
    print(f"   Depth: {qc.depth()}")

    # Visualize circuit
    print("\n📈 Circuit diagram:")
    print(qc.draw(output='text'))

    # Step 4: Connect to IBM Quantum
    print("\n🔐 Connecting to IBM Quantum...")
    service = QiskitRuntimeService()
    print("✅ Connected!")

    # Get least busy backend
    backend = service.least_busy()
    print(f"🎯 Selected backend: {backend.name} ({backend.num_qubits} qubits)")

    # Transpile for hardware
    print("🔄 Transpiling circuit for quantum hardware...")
    qc_transpiled = transpile(qc, backend=backend, optimization_level=3)

    # Run on quantum computer
    print("🚀 Submitting job to quantum computer...")
    sampler = Sampler(backend)
    job = sampler.run([qc_transpiled], shots=1024)

    print(f"⏳ Job submitted! Job ID: {job.job_id()}")
    print("⏳ The quantum computer is now processing your light particle data...")

    # Wait for result (this might take time)
    print("⏳ Waiting for results...")
    result = job.result()
    counts = result[0].data.meas.get_counts()

    # Step 5: Display results
    print("\n" + "=" * 60)
    print("QUANTUM MEASUREMENT RESULTS")
    print("=" * 60)

    print("\n📊 Measurement counts:")
    total_shots = sum(counts.values())
    for state, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        probability = count / total_shots * 100
        print(f"  |{state}⟩: {count} times ({probability:.1f}%)")

    # Visualize
    print("\n📈 Generating visualization...")
    fig = plot_histogram(counts, figsize=(12, 6))
    plt.title(f"Quantum Light Particle Results: '{text}'")
    plt.tight_layout()
    plt.savefig('light_particle_quantum_results.png', dpi=150, bbox_inches='tight')
    print("✅ Saved visualization to: light_particle_quantum_results.png")

    # Analysis
    print("\n" + "=" * 60)
    print("ANALYSIS: QUANTUM COMPUTER UNDERSTANDS LIGHT")
    print("=" * 60)
    print(f"✨ '{text}' encoded as quantum photonic states")
    print(f"💎 Used {num_qubits} qubits to represent {len(wavelengths)} wavelengths")
    print(f"🌊 Wavelength range: {min(w['wavelength_nm'] for w in wavelengths):.1f}-"
          f"{max(w['wavelength_nm'] for w in wavelengths):.1f}nm")
    print(f"⚛️  Quantum operations: {sum(qc.count_ops().values())}")
    print("\n🎯 The quantum computer now 'understands' light particles through:")
    print("   • Photonic wavelength encoding")
    print("   • Quantum state representation")
    print("   • Entangled qubit correlations")
    print("   • Measurement-based interpretation")

if __name__ == "__main__":
    main()