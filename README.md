# WHGBalanceVerification
White Hat Group Verification Draft

# Accounting of Multisig Clearing

On the 19th of July the White Hat Group rescued various multisig contracts that had vulnerable bytecode. We plan to redeploy new multisig contracts with this vulnerability removed. These new multisig contracts will have new addresses, but otherwise maintain their original state (owners, m_required, m_dailyLimit, ether and token balances). 

We aim  to do this as safely as possible and as quickly as possible. Therefore, we are submitting 3 csv files (`oldWallets.csv`, `multisig_rescue_ether.csv`, and multisig_rescue_tokens.csv) and  1 set of bytecode (`newWalletBytecode.txt`) that we will use to achieve this task. 

When we are satisfied with the security & accuracy of `oldWallets.csv` and `newWalletBytecode.txt`, and about 24 hours has passed with no changes to these two files, we will deploy the replacement multisig wallets and generate the `newWallets.csv` file linking the old vulnerable wallet addresses to the new replacement wallet addresses for community review. After an additional  24 hours of no changes to this file, we will send all of the tokens and ether to the newly generated wallets.
## multisig_rescue_oldwallets_jordi.csv and newWallets.csv
This file contains a list of each wallet that was emptied by the following accounts: 
0x1dba1131000664b884a1ba238464159892252d3a

`Old Wallet, "[owners]", required, day_limit`

This file should be sorted by `Old Wallet`.
`[owners]` should be a string but formatted as a javascript array.

Upon verifying this data, and verifying the bytecode for the upgraded multisig contracts, we will generate all of the new wallets and create a .csv file with 

`oldWallet, newWallet`

This will also need to be verified by the community. 
https://gist.github.com/jbaylina/3c6db1c092cb23893ad5a4414eb628d5 
## multisig_rescue_ether.csv

`wallet, amount, cumulativeAmount`

Sorted by amount and then the wallet with the 0 amounts omitted.
## multisig_rescue_tokens.csv  

`tokenAddress, tokenSymbol, wallet, amount, cumulativeAmount`

Sorted by token address (all characters should be lowercase) and then the wallet with the 0 amounts omitted.



## Helping

We are happy to compare against any version of the accounting.

Please create a new folder for each implementation. Sample list of multisig_rescue_ether_jordi.csv can be found 
https://gist.github.com/jbaylina/2cdf93d94ad1034e562ccc1d40bc64ea

Sample of multisig_rescue_tokens_jordi.csv  https://gist.github.com/jbaylina/9daaef61f604b08d0e2c24bf5b16ec2a 

The operation is assumed to have started at block 4044813 and ended at 4046151 (Please verify).








