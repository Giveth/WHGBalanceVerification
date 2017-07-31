pragma solidity ^0.4.13;

contract Owned {
    function Owned() {
        owner = msg.sender;
    }

    address public owner;

    // This contract only defines a modifier and a few useful functions
    // The function body is inserted where the special symbol "_" in the
    // definition of a modifier appears.
    modifier onlyOwner { if (msg.sender == owner) _; }

    function changeOwner(address _newOwner) onlyOwner {
        owner = _newOwner;
    }

    // This is a general safty function that allows the owner to do a lot
    //  of things in the unlikely event that something goes wrong
    // _dst is the contract being called making this like a 1/1 multisig
    function execute(address _dst, uint _value, bytes _data) onlyOwner {
        _dst.call.value(_value)(_data);
    }
}

contract ChooseWHGReturnAddress is Owned {

    mapping (address => address) public returnAddresses;
    uint public endDate;

    /// @param _endDate After this time, if `requestReturn()` has not been called
    /// the upgraded parity multisig will be locked in as the 'returnAddr'
    function ChooseWHGReturnAddress(uint _endDate) {
        endDate = _endDate;
    }

    /////////////////////////
    //   IMPORTANT
    /////////////////////////
    // @dev The `returnAddr` can be changed only once.
    //  We will send the funds to the chosen address. This is Crypto, if the
    //  address is wrong, your funds could be lost, please, proceed with extreme
    //  caution and treat this like you are sending all of your funds to this
    //  address.

    /// @notice This function is used to choose an address for returning the funds.
    ///  This function can only be called once, PLEASE READ THE NOTE ABOVE.
    /// @param _returnAddr The address that will receive the recued funds
    function requestReturn(address _returnAddr) external returns (bool) {

        // After the end date, the newly deployed parity multisig will be
        //  chosen if no transaction is made.
        require(now <= endDate);

        require(returnAddresses[msg.sender] == 0x0);
        returnAddresses[msg.sender] = _returnAddr;
        ReturnRequested(msg.sender, _returnAddr);
        
        return true;
    }

    event ReturnRequested(address indexed origin, address indexed returnAddress);
}
