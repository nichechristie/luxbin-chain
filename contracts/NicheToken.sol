// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";

/**
 * @title NicheToken
 * @dev $Niche token with fixed supply of 21 million, tied to Luxbin chain
 * Fully gas-free on Luxbin's zero-fee network
 * Inspired by Luxbin's Bitcoin-like scarcity model
 * Compatible with OpenZeppelin v5.x
 */
contract NicheToken is ERC20, ERC20Burnable {
    // Fixed supply: 21 million NICHE (mirroring Luxbin's LUX supply for consistency)
    uint256 public constant TOTAL_SUPPLY = 21_000_000 * 10**18;

    constructor() ERC20("Niche", "NICHE") {
        // Mint entire supply to deployer
        _mint(msg.sender, TOTAL_SUPPLY);
    }
}