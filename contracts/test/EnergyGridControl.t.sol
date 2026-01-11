// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/Test.sol";
import "../src/EnergyGridControl.sol";

contract EnergyGridControlTest is Test {
    EnergyGridControl public gridControl;
    address public owner;
    address public proposer;
    address public voter1;
    address public voter2;
    address public voter3;
    address public unauthorized;

    bytes public samplePhotonicData = hex"48656c6c6f20576f726c64"; // "Hello World" in hex

    function setUp() public {
        owner = address(this);
        proposer = makeAddr("proposer");
        voter1 = makeAddr("voter1");
        voter2 = makeAddr("voter2");
        voter3 = makeAddr("voter3");
        unauthorized = makeAddr("unauthorized");

        gridControl = new EnergyGridControl();

        // Authorize proposer and voters
        gridControl.authorizeProposer(proposer);
        gridControl.authorizeVoter(voter1);
        gridControl.authorizeVoter(voter2);
        gridControl.authorizeVoter(voter3);
    }

    function testProposeCommand() public {
        vm.prank(proposer);
        gridControl.proposeCommand("REDUCE_LOAD_15%", "north_america", samplePhotonicData);

        assertEq(gridControl.commandCount(), 1);
        EnergyGridControl.GridCommand memory cmd = gridControl.getCommand(1);
        assertEq(cmd.command, "REDUCE_LOAD_15%");
        assertEq(cmd.region, "north_america");
        assertEq(cmd.proposer, proposer);
        assertFalse(cmd.executed);
    }

    function testFailUnauthorizedPropose() public {
        vm.prank(unauthorized);
        gridControl.proposeCommand("TEST", "global", samplePhotonicData);
    }

    function testVoteOnCommand() public {
        // Propose command
        vm.prank(proposer);
        gridControl.proposeCommand("OPTIMIZE_SOLAR", "europe", samplePhotonicData);

        // Vote yes
        vm.prank(voter1);
        gridControl.voteOnCommand(1, true);

        vm.prank(voter2);
        gridControl.voteOnCommand(1, true);

        // Should auto-execute with 3 votes
        vm.prank(voter3);
        gridControl.voteOnCommand(1, true);

        EnergyGridControl.GridCommand memory cmd = gridControl.getCommand(1);
        assertTrue(cmd.executed);
        assertEq(cmd.votesFor, 3);
    }

    function testFailDoubleVote() public {
        vm.prank(proposer);
        gridControl.proposeCommand("TEST", "global", samplePhotonicData);

        vm.prank(voter1);
        gridControl.voteOnCommand(1, true);

        vm.prank(voter1);
        vm.expectRevert("Already voted");
        gridControl.voteOnCommand(1, true);
    }

    function testRegisterEnergyNode() public {
        vm.prank(voter1);
        gridControl.registerEnergyNode("New York, USA", 500);

        EnergyGridControl.EnergyNode memory node = gridControl.energyNodes(voter1);
        assertEq(node.location, "New York, USA");
        assertEq(node.capacity, 500);
        assertTrue(node.isActive);
    }

    function testFailRegisterTwice() public {
        vm.prank(voter1);
        gridControl.registerEnergyNode("Location", 100);

        vm.prank(voter1);
        vm.expectRevert("Node already registered");
        gridControl.registerEnergyNode("Another", 200);
    }

    function testHeartbeat() public {
        vm.prank(voter1);
        gridControl.registerEnergyNode("Location", 100);

        uint256 beforeHeartbeat = gridControl.energyNodes(voter1).lastHeartbeat;

        vm.warp(block.timestamp + 1 hours);

        vm.prank(voter1);
        gridControl.heartbeat();

        uint256 afterHeartbeat = gridControl.energyNodes(voter1).lastHeartbeat;
        assertGt(afterHeartbeat, beforeHeartbeat);
    }

    function testEmergencyShutdown() public {
        // Should not revert for owner
        gridControl.emergencyShutdown();
    }

    function testFailEmergencyShutdownUnauthorized() public {
        vm.prank(unauthorized);
        vm.expectRevert("Ownable: caller is not the owner");
        gridControl.emergencyShutdown();
    }
}