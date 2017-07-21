const Web3 = require("web3");
const async = require("async");
// create an instance of web3 using the HTTP provider.
// NOTE in mist web3 is already available, so check first if its available before instantiating
const web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));

const BigNumber = require("bignumber.js");
const fs = require("fs");

/*
var walletAbi =
var walletCode =
*/


const loadFromFile = () => {
    const multisigs = [];
    fs.readFile('wallets.csv', 'utf8', (err, data) => {
        if (err) {
            cb(err);
            return;
        }
        lines = data.split('\n');
        for (i=0; i<lines.length; i++) {
            values = /"(.*)",(\[.*\]),(.*),(.*)/.exec(lines[i]);
            if (values.length == 5) {
                multisigs.push({
                    oldWallet = values[1];
                    owners: JSON.parse(values[2]);
                    required = new BigInteger(values(3));
                    dailyLimit = new BigInteger(values(4));
                })
            }
        }
        cb(null, multisigs);
    });
}

const createWaller = (tokenAddr, cb) => {
    const walletContract = web3.eth.contract(walletAbi);
    walletContract.new(
        owners,
        required,
        dailyLimit,
        {
            from: sourceAccount,
            data: walletCode,
            gas: "800000",
            gasPrice: eth.gasPrice.mul(1.1).floor(),
        },
        (err, contract) => {
            if (err) {
                cb(err);
                return;
            }
            if (typeof contract.address !== "undefined") {
                console.log(`Contract mined! address: ${ contract.address } transactionHash: ${ contract.transactionHash }`);
                cb(null, contract.address);
            }
        });
};

loadFromFile((err) => {
    if (err) {
        console.log("ERROR: ", err);
    } else {
        console.log(JSON.stringify(res, null, 2));
    }
});

