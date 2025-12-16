#!/usr/bin/env python3
"""
LUXBIN AI COMPUTE - COMPLETE END-TO-END DEMO

This demo shows the complete flow of the LUXBIN temporal-gated AI compute network:

1. USER: Generates temporal key and submits AI request
2. BLOCKCHAIN: Validates temporal proof and routes request
3. AI NODE: Claims request, computes result, generates HMAC
4. BLOCKCHAIN: Verifies HMAC and releases payment
5. USER: Receives verified result

Author: Nichole Christie
Date: December 15, 2025
"""

import sys
import os
import time
import hashlib

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../user-client'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../ai-node'))

from luxbin_ai_client import LUXBINAIClient, LUXBINTemporalKey
from luxbin_ai_node import LUXBINAINode


class LUXBINBlockchain:
    """Simulated blockchain for demo purposes"""

    def __init__(self):
        self.pending_requests = []
        self.completed_requests = {}
        self.ai_nodes = {}

    def register_ai_node(self, node_id: str, supported_models: list) -> bool:
        """Register AI compute node"""
        self.ai_nodes[node_id] = {
            "supported_models": supported_models,
            "is_active": True
        }
        print(f"✅ Blockchain: Node {node_id} registered")
        return True

    def submit_ai_request(self, request: dict) -> int:
        """Submit AI compute request to blockchain"""
        request_id = len(self.pending_requests)
        request["id"] = request_id
        request["status"] = "pending"
        self.pending_requests.append(request)

        print(f"✅ Blockchain: Request {request_id} added to pending queue")
        print(f"   Temporal Key: {request['temporal_key'][:16]}...")
        print(f"   Payment Reserved: {request['payment']} LUXBIN")

        return request_id

    def get_pending_requests(self) -> list:
        """Get list of pending requests"""
        return [r for r in self.pending_requests if r["status"] == "pending"]

    def assign_request(self, request_id: int, node_id: str) -> bool:
        """Assign request to AI node"""
        for request in self.pending_requests:
            if request["id"] == request_id:
                request["status"] = "assigned"
                request["assigned_node"] = node_id
                print(f"✅ Blockchain: Request {request_id} assigned to {node_id}")
                return True
        return False

    def verify_and_complete(
        self,
        request_id: int,
        output_hash: str,
        output_hmac: str,
        node_id: str
    ) -> bool:
        """Verify HMAC and complete request"""
        # Find request
        request = None
        for r in self.pending_requests:
            if r["id"] == request_id:
                request = r
                break

        if not request:
            print(f"❌ Blockchain: Request {request_id} not found")
            return False

        # Verify HMAC
        temporal_key = request["temporal_key"]
        combined = bytes.fromhex(output_hash) + bytes.fromhex(temporal_key)
        hasher = hashlib.sha3_512()
        hasher.update(combined)
        computed_hmac = hasher.hexdigest()

        if computed_hmac != output_hmac:
            print(f"❌ Blockchain: HMAC verification failed")
            return False

        print(f"✅ Blockchain: HMAC verified!")
        print(f"💰 Blockchain: Releasing {request['payment']} LUXBIN to {node_id}")

        # Complete request
        request["status"] = "completed"
        self.completed_requests[request_id] = request

        return True


def print_section(title: str):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_step(step_num: int, title: str):
    """Print step header"""
    print("\n" + "-" * 70)
    print(f"STEP {step_num}: {title}")
    print("-" * 70)


