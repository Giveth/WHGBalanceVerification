
This token detection is very much like jordi's with minor differences.
 - I do not use a pre-defined list of wallets or tokens.
 - the only "input" is the whg address and the transfer event log topic.
 - the filter doesn't include the token address, which allowed me to find the additional token
 - I was using web3.toDecimal where jordi uses BigNumber(hex, 16) and got come rounding errors.
 - I'm comparing balance at current block via contract call vs balance at block before hack
 - I'm not considering the token's decimal places


method:

using a filter, as defined https://github.com/ethereum/wiki/wiki/JavaScript-API#web3ethfilter

1. find Tranfer event logs going to whg, emmitted from any contract

2. for each address emitting the event log (a token), sum all transfer amounts

3. subtract tokens held at whg before hack

4. compare the sum of transfer amounts with the current balance from a call to contract.

5. print if not matching


results:

54 transfer events
27 tokens
3 web3.toDecimal rounding errors

rounding errors when using web3.toDecimal:
0x888666CA69E0f178DED6D75b5726Cee99A87D698 (ICONOMI) - current balance has 2147483648 more than transfers
0x1f573d6fb3f13d689ff844b4ce37794d79a7ff1c (Bancor)  - current balance has 16777216 less than transfers
0xa74476443119a942de498590fe1f2454d7d4ac0d (Golem)   - current balance has 134217728 less than transfers


--------------------------


Comparing to jordi's token data:
 - Jordi's list does not include token 0xc63e7b1dece63a77ed7e4aeef5efb3b05c81438d (the FUCK token), which makes sense to not include.
 - my code finds 2 extra transactions, both for this token
 - my code finds 1 extra token

--------------------------

The transfers match the current balance of the whg account, minus tokens it held before the hack.
