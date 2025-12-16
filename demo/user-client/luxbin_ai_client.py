#!/usr/bin/env python3
"""
LUXBIN AI Compute - User Client

This client demonstrates how users interact with the LUXBIN AI Compute network:
1. Generate temporal cryptographic keys
2. Submit AI compute requests to blockchain
3. Retrieve verified results

Author: Nichole Christie
Date: December 15, 2025
"""

import hashlib
import time
from datetime import datetime
from typing import Optional, Dict, Any

# LUXBIN alphabet for photonic encoding
LUXBIN_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "


class LUXBINTemporalKey:
    """Generates temporal cryptographic keys for AI compute access"""

    @staticmethod
    def timestamp_to_binary(timestamp: int) -> bytes:
        """Convert Unix timestamp to binary representation (HH:MM:SS)"""
        hours = (timestamp // 3600) % 24
        minutes = (timestamp // 60) % 60
        seconds = timestamp % 60

        binary = ""
        binary += format(hours, '05b')    # 5 bits for hours (0-23)
        binary += format(minutes, '06b')  # 6 bits for minutes (0-59)
        binary += format(seconds, '06b')  # 6 bits for seconds (0-59)

        return binary.encode('utf-8')

    @staticmethod
    def luxbin_encode(text: str) -> Dict[str, Any]:
        """Encode text using LUXBIN photonic encoding"""
        text = text.upper()

        # Validate characters
        for char in text:
            if char not in LUXBIN_ALPHABET:
                raise ValueError(f"Invalid character '{char}' not in LUXBIN alphabet")

        # Calculate HSL color
        total_pos = sum(LUXBIN_ALPHABET.index(char) for char in text)
        avg_pos = total_pos // len(text)
        alphabet_len = len(LUXBIN_ALPHABET)

        hue = (avg_pos * 360) // alphabet_len
        saturation = 100
        lightness = 70

        # Generate binary representation
        binary = ""
        for char in text:
            pos = LUXBIN_ALPHABET.index(char)
            binary += format(pos, '06b')  # 6 bits per character

        return {
            "text": text,
            "color": {"hue": hue, "saturation": saturation, "lightness": lightness},
            "binary": binary.encode('utf-8')
        }

    @staticmethod
    def generate_temporal_key(timestamp: int, phrase: str) -> str:
        """
        Generate temporal cryptographic key

        Process:
        1. Convert timestamp to binary
        2. Encode phrase using LUXBIN
        3. Combine time_binary + photonic_binary
        4. Hash with SHA3-512

        Returns:
            512-bit temporal key as hex string
        """
        # Step 1: Time to binary
        time_binary = LUXBINTemporalKey.timestamp_to_binary(timestamp)

        # Step 2: Phrase to LUXBIN photonic
        photonic = LUXBINTemporalKey.luxbin_encode(phrase)

        # Step 3: Combine binaries
        combined = time_binary + photonic["binary"]

        # Step 4: Hash with SHA3-512
        hasher = hashlib.sha3_512()
        hasher.update(combined)
        temporal_key = hasher.hexdigest()

        return temporal_key


class LUXBINAIClient:
    """Client for interacting with LUXBIN AI Compute network"""

    def __init__(self, account_id: str, phrase: str):
        """
        Initialize LUXBIN AI client

        Args:
            account_id: User's blockchain account ID
            phrase: Secret phrase for temporal key generation
        """
        self.account_id = account_id
        self.phrase = phrase
        self.requests = {}

    def generate_temporal_key(self) -> str:
        """Generate temporal key for current timestamp"""
        timestamp = int(time.time())
        return LUXBINTemporalKey.generate_temporal_key(timestamp, self.phrase)

    def hash_prompt(self, prompt: str) -> str:
        """Hash AI prompt for on-chain storage"""
        hasher = hashlib.blake2b(digest_size=32)
        hasher.update(prompt.encode('utf-8'))
        return hasher.hexdigest()

    def submit_ai_request(
        self,
        prompt: str,
        model: str = "GPT4",
        max_tokens: int = 10000,
        payment: int = 1000
    ) -> Dict[str, Any]:
        """
        Submit AI compute request to blockchain

        Args:
            prompt: The AI prompt/question
            model: AI model to use (GPT4, ClaudeOpus, etc.)
            max_tokens: Maximum tokens for response
            payment: Amount in LUXBIN tokens

        Returns:
            Request details including temporal key and request hash
        """
        # Generate temporal key
        temporal_key = self.generate_temporal_key()

        # Hash the prompt
        request_hash = self.hash_prompt(prompt)

        # Create request
        request = {
            "requester": self.account_id,
            "temporal_key": temporal_key,
            "request_hash": request_hash,
            "prompt": prompt,  # Not stored on-chain
            "model": model,
            "max_tokens": max_tokens,
            "payment": payment,
            "timestamp": int(time.time()),
            "status": "pending"
        }

        # Store locally (in real implementation, submit to blockchain)
        request_id = len(self.requests)
        self.requests[request_id] = request

        print(f"\n✅ AI Compute Request Submitted")
        print(f"   Request ID: {request_id}")
        print(f"   Model: {model}")
        print(f"   Temporal Key: {temporal_key[:16]}...")
        print(f"   Request Hash: {request_hash[:16]}...")
        print(f"   Payment: {payment} LUXBIN tokens")
        print(f"   Prompt: \"{prompt}\"")

        return request

    def verify_result(
        self,
        request_id: int,
        output: str,
        output_hash: str,
        output_hmac: str
    ) -> bool:
        """
        Verify AI compute result using HMAC

        Args:
            request_id: ID of the request
            output: The AI output
            output_hash: Hash of the output
            output_hmac: HMAC signature

        Returns:
            True if verification passes
        """
        if request_id not in self.requests:
            print(f"❌ Request {request_id} not found")
            return False

        request = self.requests[request_id]
        temporal_key = request["temporal_key"]

        # Verify output hash
        hasher = hashlib.blake2b(digest_size=32)
        hasher.update(output.encode('utf-8'))
        computed_hash = hasher.hexdigest()

        if computed_hash != output_hash:
            print(f"❌ Output hash mismatch")
            return False

        # Verify HMAC
        combined = bytes.fromhex(output_hash) + bytes.fromhex(temporal_key)
        hasher = hashlib.sha3_512()
        hasher.update(combined)
        computed_hmac = hasher.hexdigest()

        if computed_hmac != output_hmac:
            print(f"❌ HMAC verification failed")
            return False

        print(f"\n✅ Result Verified!")
        print(f"   Request ID: {request_id}")
        print(f"   Output Hash: {output_hash[:16]}...")
        print(f"   HMAC: {output_hmac[:16]}...")
        print(f"   Output: \"{output}\"")

        return True


def demo_user_flow():
    """Demonstrate complete user flow"""
    print("=" * 60)
    print("LUXBIN AI COMPUTE - USER CLIENT DEMO")
    print("=" * 60)

    # Initialize client
    client = LUXBINAIClient(
        account_id="alice",
        phrase="AI COMPUTE REQUEST"
    )

    print("\n📱 User: Alice")
    print(f"   Phrase: \"{client.phrase}\"")

    # Submit AI request
    print("\n" + "-" * 60)
    print("Step 1: Submit AI Compute Request")
    print("-" * 60)

    request = client.submit_ai_request(
        prompt="Explain quantum computing in simple terms",
        model="GPT4",
        max_tokens=10000,
        payment=1000
    )

    # Simulate waiting for result
    print("\n⏳ Waiting for AI node to process...")
    time.sleep(1)

    # Simulate receiving result (in real implementation, comes from blockchain)
    print("\n" + "-" * 60)
    print("Step 2: Receive and Verify Result")
    print("-" * 60)

    # Mock AI output
    output = "Quantum computing uses quantum bits (qubits) that can be 0, 1, or both simultaneously..."

    # Hash output
    hasher = hashlib.blake2b(digest_size=32)
    hasher.update(output.encode('utf-8'))
    output_hash = hasher.hexdigest()

    # Generate HMAC (as AI node would)
    combined = bytes.fromhex(output_hash) + bytes.fromhex(request["temporal_key"])
    hasher = hashlib.sha3_512()
    hasher.update(combined)
    output_hmac = hasher.hexdigest()

    # Verify result
    verified = client.verify_result(
        request_id=0,
        output=output,
        output_hash=output_hash,
        output_hmac=output_hmac
    )

    if verified:
        print("\n✅ Payment released to AI node")
        print("✅ Transaction complete!")

    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    demo_user_flow()
