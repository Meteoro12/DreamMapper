pragma solidity ^0.8.0;

contract DreamJournal {
    struct Dream {
        uint id;
        string content;
        address creator;
        bool isShared;
    }

    event DreamAdded(uint id, address indexed creator);
    event DreamUpdated(uint id, string content);
    event DreamDeleted(uint id);
    event DreamShared(uint id, bool isShared);

    mapping(uint => Dream) private dreams;
    uint private dreamCounter;

    modifier onlyOwner(uint _dreamId) {
        require(msg.sender == dreams[_dreamId].creator, "Not the dream owner");
        _;
    }

    function addDream(string memory _content) public {
        dreamCounter++;
        dreams[dreamCounter] = Dream(dreamCounter, _content, msg.sender, false);
        emit DreamAdded(dreamCounter, msg.sender);
    }

    function updateDream(uint _dreamId, string memory _content) public onlyOwner(_dreamId) {
        Dream storage dream = dreams[_dreamId];
        dream.content = _content;
        emit DreamUpdated(_dreamId, _content);
    }

    function deleteDream(uint _dreamId) public onlyOwner(_dreamId) {
        delete dreams[_dreamId];
        emit DreamDeleted(_dreamId);
    }

    function shareDream(uint _dreamId, bool _share) public onlyOwner(_dreamId) {
        Dream storage dream = dreams[_dreamId];
        dream.isShared = _share;
        emit DreamShared(_dreamId, _share);
    }

    function getDream(uint _dreamId) public view returns (string memory content, address creator, bool isShared) {
        require(dreams[_dreamId].id != 0, "Dream does not exist");
        Dream storage dream = dreams[_dreamId];
        return (dream.content, dream.creator, dream.isShared);
    }
}