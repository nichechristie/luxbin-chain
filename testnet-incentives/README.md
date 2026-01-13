# LUXBIN Chain - Incentivized Testnet Program

Earn **real LUX tokens** by testing LUXBIN Chain! 🚀

## Overview

The LUXBIN testnet isn't just for testing—it's your opportunity to earn mainnet LUX tokens before launch. We've allocated **10 million LUX** (10% of total supply) for early testers and contributors.

### Why Test on LUXBIN?

- 💰 **Guaranteed Airdrop**: Points → Mainnet LUX tokens
- 🐛 **Bug Bounties**: Up to $10k USDC for finding bugs
- 🏆 **Developer Quests**: Build and earn
- 🎨 **Early Tester NFT**: Exclusive perks + 2x multiplier
- ⚡ **$0 Gas Fees**: Test without spending money

---

## How to Earn

### 1. Testnet Activity Points → Mainnet Airdrop

Every action on testnet earns points. When we launch mainnet, points convert to LUX tokens.

**Points System**:

| Activity | Points |
|----------|--------|
| Create wallet | 10 |
| Make transaction | 1 |
| Deploy contract | 50 |
| Interact with contract | 5 |
| Test bridge | 25 |
| Test quantum wallet | 100 |
| Daily active | 5 |
| Weekly streak (7 days) | 50 |
| Refer a friend | 100 |

**Conversion**: 1 point = 1 LUX token

**Example**:
- Deploy 10 contracts: 500 points
- Test quantum wallet: 100 points
- Daily active for 30 days: 150 points
- **Total**: 750 LUX tokens at mainnet launch

---

### 2. Bug Bounty Program

Find bugs, get paid **real money** (USDC) + bonus points!

| Severity | Bounty | Points | Description |
|----------|--------|--------|-------------|
| **Critical** | $10,000 | 5,000 | Smart contract exploit, fund loss risk |
| **High** | $2,500 | 2,500 | Security issue, no immediate fund risk |
| **Medium** | $500 | 1,000 | Functionality bug, workaround exists |
| **Low** | $100 | 250 | Minor issue, cosmetic |
| **Info** | $50 | 50 | Suggestion, optimization |

**How to report**:
```python
python3 luxbin_testnet_rewards.py report-bug \
  --severity critical \
  --description "Found exploit in bridge contract" \
  --proof "POC-exploit.md"
```

**What qualifies**:
- Smart contract vulnerabilities
- Quantum wallet security issues
- Bridge exploits
- Gas calculation errors
- UI/UX problems

---

### 3. Developer Quests

Build on testnet, earn LUX on mainnet!

| Quest | Reward | Description |
|-------|--------|-------------|
| **Deploy First Contract** | 500 LUX | Deploy any smart contract |
| **Create NFT Collection** | 1,000 LUX | Deploy ERC-721/1155 collection |
| **Build a DEX** | 5,000 LUX | Create functional DEX with liquidity |
| **Integrate Quantum Wallet** | 2,000 LUX | Add quantum security to your dApp |
| **Cross-Chain Bridge** | 3,000 LUX | Bridge assets from Ethereum |
| **Tutorial Series** | 200 LUX | Complete all tutorials |

**How to claim**:
```bash
# After building your DEX
python3 luxbin_testnet_rewards.py complete-quest --quest build_dex
```

---

### 4. Early Tester NFT

Limited edition NFT for early testers with special perks!

**Perks**:
- ✨ **2x points multiplier** on all activities
- 🎯 **10% bonus** on final airdrop
- 👑 Exclusive Discord role
- 🚀 Priority mainnet access
- 🏆 Permanent Hall of Fame recognition

**How to get**:
- Be active on testnet (50+ points)
- Complete at least 1 quest
- Request NFT via Discord or CLI

---

## Getting Started

### 1. Connect to LUXBIN Testnet

**Network Details**:
```
Network Name: LUXBIN Testnet
RPC URL: http://localhost:8545 (or public RPC TBD)
Chain ID: 1337
Currency: tLUX (testnet LUX)
```

**Add to MetaMask**:
```javascript
await window.ethereum.request({
  method: 'wallet_addEthereumChain',
  params: [{
    chainId: '0x539',
    chainName: 'LUXBIN Testnet',
    rpcUrls: ['http://localhost:8545'],
    nativeCurrency: {
      name: 'Test LUX',
      symbol: 'tLUX',
      decimals: 18
    }
  }]
});
```

### 2. Get Test Tokens

**Faucet** (coming soon):
- Visit: https://faucet.luxbin.ai
- Enter wallet address
- Receive 100 tLUX

**Or via CLI**:
```bash
python3 luxbin_testnet_rewards.py register
```

### 3. Start Earning

**Option A: Developer**:
```bash
# Deploy a contract
forge create MyContract --rpc-url http://localhost:8545

# Complete quest
python3 luxbin_testnet_rewards.py complete-quest --quest deploy_first_contract
```

**Option B: Tester**:
```bash
# Test quantum wallet
python3 quantum_wallet_security.py --testnet

# Report bugs
python3 luxbin_testnet_rewards.py report-bug --severity medium
```

