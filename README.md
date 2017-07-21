# WHGBalanceVerification

White Hat Group Deployment Strategy and Data Verification Document



# Strategy  

On the 19th of July the White Hat Group rescued various multisig contracts deployed with vulnerable bytecode. We plan to deploy new multisig contracts with this vulnerability removed. These new multisig contracts will have new addresses, but otherwise maintain the expected constructor parameters (`[_owners]`, `_required`, `_dayLimit`) and the appropriate ether and token balances. 

We aim to do this as safely as possible and as quickly as possible. Therefore, we are submitting the 3 csv files (`multisig_rescue_wallets_filtered.csv`, `multisig_rescue_ether.csv`, and `multisig_rescue_tokens.csv`) that contain the data needed to achieve this task for community review. These files will be used directly for the deployment of the new multisig contracts and the transactions that will fill them.

This deployment will be simulated on the Test Net tomorrow morning (July 22nd).

When we are satisfied with the security & accuracy of `multisig_rescue_wallets_filtered.csv`and our deployment scripts, and the chosen multisig wallet implementation has been finalized by Parity, we will deploy the replacement multisig wallets to the Main Net and generate the `newWallets.csv` file linking the old vulnerable wallet addresses to the new replacement wallet addresses for community review before sending all of the tokens and ether to the newly generated wallets.



#The Contents of ./jbaylina

Please follow the formatting outlined below for your own audits.



## `multisig_rescue_oldwallets_jordi.csv` 

This file describes each wallet that was attempted to be rescued by `0x1dba1131000664b884a1ba238464159892252d3a`specifically listing:

`oldWallet`, `[owners]`, `required`, `day_limit`

Sorted by `oldWallet`; `[owners]` should be a string but formatted as a javascript array.



## `newWallets.csv` (to be generated after deployment to Main Net)

Upon verifying `multisig_rescue_oldwallets_jordi.csv`, and confirming the code for the new multisig contracts with Parity, we will deploy the new wallets and create `newWallets.csv` with 

`oldWallet`, `newWallet`

Sorted by ‘oldWallet’

This will also need to be verified by the community. 



## `multisig_rescue_ether_jordi.csv`

This file lists the tokens that are assumed to have been rescued from each wallet, specifically listing: 

`wallet`, `amount`, `cumulativeAmount`

Sorted by `wallet` with `amount == 0` omitted; `amount` and `cumulativeAmount` are listed in wei.



## `multisig_rescue_tokens_jordi.csv`  

This file lists the tokens that are assumed to have been rescued from each wallet, specifically listing: 

`tokenAddress, tokenSymbol, wallet, amount, cumulativeAmount`

Sorted by `tokenAddress` (all characters should be lowercase) and then by `wallet` with `amount == 0` omitted; `amount` and `cumulativeAmount` are listed in the lowest unit of the token.



# Helping

We are excited to compare our results against YOURS.

Please create a new folder for your implementation. 

The operation is assumed to have started at block 4041168 and ended at 4046151 (Please verify).

We have already recived a community contribution from Bokkypoobah which lives in the ./BokkyPoobah directory. This closely matches the ./jbaylina with a few intersting differences. @rodney757 verified BokkyPoobah's data to produce `multisig_rescue_wallets_filtered.csv` see his README.md in ./rodney757 . @Lefterisjp included an independent analysis which is currently underway. Please see his README.md in ./lefteris. 
