#!/usr/bin/env python3
"""
LUXBIN AI Compute - AI Node

This AI node demonstrates how compute providers participate in the LUXBIN AI network:
1. Register as an AI compute node
2. Listen for pending AI requests
3. Compute results using AI models
4. Submit HMAC-verified results to blockchain

Author: Nichole Christie
Date: December 15, 2025
"""

import hashlib
import time
from typing import Dict, List, Any, Optional


class LUXBINAINode:
    """AI compute node that processes requests and earns LUXBIN tokens"""

    def __init__(self, node_id: str, supported_models: List[str]):
        """
        Initialize AI compute node

        Args:
            node_id: Node's blockchain account ID
            supported_models: List of AI models this node can run
        """
        self.node_id = node_id
        self.supported_models = supported_models
        self.is_registered = False
        self.total_completed = 0
        self.total_failed = 0
        self.earnings = 0

    def register(self) -> bool:
        """Register node on blockchain"""
        print(f"\n🤖 Registering AI Node: {self.node_id}")
        print(f"   Supported Models: {', '.join(self.supported_models)}")

        # In real implementation, this would call blockchain extrinsic
        self.is_registered = True

        print(f"✅ Node registered successfully!")
        return True

    def listen_for_requests(self, pending_requests: List[Dict]) -> Optional[Dict]:
        """
        Check pending requests and claim one if compatible

        Args:
            pending_requests: List of pending AI compute requests

        Returns:
            Claimed request or None
        """
        if not self.is_registered:
            print("❌ Node not registered")
            return None

        print(f"\n👀 Scanning {len(pending_requests)} pending requests...")

        for request in pending_requests:
            if request["model"] in self.supported_models:
                print(f"\n✅ Found compatible request!")
                print(f"   Request ID: {request.get('id', 'N/A')}")
                print(f"   Model: {request['model']}")
                print(f"   Payment: {request['payment']} LUXBIN")
                return request

        print("   No compatible requests found")
        return None

    def run_ai_model(self, model: str, prompt: str, max_tokens: int) -> str:
        """
        Run AI model to generate output

        Args:
            model: AI model to use
            prompt: User's prompt
            max_tokens: Maximum tokens

        Returns:
            AI output text
        """
        print(f"\n🧠 Running {model}...")
        print(f"   Prompt: \"{prompt}\"")
        print(f"   Max Tokens: {max_tokens}")

        # Simulate AI processing
        time.sleep(1)

        # Mock responses (in real implementation, call actual AI APIs)
        responses = {
            "GPT4": "Quantum computing uses quantum bits (qubits) that can be 0, 1, or both simultaneously (superposition). This allows quantum computers to process certain calculations exponentially faster than classical computers.",

            "ClaudeOpus": "Quantum computing is based on quantum mechanics principles. Unlike classical bits that are either 0 or 1, qubits can exist in superposition - being both 0 and 1 at once. This enables quantum computers to solve specific problems much faster.",

            "ClaudeSonnet": "Quantum computers work differently than regular computers. They use qubits which can be in multiple states at once, allowing them to try many solutions simultaneously.",

            "GeminiPro": "Quantum computing leverages quantum mechanical phenomena like superposition and entanglement to perform computations that would be impractical for classical computers.",

            "LocalLLM": "Quantum computing uses quantum physics to do calculations. Qubits can be 0 and 1 at the same time, making quantum computers very fast for certain tasks."
        }

        output = responses.get(model, f"Response from {model}: {prompt}")

        print(f"✅ AI computation complete!")
        print(f"   Output: \"{output[:80]}...\"")

        return output

    def generate_hmac(self, output: str, temporal_key: str) -> Dict[str, str]:
        """
        Generate HMAC signature for AI output

        Args:
            output: AI output text
            temporal_key: Temporal key from request

        Returns:
            Dict with output_hash and output_hmac
        """
        # Hash the output
        hasher = hashlib.blake2b(digest_size=32)
        hasher.update(output.encode('utf-8'))
        output_hash = hasher.hexdigest()

        # Generate HMAC using temporal key
        combined = bytes.fromhex(output_hash) + bytes.fromhex(temporal_key)
        hasher = hashlib.sha3_512()
        hasher.update(combined)
        output_hmac = hasher.hexdigest()

        return {
            "output_hash": output_hash,
            "output_hmac": output_hmac
        }

    def submit_result(
        self,
        request_id: int,
        output: str,
        temporal_key: str,
        payment: int
    ) -> bool:
        """
        Submit verified result to blockchain

        Args:
            request_id: ID of the request
            output: AI output
            temporal_key: Temporal key from request
            payment: Payment amount

        Returns:
            True if submission successful
        """
        print(f"\n📤 Submitting result to blockchain...")

        # Generate HMAC
        hmac_data = self.generate_hmac(output, temporal_key)

        print(f"   Request ID: {request_id}")
        print(f"   Output Hash: {hmac_data['output_hash'][:16]}...")
        print(f"   HMAC: {hmac_data['output_hmac'][:16]}...")

        # In real implementation, submit to blockchain
        # blockchain.submit_ai_compute_result(request_id, output_hash, output_hmac)

        # Simulate blockchain verification
        time.sleep(0.5)

        print(f"\n✅ Result verified by blockchain!")
        print(f"💰 Payment received: {payment} LUXBIN tokens")

        # Update stats
        self.total_completed += 1
        self.earnings += payment

        return True

    def process_request(self, request: Dict) -> bool:
        """
        Complete flow: claim → compute → submit result

        Args:
            request: AI compute request

        Returns:
            True if processing successful
        """
        print("\n" + "=" * 60)
        print(f"PROCESSING REQUEST")
        print("=" * 60)

        # Extract request details
        request_id = request.get("id", 0)
        model = request["model"]
        prompt = request.get("prompt", "")
        max_tokens = request.get("max_tokens", 10000)
        temporal_key = request["temporal_key"]
        payment = request["payment"]

        # Run AI model
        output = self.run_ai_model(model, prompt, max_tokens)

        # Submit result
        success = self.submit_result(request_id, output, temporal_key, payment)

        if success:
            print(f"\n✅ Request {request_id} completed successfully!")
        else:
            print(f"\n❌ Request {request_id} failed")
            self.total_failed += 1

        return success

    def get_stats(self) -> Dict[str, Any]:
        """Get node statistics"""
        return {
            "node_id": self.node_id,
            "is_registered": self.is_registered,
            "supported_models": self.supported_models,
            "total_completed": self.total_completed,
            "total_failed": self.total_failed,
            "earnings": self.earnings,
            "success_rate": (
                self.total_completed / (self.total_completed + self.total_failed) * 100
                if (self.total_completed + self.total_failed) > 0
                else 0
            )
        }


