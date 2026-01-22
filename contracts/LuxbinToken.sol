// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";

/**
 * @title LuxbinToken
 * @dev LUXBIN token with fixed supply of 21 million, similar to Bitcoin
 * Compatible with OpenZeppelin v5.x
 */
contract LuxbinToken is ERC20, ERC20Burnable {
    // Fixed supply: 21 million LUXBIN (like Bitcoin)
    uint256 public constant TOTAL_SUPPLY = 21_000_000 * 10**18;

    constructor() ERC20("LUXBIN", "LUX") {
        // Mint entire supply to deployer
        _mint(msg.sender, TOTAL_SUPPLY);
    }
}
