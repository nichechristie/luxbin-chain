#!/usr/bin/env python3
"""
Save IBM Quantum token
"""

from qiskit_ibm_runtime import QiskitRuntimeService

token = "nO94Ysggtl2E7eWaHRubOX8kIp8JkKAd2FSm90qyBlTc"

QiskitRuntimeService.save_account(
    channel="ibm_quantum_platform",
    token=token,
    overwrite=True
)

print("IBM Quantum token saved.")