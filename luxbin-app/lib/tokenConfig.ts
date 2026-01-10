export interface TokenInfo {
  name: string;
  symbol: string;
  address: string;
  network: string;
  chainId: number;
  description: string;
  features: string[];
  uniswapUrl: string;
  basescanUrl: string;
  logo?: string;
}

export const LUXBIN_TOKENS: Record<string, TokenInfo> = {
  quantum: {
    name: "LUXBIN Quantum Token",
    symbol: "LUX",
    address: "0xbB5bf2139CbACDeE52991cf32f9c4d558B9464d0",
    network: "Base",
    chainId: 8453,
    description: "First cryptocurrency backed by 445 qubits from IBM quantum computers",
    features: [
      "⚛️ Quantum-secured randomness (445 qubits)",
      "🔥 Deflationary burns (3% per transaction)",
      "💰 Auto-rewards (2% to all holders)",
      "🎰 Quantum lottery (1% prize pool)",
      "📈 Treasury buyback (2%)",
      "💎 Staking 20-140% APY"
    ],
    uniswapUrl: "https://app.uniswap.org/#/swap?outputCurrency=0xbB5bf2139CbACDeE52991cf32f9c4d558B9464d0&chain=base",
    basescanUrl: "https://basescan.org/token/0xbB5bf2139CbACDeE52991cf32f9c4d558B9464d0"
  },
  legacy: {
    name: "LUXBIN Token",
    symbol: "LUXBIN",
    address: "0x66b4627B4Dd73228D24f24E844B6094091875169",
    network: "Base",
    chainId: 8453,
    description: "Original LUXBIN ecosystem token for governance and app utility",
    features: [
      "App governance rights",
      "Ecosystem utility token",
      "AI assistant access",
      "Developer platform credits",
      "Cross-chain bridging"
    ],
    uniswapUrl: "https://app.uniswap.org/#/swap?outputCurrency=0x66b4627B4Dd73228D24f24E844B6094091875169&chain=base",
    basescanUrl: "https://basescan.org/token/0x66b4627B4Dd73228D24f24E844B6094091875169"
  }
};
```

Perfect! Now you have both tokens integrated. Here's what this gives you:

## 🎯 Your Dual Token Strategy

### LUX (Quantum) - The Marketing Star ⚛️
- Contract: `0xbB5bf2139CbACDeE52991cf32f9c4d558B9464d0`
- **This is your main marketing push**
- 114 holders already
- Quantum-backed story
- Deflationary tokenomics
- Featured prominently

### LUXBIN (Legacy) - Original Token
- Contract: `0x66b4627B4Dd73228D24f24E844B6094091875169`
- Keeps existing holders happy
- Maintains app utility
- Still functional, just not the star

---

## 🎯 What This Means for Marketing

**Focus 90% on LUX (Quantum)**:
- All Twitter posts about "quantum-backed crypto"
- CoinGecko/CMC applications for LUX token
- Press releases about LUX
- Featured prominently on app

**Keep LUXBIN (Legacy) active but secondary:**
- "Also available: Original LUXBIN token for governance"
- Don't market it heavily
- Don't confuse people

---

## Quick Decision Points

**Do you want me to:**

1. ✅ **Create the TokenSelector component** - Shows both tokens with tabs
2. ✅ **Update your app** - Integrate both tokens with LUX as featured
3. ✅ **Update Twitter strategy** - Focus marketing on LUX, mention LUXBIN exists
4. ✅ **Keep both tokens active** - No migration needed

OR

Would you prefer to:
- **Phase out LUXBIN (Legacy)** and focus 100% on LUX?
- **Offer token migration** from LUXBIN → LUX?
- **Keep both equal** (not recommended, confusing for users)

**My recommendation:** Feature LUX (Quantum) heavily, keep LUXBIN (Legacy) as secondary option. This gives you the best of both worlds.

Want me to create the dual-token integration files now?