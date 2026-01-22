#!/usr/bin/env python3
"""
Run Shor's Algorithm on the Quantum Network
"""

import sys
import os
sys.path.append('.')
sys.path.append('quantum-internet')

from deploy_ai_agents_security import AIAgentDeployment

def main():
    # Initialize the quantum network
    network = AIAgentDeployment()

    # Apply Shor's Algorithm with default number 15
    result = network.apply_shors_algorithm_to_network(number_to_factor=15)

    print("\n" + "="*60)
    print("FINAL RESULTS:")
    print(f"Number factored: {result['target_number']}")
    if result['factors_found']:
        print(f"Factors: {' × '.join(map(str, result['factors_found']))}")
    else:
        print("No factors found")
    print("="*60)

if __name__ == "__main__":
    main()