#!/usr/bin/env python3
"""
LUXBIN Chain - Incentivized Testnet Rewards Program

Earn real LUX tokens by testing on LUXBIN testnet!

Programs:
1. Testnet Activity Points → Mainnet LUX Airdrop
2. Bug Bounty Program (pay USDC/ETH for finding bugs)
3. Developer Quests (build on testnet, earn LUX on mainnet)
4. Early Tester NFT (proof of participation + bonus rewards)
"""

import json
from datetime import datetime
from typing import Dict, List, Optional


class LUXBINTestnetRewards:
    """
    Incentivized testnet program for LUXBIN Chain

    Features:
    - Track testnet activity points
    - Calculate mainnet LUX airdrop amounts
    - Manage bug bounties
    - Issue early tester NFTs
    - Run developer quests
    """

    def __init__(self):
        # Airdrop pool
        self.total_airdrop_pool = 10_000_000  # 10M LUX reserved for testnet users
        self.points_to_lux_rate = 1.0  # 1 point = 1 LUX

        # Activity multipliers
        self.activity_points = {
            'wallet_creation': 10,
            'transaction': 1,
            'contract_deployment': 50,
            'contract_interaction': 5,
            'bridge_test': 25,
            'quantum_wallet_test': 100,
            'daily_active': 5,
            'weekly_streak': 50,
            'referral': 100,
            'bug_report': 500,
            'critical_bug': 5000
        }

        # Bug bounty rewards (paid in real USDC/ETH)
        self.bug_bounties = {
            'critical': 10000,  # $10k USDC
            'high': 2500,       # $2.5k USDC
            'medium': 500,      # $500 USDC
            'low': 100,         # $100 USDC
            'informational': 50 # $50 USDC
        }

        # Developer quest rewards
        self.quest_rewards = {
            'deploy_first_contract': 500,
            'create_nft_collection': 1000,
            'build_dex': 5000,
            'integrate_quantum_wallet': 2000,
            'cross_chain_bridge': 3000,
            'complete_tutorial_series': 200
        }

        # User tracking
        self.users = {}
        self.leaderboard = []

    def register_user(self, wallet_address: str) -> Dict:
        """Register new testnet user"""

        if wallet_address in self.users:
            return self.users[wallet_address]

        user = {
            'wallet_address': wallet_address,
            'points': 0,
            'activities': [],
            'quests_completed': [],
            'bugs_reported': [],
            'referrals': [],
            'early_tester_nft': None,
            'estimated_airdrop': 0,
            'joined_date': datetime.now().isoformat()
        }

        # Award registration bonus
        user['points'] += self.activity_points['wallet_creation']
        user['activities'].append({
            'type': 'wallet_creation',
            'points': self.activity_points['wallet_creation'],
            'timestamp': datetime.now().isoformat()
        })

        self.users[wallet_address] = user

        print(f"✅ User registered: {wallet_address}")
        print(f"   Bonus: {self.activity_points['wallet_creation']} points")

        return user

    def track_activity(self, wallet_address: str, activity_type: str,
                      metadata: Optional[Dict] = None) -> Dict:
        """Track user activity and award points"""

        if wallet_address not in self.users:
            self.register_user(wallet_address)

        user = self.users[wallet_address]
        points = self.activity_points.get(activity_type, 0)

        # Award points
        user['points'] += points

        # Record activity
        activity = {
            'type': activity_type,
            'points': points,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        user['activities'].append(activity)

        # Update estimated airdrop
        user['estimated_airdrop'] = user['points'] * self.points_to_lux_rate

        print(f"🎯 Activity tracked: {activity_type}")
        print(f"   User: {wallet_address[:10]}...")
        print(f"   Points earned: +{points}")
        print(f"   Total points: {user['points']}")
        print(f"   Estimated airdrop: {user['estimated_airdrop']} LUX")

        return user

    def complete_quest(self, wallet_address: str, quest_name: str) -> Dict:
        """Complete developer quest and earn bonus LUX"""

        if wallet_address not in self.users:
            self.register_user(wallet_address)

        user = self.users[wallet_address]

        # Check if already completed
        if quest_name in user['quests_completed']:
            return {
                'status': 'already_completed',
                'message': f"Quest '{quest_name}' already completed"
            }

        # Award quest points
        points = self.quest_rewards.get(quest_name, 0)
        if points == 0:
            return {
                'status': 'invalid_quest',
                'message': f"Quest '{quest_name}' not found"
            }

        user['points'] += points
        user['quests_completed'].append(quest_name)
        user['estimated_airdrop'] = user['points'] * self.points_to_lux_rate

        print(f"🏆 QUEST COMPLETED: {quest_name}")
        print(f"   User: {wallet_address[:10]}...")
        print(f"   Reward: {points} points")
        print(f"   Total points: {user['points']}")
        print(f"   Estimated airdrop: {user['estimated_airdrop']} LUX")

        return {
            'status': 'completed',
            'quest': quest_name,
            'points_earned': points,
            'total_points': user['points']
        }

    def report_bug(self, wallet_address: str, severity: str,
                   description: str, proof: str) -> Dict:
        """
        Report bug and earn bug bounty

        Severity levels:
        - critical: $10k USDC (smart contract exploit, fund loss risk)
        - high: $2.5k USDC (security issue, no immediate fund risk)
        - medium: $500 USDC (functionality bug, workaround exists)
        - low: $100 USDC (minor issue, cosmetic)
        - informational: $50 USDC (suggestion, optimization)
        """

        if wallet_address not in self.users:
            self.register_user(wallet_address)

        user = self.users[wallet_address]

        # Get bounty amount
        bounty_usd = self.bug_bounties.get(severity, 0)
        if bounty_usd == 0:
            return {
                'status': 'invalid_severity',
                'message': f"Severity '{severity}' not recognized"
            }

        # Award points based on severity
        points_map = {
            'critical': self.activity_points['critical_bug'],
            'high': 2500,
            'medium': 1000,
            'low': 250,
            'informational': 50
        }
        points = points_map.get(severity, 0)

        bug_report = {
            'severity': severity,
            'description': description,
            'proof': proof,
            'bounty_usd': bounty_usd,
            'points': points,
            'status': 'pending_review',
            'reported_at': datetime.now().isoformat()
        }

        user['bugs_reported'].append(bug_report)
        user['points'] += points
        user['estimated_airdrop'] = user['points'] * self.points_to_lux_rate

        print(f"🐛 BUG REPORT SUBMITTED")
        print(f"   Reporter: {wallet_address[:10]}...")
        print(f"   Severity: {severity.upper()}")
        print(f"   Bounty: ${bounty_usd:,} USDC")
        print(f"   Bonus points: {points}")
        print(f"   Status: Pending review")
        print()
        print(f"💡 If approved:")
        print(f"   - ${bounty_usd:,} USDC sent to your wallet")
        print(f"   - {points} points added")
        print(f"   - Listed on security hall of fame")

        return {
            'status': 'submitted',
            'bug_report': bug_report,
            'bounty_amount': f"${bounty_usd:,} USDC",
            'points_if_approved': points
        }

    def issue_early_tester_nft(self, wallet_address: str) -> Dict:
        """Issue Early Tester NFT (proof of participation + bonus)"""

        if wallet_address not in self.users:
            return {
                'status': 'not_registered',
                'message': 'User not registered'
            }

        user = self.users[wallet_address]

        if user['early_tester_nft']:
            return {
                'status': 'already_issued',
                'message': 'NFT already issued to this wallet'
            }

        # Award NFT and bonus
        bonus_points = 500
        nft_id = f"LUXBIN-EARLY-TESTER-{len(self.users)}"

        user['early_tester_nft'] = {
            'nft_id': nft_id,
            'issued_at': datetime.now().isoformat(),
            'bonus_points': bonus_points,
            'perks': [
                '2x points multiplier on all future activities',
                'Exclusive Discord role',
                'Priority access to mainnet launch',
                'Bonus 10% on final airdrop',
                'Permanent recognition on LUXBIN Hall of Fame'
            ]
        }

        user['points'] += bonus_points
        user['estimated_airdrop'] = user['points'] * self.points_to_lux_rate * 1.1  # 10% bonus

        print(f"🎨 EARLY TESTER NFT ISSUED!")
        print(f"   Recipient: {wallet_address[:10]}...")
        print(f"   NFT ID: {nft_id}")
        print(f"   Bonus: {bonus_points} points")
        print(f"   Perks: 2x multiplier + 10% airdrop bonus")

        return {
            'status': 'issued',
            'nft': user['early_tester_nft']
        }

    def calculate_final_airdrop(self, snapshot_date: Optional[str] = None) -> Dict:
        """Calculate final airdrop amounts for all users"""

        print(f"\n{'='*80}")
        print(f"📸 MAINNET AIRDROP SNAPSHOT")
        print(f"{'='*80}")
        print(f"Date: {snapshot_date or datetime.now().isoformat()}")
        print(f"Total pool: {self.total_airdrop_pool:,} LUX")
        print(f"Registered users: {len(self.users)}")
        print()

        # Calculate total points
        total_points = sum(user['points'] for user in self.users.values())

        airdrop_results = {
            'snapshot_date': snapshot_date or datetime.now().isoformat(),
            'total_pool': self.total_airdrop_pool,
            'total_users': len(self.users),
            'total_points': total_points,
            'allocations': []
        }

        # Calculate each user's share
        for wallet, user in self.users.items():
            # Base allocation
            points = user['points']
            share = points / total_points if total_points > 0 else 0
            base_airdrop = share * self.total_airdrop_pool

            # Apply early tester bonus
            multiplier = 1.1 if user['early_tester_nft'] else 1.0
            final_airdrop = base_airdrop * multiplier

            allocation = {
                'wallet_address': wallet,
                'points': points,
                'share_percentage': share * 100,
                'base_airdrop': base_airdrop,
                'early_tester_bonus': user['early_tester_nft'] is not None,
                'multiplier': multiplier,
                'final_airdrop': final_airdrop,
                'activities_count': len(user['activities']),
                'quests_completed': len(user['quests_completed']),
                'bugs_reported': len(user['bugs_reported'])
            }

            airdrop_results['allocations'].append(allocation)

        # Sort by final airdrop amount
        airdrop_results['allocations'].sort(key=lambda x: x['final_airdrop'], reverse=True)

        # Print top 10
        print("🏆 TOP 10 TESTERS:")
        print("-" * 80)
        for i, alloc in enumerate(airdrop_results['allocations'][:10], 1):
            print(f"{i}. {alloc['wallet_address'][:10]}... - {alloc['final_airdrop']:,.0f} LUX")
            print(f"   Points: {alloc['points']:,} | Quests: {alloc['quests_completed']} | Bugs: {alloc['bugs_reported']}")

        return airdrop_results

    def get_leaderboard(self, limit: int = 20) -> List[Dict]:
        """Get testnet leaderboard"""

        leaderboard = []

        for wallet, user in self.users.items():
            leaderboard.append({
                'rank': 0,  # Will be set after sorting
                'wallet_address': wallet,
                'points': user['points'],
                'estimated_airdrop': user['estimated_airdrop'],
                'activities': len(user['activities']),
                'quests': len(user['quests_completed']),
                'bugs': len(user['bugs_reported']),
                'early_tester': user['early_tester_nft'] is not None
            })

        # Sort by points
        leaderboard.sort(key=lambda x: x['points'], reverse=True)

        # Assign ranks
        for i, entry in enumerate(leaderboard, 1):
            entry['rank'] = i

        return leaderboard[:limit]

    def get_user_stats(self, wallet_address: str) -> Dict:
        """Get detailed user statistics"""

        if wallet_address not in self.users:
            return {
                'status': 'not_found',
                'message': 'User not registered'
            }

        user = self.users[wallet_address]
        leaderboard = self.get_leaderboard(limit=len(self.users))
        rank = next((i+1 for i, u in enumerate(leaderboard) if u['wallet_address'] == wallet_address), None)

        return {
            'wallet_address': wallet_address,
            'rank': rank,
            'total_users': len(self.users),
            'points': user['points'],
            'estimated_airdrop': user['estimated_airdrop'],
            'activities_count': len(user['activities']),
            'quests_completed': user['quests_completed'],
            'bugs_reported': len(user['bugs_reported']),
            'referrals': len(user['referrals']),
            'early_tester_nft': user['early_tester_nft'],
            'joined_date': user['joined_date']
        }


def demo_testnet_rewards():
    """Demo the testnet rewards system"""

    print("=" * 80)
    print("🚀 LUXBIN CHAIN - INCENTIVIZED TESTNET PROGRAM")
    print("=" * 80)
    print()

    rewards = LUXBINTestnetRewards()

    # Simulate user activity
    print("📝 SCENARIO: Active Testnet User Journey")
    print("=" * 80)
    print()

    user_wallet = "0xTestUser123456789abcdef"

    # 1. Register
    print("STEP 1: Register on testnet")
    print("-" * 40)
    rewards.register_user(user_wallet)
    print()

    input("Press Enter to continue...\n")

    # 2. Deploy contract
    print("STEP 2: Deploy first smart contract")
    print("-" * 40)
    rewards.track_activity(user_wallet, 'contract_deployment', {
        'contract': 'MyFirstToken',
        'address': '0xContract123...'
    })
    print()

    input("Press Enter to continue...\n")

    # 3. Test quantum wallet
    print("STEP 3: Test quantum wallet security")
    print("-" * 40)
    rewards.track_activity(user_wallet, 'quantum_wallet_test', {
        'multisig_created': True
    })
    print()

    input("Press Enter to continue...\n")

    # 4. Complete quest
    print("STEP 4: Complete developer quest")
    print("-" * 40)
    rewards.complete_quest(user_wallet, 'deploy_first_contract')
    print()

    input("Press Enter to continue...\n")

    # 5. Report bug
    print("STEP 5: Report a bug")
    print("-" * 40)
    rewards.report_bug(
        user_wallet,
        'medium',
        'Gas estimation incorrect for cross-chain transfers',
        'Screenshot + reproduction steps attached'
    )
    print()

    input("Press Enter to continue...\n")

    # 6. Issue NFT
    print("STEP 6: Receive Early Tester NFT")
    print("-" * 40)
    rewards.issue_early_tester_nft(user_wallet)
    print()

    input("Press Enter to continue...\n")

    # 7. Show stats
    print("STEP 7: View your stats")
    print("-" * 40)
    stats = rewards.get_user_stats(user_wallet)
    print(f"Rank: #{stats['rank']}/{stats['total_users']}")
    print(f"Total Points: {stats['points']}")
    print(f"Estimated Mainnet Airdrop: {stats['estimated_airdrop']} LUX")
    print(f"Activities: {stats['activities_count']}")
    print(f"Quests: {len(stats['quests_completed'])}")
    print(f"Bugs: {stats['bugs_reported']}")
    print(f"Early Tester: {'✅ Yes' if stats['early_tester_nft'] else '❌ No'}")
    print()

    print("=" * 80)
    print("💡 WAYS TO EARN MORE POINTS")
    print("=" * 80)
    print()
    print("Daily Activities:")
    print("  • Make transactions: 1 point each")
    print("  • Deploy contracts: 50 points each")
    print("  • Test quantum wallet: 100 points")
    print("  • Daily login: 5 points")
    print()
    print("Developer Quests:")
    print("  • Build a DEX: 5,000 points")
    print("  • Create NFT collection: 1,000 points")
    print("  • Integrate quantum wallet: 2,000 points")
    print()
    print("Bug Bounties:")
    print("  • Critical bug: $10k USDC + 5,000 points")
    print("  • High severity: $2.5k USDC + 2,500 points")
    print("  • Medium: $500 USDC + 1,000 points")
    print()
    print("Bonuses:")
    print("  • Refer a friend: 100 points")
    print("  • Weekly streak: 50 points")
    print("  • Early Tester NFT: 2x multiplier + 10% airdrop bonus")
    print()


if __name__ == "__main__":
    demo_testnet_rewards()
