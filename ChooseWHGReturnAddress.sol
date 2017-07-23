pragma solidity ^0.4.13;

contract ChooseWHGReturnAddress {

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
