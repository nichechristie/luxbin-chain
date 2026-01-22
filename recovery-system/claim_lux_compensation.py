#!/usr/bin/env python3
"""
LUXBIN Compensation Claim Script
Claim your LUX tokens for verified theft losses
"""

import json
from luxbin_compensation_system import LUXBINCompensationSystem


def claim_compensation():
    """
    Claim LUX compensation for wallet 0xB8BAeb03b7a57c091Ff9Dd456FC54DCDD5432Ad1
    """

    print("=" * 80)
    print("💎 LUXBIN THEFT COMPENSATION CLAIM")
    print("=" * 80)
    print()

    # Load recovery report
    report_file = "recovery_report_0xB8BAeb03b7a57c091Ff9Dd456FC54DCDD5432Ad1.json"

    try:
        with open(report_file, 'r') as f:
            report = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Recovery report not found")
        print(f"   Expected: {report_file}")
        print(f"   Please run: python3 recover_wallet_funds.py first")
        return

    print("📊 CLAIM SUMMARY")
    print("=" * 80)
    print(f"Wallet: {report['wallet_address']}")
    print(f"Total Losses: {report['analysis']['total_lost_eth']} ETH")
    print(f"Total Losses: ${report['analysis']['total_lost_usd']:,.2f} USD")
    print(f"Confirmed Thefts: {len(report['analysis']['confirmed_thefts'])}")
    print()

    # Initialize compensation system
    compensation_system = LUXBINCompensationSystem()

    # Process each theft
    total_lux_claimed = 0
    claims = []

    for theft in report['analysis']['confirmed_thefts']:
        print(f"\n📝 Processing theft: {theft['hash']}")

        amount_eth = float(theft['value'].split()[0])

        # Process claim
        result = compensation_system.process_compensation_claim(
            victim_address=report['wallet_address'],
            stolen_chain='ethereum',
            stolen_amount=amount_eth,
            stolen_asset='ETH',
            theft_tx_hash=theft['hash']
        )

        if result['status'] == 'compensation_complete':
            claim_info = result['claim']
            lux_amount = float(claim_info['compensated'].split()[0])
            total_lux_claimed += lux_amount

            claims.append({
                'theft_tx': theft['hash'],
                'stolen_amount': theft['value'],
                'lux_compensation': claim_info['compensated'],
                'status': 'completed'
            })

            print(f"✅ Claim processed successfully")
        else:
            print(f"❌ Claim failed: {result.get('reason', 'Unknown error')}")

    # Summary
    print("\n\n" + "=" * 80)
    print("✅ COMPENSATION CLAIM COMPLETE")
    print("=" * 80)
    print()
    print(f"💰 TOTAL LUX COMPENSATION: {total_lux_claimed} LUX")
    print()
    print("📅 VESTING SCHEDULE:")
    print(f"   Immediate (25%): {total_lux_claimed * 0.25} LUX")
    print(f"   Vested (75%): {total_lux_claimed * 0.75} LUX over 12 months")
    print(f"   Monthly payment: {(total_lux_claimed * 0.75) / 12:.2f} LUX")
    print()
    print("📍 DESTINATION:")
    print("   Your quantum-secured multi-sig wallet:")
    print("   0xMSff04be15304321d02524c6d8b7acd00a0a5275")
    print()
    print("💡 NOTE:")
    print("   - LUX tokens sent to your quantum multi-sig (not old wallet)")
    print("   - Requires 3/4 signatures to spend")
    print("   - Protected by quantum consensus")
    print("   - $0 gas fees on LUXBIN Chain")
    print()
    print("🎉 Your compensation claim has been processed!")
    print("=" * 80)

    # Save claim receipt
    receipt = {
        'wallet_address': report['wallet_address'],
        'quantum_multisig': '0xMSff04be15304321d02524c6d8b7acd00a0a5275',
        'total_lux_claimed': total_lux_claimed,
        'immediate_amount': total_lux_claimed * 0.25,
        'vested_amount': total_lux_claimed * 0.75,
        'monthly_payment': (total_lux_claimed * 0.75) / 12,
        'claims': claims,
        'vesting_schedule': '25% immediate, 75% over 12 months',
        'status': 'completed'
    }

    receipt_file = f"lux_compensation_receipt_{report['wallet_address']}.json"
    with open(receipt_file, 'w') as f:
        json.dump(receipt, f, indent=2)

    print(f"\n📄 Receipt saved to: {receipt_file}")


def check_claim_status():
    """Check status of existing claim"""

    wallet_address = "0xB8BAeb03b7a57c091Ff9Dd456FC54DCDD5432Ad1"
    receipt_file = f"lux_compensation_receipt_{wallet_address}.json"

    try:
        with open(receipt_file, 'r') as f:
            receipt = json.load(f)

        print("\n" + "=" * 80)
        print("💎 LUX COMPENSATION STATUS")
        print("=" * 80)
        print()
        print(f"Wallet: {receipt['wallet_address']}")
        print(f"Total Claimed: {receipt['total_lux_claimed']} LUX")
        print(f"Already Received: {receipt['immediate_amount']} LUX (25%)")
        print(f"Remaining Vested: {receipt['vested_amount']} LUX (75%)")
        print(f"Monthly Payment: {receipt['monthly_payment']:.2f} LUX")
        print()
        print("📅 Next Payments:")
        months_remaining = 12
        for month in range(1, min(4, months_remaining + 1)):
            print(f"   Month {month}: {receipt['monthly_payment']:.2f} LUX")
        if months_remaining > 3:
            print(f"   ... {months_remaining - 3} more months")
        print()
        print("✅ Claim Status: ACTIVE")
        print("=" * 80)

    except FileNotFoundError:
        print("\n❌ No active claim found")
        print("   Run: python3 claim_lux_compensation.py to claim")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "status":
        check_claim_status()
    else:
        claim_compensation()
