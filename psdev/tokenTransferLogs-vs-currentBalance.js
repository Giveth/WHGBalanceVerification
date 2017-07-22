var Web3 = require('web3');
var BigNumber = require('bignumber.js');

var web3 = new Web3();
web3.setProvider(new web3.providers.HttpProvider('http://192.168.1.3:8545'));

var abi = [{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"type":"function"}];
var whgAddress = "0x1DBA1131000664b884A1Ba238464159892252D3a";
var startBlock = 4041168;
var endBlock = 4046151;

var transfers = [];
var whgTokenBalances = {};
var anomalies = 0;

function topic2Address(topic) {
    if(topic == undefined) { return ""; }
    var topicStr = new String(topic);
    return "0x" + topicStr.substr(26,topicStr.length);
}

function compare(a,b) {
    if (a.token < b.token)
        return -1;
    if (a.token > b.token)
        return 1;
    if (a.from < b.from)
        return -1;
    if (a.from > b.from)
        return 1;
    return 0;
}

var options = {
    fromBlock: startBlock,
    toBlock: endBlock,
    topics: ["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef", null, "0x0000000000000000000000001dba1131000664b884a1ba238464159892252d3a"]
};

var filter = web3.eth.filter(options);
filter.get(function(error, logs){
    logs.forEach((log) => {
        var transfer = {
            token: log.address,
            from: topic2Address(log.topics[1]),
            to: topic2Address(log.topics[2]),
            // amount: log.data
            amount:  new BigNumber(log.data.substring(2), 16)
        }
        transfers.push(transfer);
    });

   transfers.sort(compare);

    // sum per token
    transfers.forEach((transfer) => {
        if (whgTokenBalances[transfer.token] == undefined) {
            whgTokenBalances[transfer.token] = new BigNumber(0);
            // whgTokenBalances[transfer.token] = web3.toDecimal(0x0);
        }
        // whgTokenBalances[transfer.token] = whgTokenBalances[transfer.token] + web3.toDecimal(transfer.amount);
        whgTokenBalances[transfer.token] = whgTokenBalances[transfer.token].add(transfer.amount);
    });

    // compare transfers with current balance
    Object.keys(whgTokenBalances).forEach((tokenAddress) => {
        var token = web3.eth.contract(abi).at(tokenAddress);
        var sumTransfers = whgTokenBalances[tokenAddress];
        var currentBalance = new BigNumber(token.balanceOf(whgAddress));
        var preBalance = new BigNumber(token.balanceOf(whgAddress, startBlock-1));

        var balanceDiffBeforeHack = currentBalance.minus(preBalance);

        // var balance = web3.toDecimal(web3.fromDecimal(balanceDiffBeforeHack));

        if (!balanceDiffBeforeHack.equals(sumTransfers)) {
            var diffExpected = sumTransfers.minus(balanceDiffBeforeHack);
            anomalies++;
            console.log("");
            console.log("token=" + tokenAddress);
            console.log("           sumTransfers=" + sumTransfers);
//            console.log("                balance=" + balance);
            console.log("           diffExpected=" + diffExpected);
            console.log("  balanceDiffBeforeHack=" + balanceDiffBeforeHack.toFixed());
            console.log("         currentBalance=" + currentBalance.toFixed());
            console.log("             preBalance=" + preBalance.toFixed());
        }
    });

    // console.log("transferCount=" + transfers.length);
    // console.log("   tokenCount=" + Object.keys(whgTokenBalances).length);
    // console.log("    anomalies=" + anomalies);

    //output file matching jordi's but without TokenSymbol
    transfers.forEach((transfer) => {
        if (whgTokenBalances[transfer.token] == undefined) {
            whgTokenBalances[transfer.token] = new BigNumber(0);
        }

        whgTokenBalances[transfer.token] = whgTokenBalances[transfer.token].add(transfer.amount);

        console.log("\"" + transfer.token + "\",\"" + transfer.from + "\"," + transfer.amount.toFixed() + "," + whgTokenBalances[transfer.token].toFixed());
    });

});