**Option C: Builder**:
```bash
# Build a DEX, NFT marketplace, or any dApp
# Complete quests and earn big rewards
```

---

## Tracking Your Progress

### Check Your Stats

```bash
python3 luxbin_testnet_rewards.py stats --wallet 0xYourAddress
```

**Output**:
```
🏆 Your Testnet Stats
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Rank: #42 / 1,523
Points: 2,450
Estimated Airdrop: 2,695 LUX (with 10% NFT bonus)
Activities: 127
Quests: 3
Bugs: 1
Early Tester NFT: ✅ Yes
```

### View Leaderboard

```bash
python3 luxbin_testnet_rewards.py leaderboard
```

---

## Airdrop Details

### When?

Mainnet airdrop occurs when LUXBIN Chain launches (Q2 2026 target).

### How Much?

- **Total Pool**: 10,000,000 LUX (10% of supply)
- **Distribution**: Proportional to points earned
- **Bonuses**: Early Tester NFT holders get 10% extra

### Distribution Schedule

- **25% Immediate**: Available at mainnet launch
- **75% Vested**: Released monthly over 12 months

**Example**:
- You earned: 1,000 LUX
- At launch: 250 LUX (25%)
- Monthly: 62.5 LUX × 12 months

---

## Important Notes

### ⚠️ Scam Warning

**Legitimate**:
- ✅ Testnet activities earn points
- ✅ Points convert to mainnet LUX
- ✅ Bug bounties paid in real USDC/ETH
- ✅ Quests reward mainnet LUX

**SCAMS**:
- ❌ Anyone offering to "swap" testnet tokens for mainnet
- ❌ Sites asking for private keys
- ❌ Fake airdrop sites
- ❌ "Buy testnet points" offers

**Official channels only**:
- Website: https://luxbin.ai
- GitHub: https://github.com/mermaidnicheboutique-code/luxbin-chain
- Discord: (official link only)

### No Guarantees

While we're committed to the airdrop, standard disclaimers apply:
- Participate at your own risk
- Points system may be adjusted
- Anti-sybil measures in place
- Final airdrop subject to KYC/compliance if required

---

## FAQ

**Q: Is testnet LUX worth anything?**
A: No. Testnet tokens are worthless. But your **points** convert to real mainnet LUX.

**Q: Can I sell my testnet points?**
A: No. Points are non-transferable and tied to your wallet.

**Q: How do I maximize my airdrop?**
A:
1. Get Early Tester NFT (2x multiplier + 10% bonus)
2. Complete high-value quests (DEX = 5,000 points)
3. Report bugs (up to 5,000 points + cash bounty)
4. Daily activity (5 points/day = 150/month)

**Q: What if I use multiple wallets?**
A: We have anti-sybil detection. Genuine multi-wallet users OK, but farming will be penalized.

**Q: When does the testnet close?**
A: At mainnet launch (Q2 2026 target). Snapshot taken at launch date.

**Q: Can I still participate after mainnet?**
A: No. This is a **pre-launch** incentive program.

---

## Technical Integration

### For dApp Developers

Track user activities in your dApp:

```python
from luxbin_testnet_rewards import LUXBINTestnetRewards

rewards = LUXBINTestnetRewards()

# User deploys contract via your dApp
rewards.track_activity(
    wallet_address=user_wallet,
    activity_type='contract_deployment',
    metadata={'contract': 'UserToken', 'via': 'YourDApp'}
)
```

### API Endpoints (Coming Soon)

```bash
GET  /api/testnet/stats/:wallet
GET  /api/testnet/leaderboard
POST /api/testnet/activity
POST /api/testnet/bug-report
POST /api/testnet/quest-complete
```

---

## Resources

- **Documentation**: [/docs/testnet-incentives/](../docs/)
- **Bug Reports**: [GitHub Issues](https://github.com/mermaidnicheboutique-code/luxbin-chain/issues)
- **Developer Quests**: [/quests/](./quests/)
- **Support**: nicholechristie555@gmail.com

---

## Summary

**Earn Path**:
```
Test on LUXBIN Testnet
   ↓
Earn Points (activities, quests, bugs)
   ↓
Get Early Tester NFT (2x multiplier)
   ↓
Mainnet Launch
   ↓
Receive LUX Airdrop (25% immediate, 75% vested)
   ↓
Sell on DEX or Hold for staking
```

**Max Earnings Example**:
- Deploy 20 contracts: 1,000 points
- Build DEX: 5,000 points
- Test quantum wallet 10x: 1,000 points
- Find 1 critical bug: 5,000 points + $10k USDC
- Daily active 90 days: 450 points
- Early Tester NFT: 2x multiplier + 10% bonus
- **Total**: ~26,895 LUX + $10k USDC

---

**Built by**: Nichole Christie
**Powered by**: LUXBIN Chain + Quantum Security
**Start earning**: [Register Now](https://luxbin.ai/testnet)

🚀 **The only testnet where your testing actually pays you.**
