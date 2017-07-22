# Link to upstream repo calculation?

This subdirectory is the current reflection of the code and data located here: https://github.com/LefterisJP/multisigwallet_whitehat_movements_verification

This subdirectory may be out of date. To make sure if new data exists checkout the originating repo above.




# What is this?

This is a repository containing code for an independent verification of the data concerning the whitehat movements of multiple accounts on the 19th of July concerning the [Ethereum Parity wallet vulnerability](https://www.reddit.com/r/ethereum/comments/6obofq/a_modified_version_of_a_common_multisig_had_a/).

# How to run it?

Use python. I assume you know how to use it. Requirements are all the pyethereum/pyethapp stuff. Also you will need an ethereum node synced in the mainnet on the local host and with rpc open. You can tweak values in the script.

To install requirements do

`pip install -r requirements.txt`

To run the script do:

`python main.py`

This will create the results file in your local directory.

# What is the result?

Two CSV files containing one row per multisig wallet that was touched by the whitehat address. Each row contains the following data in the order shown:
```
multisig_address,amount_in_wei,NEVERDIE,DAO.Casino,1ST,ADST,ADT,ADX,ANT,ARC,BAT,BeerCoin  ,BCDN,BNC,BNT,BQX,CAT,CFI,CRB,CREDO,CTL,CryptoCarbon,CVC,DAO,DDF,DGD,DGX 1.0,DICE,DRP,DNT,EDG,EMV,EOS,FAM,FUN,GNO,GNT,GUP,GT,HKG,HMQ,ICN,JET,JetCoins,LUN,MCAP,MCO,MGO,MDA,MIT,MKR,MLN,MNE,MSP,MTL,MYST,NET,NMR,NxC,OAX,OMG,PAY,PLBT,PTOY,PLU,QAU,QRL,REP,RLC,RLT,ROUND,SGEL,SGT,SHIT,SKIN,SKO1,SNGLS,SNM,SNT,SRC,STORJ,SWT,SNC,TaaS,TFL,TIME,TIX,TKN,TRST,Unicorn  ,VSL,VSM,VERI,VRS,WINGS,XAUR,XID,XRL
```

It is the address of the multisig, the amount of moved ether in WEI and then followed by the moved wei-equivalent token balances for all the known tokens. This data considers `start_block` as `4044976` and `end_block` as `4048770`.


The `big_xxx.csv` file corresponds to movements by the big whitehat address: `0x1dba1131000664b884a1ba238464159892252d3a' and the `small_xxx.csv` corresponds to movements by other smaller addresses known to be whitehat and planning to return funds.

These other addresses are:

- `0x1ff21eca1c3ba96ed53783ab9c92ffbf77862584`
- `0xd1f27c48b948d49f3d098f499b8a1830d8a7e229`
