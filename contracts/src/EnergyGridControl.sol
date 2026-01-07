// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/console.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title EnergyGridControl
 * @dev Decentralized energy grid optimization using LUXBIN photonic encoding
 * @notice Manages global energy consumption through photonic command signals
 * @author NicheAI - Sustainable Computing Technologies
 */
contract EnergyGridControl is Ownable, ReentrancyGuard {
    // Structs
    struct GridCommand {
        string command;           // e.g., "REDUCE_LOAD_15%"
        string region;           // Geographic region
        bytes photonicData;      // LUXBIN encoded photonic sequence
        address proposer;        // Command proposer
        uint256 timestamp;       // Proposal time
        uint256 executionTime;   // When to execute
        bool executed;          // Execution status
        uint256 votesFor;       // Consensus votes
        uint256 votesAgainst;
    }

    struct EnergyNode {
        address nodeAddress;
        string location;
        uint256 capacity;        // Energy capacity in MW
        bool isActive;
        uint256 lastHeartbeat;
    }

    // State variables
    mapping(uint256 => GridCommand) public commands;
    mapping(address => EnergyNode) public energyNodes;
    mapping(uint256 => mapping(address => bool)) public hasVoted; // commandId => voter => voted
    mapping(address => bool) public authorizedProposers;
    mapping(address => bool) public authorizedVoters;

    uint256 public commandCount;
    uint256 public constant VOTING_PERIOD = 7 days;
    uint256 public constant EXECUTION_DELAY = 1 hours;
    uint256 public constant MIN_VOTES_REQUIRED = 3; // For demo, low threshold

    // Events
    event CommandProposed(uint256 indexed commandId, string command, string region, address proposer);
    event CommandVoted(uint256 indexed commandId, address voter, bool support);
    event CommandExecuted(uint256 indexed commandId, bytes photonicData);
    event NodeRegistered(address indexed nodeAddress, string location, uint256 capacity);
    event PhotonicSignalEmitted(uint256 indexed commandId, bytes data);

    // Modifiers
    modifier onlyAuthorizedProposer() {
        require(authorizedProposers[msg.sender] || owner() == msg.sender, "Not authorized proposer");
        _;
    }

    modifier onlyAuthorizedVoter() {
        require(authorizedVoters[msg.sender] || owner() == msg.sender, "Not authorized voter");
        _;
    }

    modifier commandExists(uint256 _commandId) {
        require(_commandId > 0 && _commandId <= commandCount, "Command does not exist");
        _;
    }

    modifier votingOpen(uint256 _commandId) {
        GridCommand storage cmd = commands[_commandId];
        require(block.timestamp <= cmd.timestamp + VOTING_PERIOD, "Voting period ended");
        require(!cmd.executed, "Command already executed");
        _;
    }

    constructor() {
        // Initialize owner as authorized
        authorizedProposers[owner()] = true;
        authorizedVoters[owner()] = true;
    }

    /**
     * @dev Propose a new energy grid command
     * @param _command The energy command (e.g., "REDUCE_LOAD_15%")
     * @param _region Geographic region for command
     * @param _photonicData LUXBIN encoded photonic sequence
     */
    function proposeCommand(
        string calldata _command,
        string calldata _region,
        bytes calldata _photonicData
    ) external onlyAuthorizedProposer nonReentrant {
        require(bytes(_command).length > 0, "Command cannot be empty");
        require(bytes(_region).length > 0, "Region cannot be empty");
        require(_photonicData.length > 0, "Photonic data required");

        commandCount++;
        GridCommand storage newCommand = commands[commandCount];
        newCommand.command = _command;
        newCommand.region = _region;
        newCommand.photonicData = _photonicData;
        newCommand.proposer = msg.sender;
        newCommand.timestamp = block.timestamp;
        newCommand.executionTime = block.timestamp + VOTING_PERIOD + EXECUTION_DELAY;

        emit CommandProposed(commandCount, _command, _region, msg.sender);
    }

    /**
     * @dev Vote on a proposed command
     * @param _commandId ID of the command to vote on
     * @param _support True for approval, false for rejection
     */
    function voteOnCommand(
        uint256 _commandId,
        bool _support
    ) external onlyAuthorizedVoter commandExists(_commandId) votingOpen(_commandId) nonReentrant {
        require(!hasVoted[_commandId][msg.sender], "Already voted");

        hasVoted[_commandId][msg.sender] = true;
        GridCommand storage cmd = commands[_commandId];

        if (_support) {
            cmd.votesFor++;
        } else {
            cmd.votesAgainst++;
        }

        emit CommandVoted(_commandId, msg.sender, _support);

        // Auto-execute if consensus reached
        if (cmd.votesFor >= MIN_VOTES_REQUIRED && cmd.votesFor > cmd.votesAgainst) {
            _executeCommand(_commandId);
        }
    }

    /**
     * @dev Execute a command after voting period or consensus
     * @param _commandId ID of the command to execute
     */
    function executeCommand(uint256 _commandId) external commandExists(_commandId) nonReentrant {
        GridCommand storage cmd = commands[_commandId];
        require(!cmd.executed, "Command already executed");
        require(block.timestamp >= cmd.timestamp + VOTING_PERIOD, "Voting period not ended");
        require(cmd.votesFor > cmd.votesAgainst, "Command not approved");

        _executeCommand(_commandId);
    }

    /**
     * @dev Internal execution of approved command
     * @param _commandId Command to execute
     */
    function _executeCommand(uint256 _commandId) internal {
        GridCommand storage cmd = commands[_commandId];
        cmd.executed = true;

        // Emit photonic signal for satellite transmission
        emit PhotonicSignalEmitted(_commandId, cmd.photonicData);
        emit CommandExecuted(_commandId, cmd.photonicData);

        console.log("Energy grid command executed:", cmd.command);
        console.log("Region:", cmd.region);
        console.log("Photonic data length:", cmd.photonicData.length);
    }

    /**
     * @dev Register an energy node in the grid
     * @param _location Geographic location
     * @param _capacity Energy capacity in MW
     */
    function registerEnergyNode(
        string calldata _location,
        uint256 _capacity
    ) external nonReentrant {
        require(!energyNodes[msg.sender].isActive, "Node already registered");

        energyNodes[msg.sender] = EnergyNode({
            nodeAddress: msg.sender,
            location: _location,
            capacity: _capacity,
            isActive: true,
            lastHeartbeat: block.timestamp
        });

        emit NodeRegistered(msg.sender, _location, _capacity);
    }

    /**
     * @dev Update node heartbeat
     */
    function heartbeat() external {
        require(energyNodes[msg.sender].isActive, "Node not registered");
        energyNodes[msg.sender].lastHeartbeat = block.timestamp;
    }

    /**
     * @dev Authorize a proposer
     * @param _proposer Address to authorize
     */
    function authorizeProposer(address _proposer) external onlyOwner {
        authorizedProposers[_proposer] = true;
    }

    /**
     * @dev Authorize a voter
     * @param _voter Address to authorize
     */
    function authorizeVoter(address _voter) external onlyOwner {
        authorizedVoters[_voter] = true;
    }

    /**
     * @dev Get command details
     * @param _commandId Command ID
     * @return Command struct
     */
    function getCommand(uint256 _commandId) external view commandExists(_commandId) returns (GridCommand memory) {
        return commands[_commandId];
    }

    /**
     * @dev Get total energy capacity across all nodes
     * @return Total capacity in MW
     */
    function getTotalGridCapacity() external view returns (uint256) {
        uint256 total = 0;
        // In production, iterate through all nodes (requires off-chain indexing)
        // For demo, return placeholder
        return total;
    }

    /**
     * @dev Emergency shutdown (owner only)
     */
    function emergencyShutdown() external onlyOwner {
        // Implement emergency protocols
        console.log("Emergency shutdown initiated by:", msg.sender);
    }
}