def demo_ai_node():
    """Demonstrate AI node operation"""
    print("=" * 60)
    print("LUXBIN AI COMPUTE - AI NODE DEMO")
    print("=" * 60)

    # Create AI node
    node = LUXBINAINode(
        node_id="bob",
        supported_models=["GPT4", "ClaudeOpus", "ClaudeSonnet"]
    )

    # Register node
    node.register()

    # Simulate pending requests from blockchain
    pending_requests = [
        {
            "id": 0,
            "requester": "alice",
            "model": "GPT4",
            "prompt": "Explain quantum computing in simple terms",
            "max_tokens": 10000,
            "payment": 1000,
            "temporal_key": "abc123def456...",  # Simplified for demo
        },
        {
            "id": 1,
            "requester": "charlie",
            "model": "LocalLLM",  # Not supported by this node
            "prompt": "What is blockchain?",
            "max_tokens": 5000,
            "payment": 500,
            "temporal_key": "xyz789...",
        },
        {
            "id": 2,
            "requester": "dave",
            "model": "ClaudeOpus",
            "prompt": "Explain machine learning",
            "max_tokens": 8000,
            "payment": 800,
            "temporal_key": "pqr456...",
        }
    ]

    # Listen and claim compatible request
    request = node.listen_for_requests(pending_requests)

    if request:
        # Process the request
        node.process_request(request)

    # Display node stats
    print("\n" + "=" * 60)
    print("NODE STATISTICS")
    print("=" * 60)
    stats = node.get_stats()
    print(f"Node ID: {stats['node_id']}")
    print(f"Models: {', '.join(stats['supported_models'])}")
    print(f"Total Completed: {stats['total_completed']}")
    print(f"Total Failed: {stats['total_failed']}")
    print(f"Success Rate: {stats['success_rate']:.1f}%")
    print(f"Total Earnings: {stats['earnings']} LUXBIN tokens")

    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    demo_ai_node()