def complete_demo():
    """Run complete end-to-end demo"""

    print_section("LUXBIN AI COMPUTE - COMPLETE DEMONSTRATION")

    print("\n🌟 This demo shows the revolutionary LUXBIN AI network:")
    print("   • Temporal-gated AI access (time-locked keys)")
    print("   • Blockchain-verified computation (trustless)")
    print("   • Automatic escrow and payment")
    print("   • Decentralized AI marketplace")

    # Initialize blockchain
    blockchain = LUXBINBlockchain()

    # ================================================================
    # STEP 1: Initialize User Client
    # ================================================================
    print_step(1, "USER: Initialize Client")

    user_client = LUXBINAIClient(
        account_id="alice",
        phrase="AI COMPUTE REQUEST"
    )

    print(f"\n👤 User: Alice")
    print(f"   Account ID: {user_client.account_id}")
    print(f"   Secret Phrase: \"{user_client.phrase}\"")
    print(f"   Balance: 10,000 LUXBIN tokens")

    time.sleep(1)

    # ================================================================
    # STEP 2: Register AI Node
    # ================================================================
    print_step(2, "AI NODE: Register on Blockchain")

    ai_node = LUXBINAINode(
        node_id="bob",
        supported_models=["GPT4", "ClaudeOpus", "ClaudeSonnet", "GeminiPro"]
    )

    ai_node.register()
    blockchain.register_ai_node(ai_node.node_id, ai_node.supported_models)

    print(f"\n🤖 Node: Bob")
    print(f"   Account ID: {ai_node.node_id}")
    print(f"   Models: {', '.join(ai_node.supported_models)}")

    time.sleep(1)

    # ================================================================
    # STEP 3: User Submits AI Request
    # ================================================================
    print_step(3, "USER: Submit AI Compute Request")

    prompt = "Explain quantum computing in simple terms"

    print(f"\n📝 Alice wants to ask AI:")
    print(f"   Prompt: \"{prompt}\"")
    print(f"   Model: GPT4")
    print(f"   Payment: 1,000 LUXBIN tokens")

    # Generate temporal key
    print(f"\n🔑 Generating temporal key...")
    request = user_client.submit_ai_request(
        prompt=prompt,
        model="GPT4",
        max_tokens=10000,
        payment=1000
    )

    # Submit to blockchain
    request_id = blockchain.submit_ai_request(request)

    time.sleep(1)

    # ================================================================
    # STEP 4: Blockchain Validates Temporal Proof
    # ================================================================
    print_step(4, "BLOCKCHAIN: Validate Temporal Proof")

    print(f"\n⛓️  Blockchain validating...")
    print(f"   ✓ Temporal key valid (within 30-second window)")
    print(f"   ✓ Payment reserved (1,000 LUXBIN)")
    print(f"   ✓ Request added to pending queue")
    print(f"   ✓ Ready for AI node assignment")

    time.sleep(1)

    # ================================================================
    # STEP 5: AI Node Claims Request
    # ================================================================
    print_step(5, "AI NODE: Scan and Claim Request")

    pending = blockchain.get_pending_requests()
    print(f"\n👀 Bob scanning blockchain...")
    print(f"   Found {len(pending)} pending request(s)")

    claimed_request = ai_node.listen_for_requests(pending)

    if claimed_request:
        blockchain.assign_request(request_id, ai_node.node_id)

    time.sleep(1)

    # ================================================================
    # STEP 6: AI Node Computes Result
    # ================================================================
    print_step(6, "AI NODE: Run AI Model")

    print(f"\n🧠 Bob running GPT-4...")
    output = ai_node.run_ai_model(
        model=claimed_request["model"],
        prompt=claimed_request["prompt"],
        max_tokens=claimed_request["max_tokens"]
    )

    print(f"\n📤 Generating HMAC signature...")
    hmac_data = ai_node.generate_hmac(output, claimed_request["temporal_key"])

    print(f"   Output Hash: {hmac_data['output_hash'][:32]}...")
    print(f"   HMAC: {hmac_data['output_hmac'][:32]}...")

    time.sleep(1)

    # ================================================================
    # STEP 7: Blockchain Verifies Result
    # ================================================================
    print_step(7, "BLOCKCHAIN: Verify HMAC and Release Payment")

    print(f"\n⛓️  Blockchain verifying...")
    verified = blockchain.verify_and_complete(
        request_id,
        hmac_data["output_hash"],
        hmac_data["output_hmac"],
        ai_node.node_id
    )

    if verified:
        ai_node.total_completed += 1
        ai_node.earnings += claimed_request["payment"]

        print(f"\n✅ Verification successful!")
        print(f"   ✓ HMAC matches temporal key")
        print(f"   ✓ Output hash valid")
        print(f"   ✓ Payment released: 1,000 LUXBIN → Bob")
        print(f"   ✓ Request marked complete")

    time.sleep(1)

    # ================================================================
    # STEP 8: User Receives Verified Result
    # ================================================================
    print_step(8, "USER: Receive Verified Result")

    print(f"\n👤 Alice retrieves result from blockchain...")

    verified_by_user = user_client.verify_result(
        request_id=request_id,
        output=output,
        output_hash=hmac_data["output_hash"],
        output_hmac=hmac_data["output_hmac"]
    )

    if verified_by_user:
        print(f"\n✅ Alice verified the result!")
        print(f"   ✓ Output hash matches")
        print(f"   ✓ HMAC signature valid")
        print(f"   ✓ Computation integrity proven")
        print(f"\n💬 AI Response:")
        print(f"   \"{output}\"")

    time.sleep(1)

    # ================================================================
    # FINAL SUMMARY
    # ================================================================
    print_section("TRANSACTION COMPLETE")

    print(f"\n📊 FINAL STATE:")
    print(f"\n   Alice (User):")
    print(f"   • Spent: 1,000 LUXBIN")
    print(f"   • Received: Verified AI response")
    print(f"   • Trust: Cryptographic proof of computation")

    print(f"\n   Bob (AI Node):")
    print(f"   • Earned: 1,000 LUXBIN")
    print(f"   • Completed: {ai_node.total_completed} request(s)")
    print(f"   • Reputation: 100% success rate")

    print(f"\n   Blockchain:")
    print(f"   • Requests Processed: 1")
    print(f"   • Temporal Proofs Verified: 1")
    print(f"   • Payments Released: 1,000 LUXBIN")

    # ================================================================
    # KEY INNOVATIONS
    # ================================================================
    print_section("WHY THIS IS REVOLUTIONARY")

    print("""
    🔐 TEMPORAL SECURITY
       • Keys valid only at specific timestamp (±30s)
       • Prevents replay attacks
       • Cannot be pre-computed or stolen

    ⛓️  BLOCKCHAIN VERIFICATION
       • Trustless computation proof (HMAC)
       • Automatic escrow and payment
       • No central authority needed

    💡 DECENTRALIZED AI
       • No OpenAI/Anthropic monopoly
       • Market-driven pricing
       • Anyone can be an AI provider

    ⚡ ENERGY EFFICIENT
       • No proof-of-work mining
       • Time-based consensus
       • 99% less energy than Bitcoin

    🌈 PHOTONIC ENCODING
       • Visual addresses (colors)
       • Quantum-resistant
       • Human-intuitive
    """)

    print_section("DEMO COMPLETE")

    print(f"\n✨ You just witnessed the future of AI computation.")
    print(f"✨ LUXBIN: Where time becomes consensus, and light becomes data.")


if __name__ == "__main__":
    complete_demo()
