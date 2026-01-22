# Luxbin Chain - Ethereum Interoperability

This directory contains tools and examples for interoperating between Luxbin Chain and Ethereum.

## Features

- **Asset Bridging**: Bridge ETH and ERC-20 tokens between Ethereum and Luxbin Chain using Snowbridge
- **Balance Checking**: Monitor Ethereum balances for bridging eligibility
- **Cross-Chain Messaging**: Send messages between chains via bridge protocols

## Setup

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
export PRIVATE_KEY="your_ethereum_private_key"
export ETH_ADDRESS="your_ethereum_address"
export INFURA_KEY="your_infura_project_id"
```

## Usage

### Check Ethereum Balance
```bash
npm run check-balance
```

### Bridge Assets to Luxbin
```bash
npm run bridge-asset
```

### Send Cross-Chain Message
```bash
npm run send-message
```

## Architecture

- **Snowbridge Integration**: Leverages existing Snowbridge bridge in `../bridges/snowbridge/`
- **Web3 Libraries**: Uses ethers.js v6 and web3.js v4 for Ethereum interactions
- **Cross-Consensus Messaging**: Implements XCMP-compatible messaging via bridge contracts

## Security Notes

- Never commit private keys to version control
- Use hardware wallets for mainnet transactions
- Test on testnets (Sepolia, Luxbin testnet) before mainnet deployment

## Related Components

- `../bridges/` - Core bridging infrastructure
- `../contracts/` - Smart contracts for interoperability
- `../scripts/snowbridge_update_subtree.sh` - Bridge updates