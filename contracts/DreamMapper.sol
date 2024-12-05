pragma solidity ^0.8.0;

contract DreamJournal {
    struct Dream {
        uint id;
        string content;
        address creator;
        bool isShared;
    }

    event DreamAdded(uint indexed dreamId, address indexed dreamCreator);
    event DreamUpdated(uint indexed dreamId, string updatedContent);
    event DreamDeleted(uint indexed dreamId);
    event DreamSharingStatusChanged(uint indexed dreamId, bool newSharingStatus);

    mapping(uint => Dream) private dreams;
    uint private totalDreamsCount;

    modifier onlyDreamCreator(uint dreamId) {
        require(msg.sender == dreams[dreamId].creator, "Not the dream owner");
        _;
    }

    function addDream(string memory dreamContent) public {
        totalDreamsCount++;
        dreams[totalDreamsCount] = Dream(totalDreamsCount, dreamContent, msg.sender, false);
        emit DreamAdded(totalDreamsCount, msg.sender);
    }

    function updateDreamContent(uint dreamId, string memory newContent) public onlyDreamCreator(dreamId) {
        Dream storage selectedDream = dreams[dreamId];
        selectedDream.content = newContent;
        emit DreamUpdated(dreamId, newContent);
    }

    function removeDream(uint dreamId) public onlyDreamCreator(dreamId) {
        delete dreams[dreamId];
        emit DreamDeleted(dreamId);
    }

    function changeDreamSharingStatus(uint dreamId, bool shareStatus) public onlyDreamCreator(dreamId) {
        Dream storage selectedDream = dreams[dreamId];
        selectedDream.isShared = shareStatus;
        emit DreamSharingStatusChanged(dreamId, shareStatus);
    }

    function fetchDreamDetails(uint dreamId) public view returns (string memory content, address dreamOwner, bool sharingStatus) {
        require(dreams[dreamId].id != 0, "Dream does not exist");
        Dream storage selectedDream = dreams[dreamId];
        return (selectedDream.content, selectedDream.creator, selectedDream.isShared);
    }
}