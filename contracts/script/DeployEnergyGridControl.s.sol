// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/Script.sol";
import "../src/EnergyGridControl.sol";

contract DeployEnergyGridControl is Script {
    function run() external {
        vm.startBroadcast();

        EnergyGridControl gridControl = new EnergyGridControl();

        console.log("EnergyGridControl deployed at:", address(gridControl));

        vm.stopBroadcast();
    }
}