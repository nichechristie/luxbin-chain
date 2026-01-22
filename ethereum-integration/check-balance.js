const Web3 = require('web3');

// Luxbin Chain Ethereum Balance Checker
// This script demonstrates checking Ethereum balances for Luxbin interoperability

async function checkEthereumBalance() {
    // Connect to Ethereum network
    const web3 = new Web3('https://mainnet.infura.io/v3/YOUR_INFURA_KEY');

    // Your Ethereum address
    const address = process.env.ETH_ADDRESS || '0x0000000000000000000000000000000000000000';

    try {
        // Get ETH balance
        const balanceWei = await web3.eth.getBalance(address);
        const balanceEth = web3.utils.fromWei(balanceWei, 'ether');

        console.log(`ETH Balance for ${address}: ${balanceEth} ETH`);

        // Get ERC-20 token balance (example: USDC)
        const usdcContract = new web3.eth.Contract([
            {
                "constant": true,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            }
        ], '0xA0b86a33E6441e88C5d5c5c5c5c5c5c5c5c5c5c5c'); // USDC contract address

        const usdcBalance = await usdcContract.methods.balanceOf(address).call();
        const usdcBalanceFormatted = web3.utils.fromWei(usdcBalance, 'mwei'); // USDC has 6 decimals

        console.log(`USDC Balance: ${usdcBalanceFormatted} USDC`);

        // Check if address is eligible for bridging
        const isEligible = parseFloat(balanceEth) > 0.1; // Example threshold
        console.log(`Eligible for bridging: ${isEligible ? 'Yes' : 'No'}`);

    } catch (error) {
        console.error('Balance check failed:', error);
    }
}

// Run the balance check
if (require.main === module) {
    checkEthereumBalance();
}

module.exports = { checkEthereumBalance };