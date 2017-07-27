const Web3 = require('web3');
const async = require('async');
// create an instance of web3 using the HTTP provider.
// NOTE in mist web3 is already available, so check first if its available before instantiating
const web3 = new Web3(new Web3.providers.HttpProvider('http://localhost:8545'));

const csv = require('./csv');

const BigNumber = require('bignumber.js');

var chooseWHGReturnAddressAbi = [{"constant":true,"inputs":[{"name":"_addr","type":"address"}],"name":"getReturnAddress","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_returnAddr","type":"address"}],"name":"requestReturn","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_addr","type":"address"}],"name":"isReturnRequested","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_newOwner","type":"address"}],"name":"changeOwner","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_dst","type":"address"},{"name":"_value","type":"uint256"},{"name":"_data","type":"bytes"}],"name":"execute","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"endDate","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"inputs":[{"name":"_endDate","type":"uint256"}],"payable":false,"type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"origin","type":"address"},{"indexed":true,"name":"returnAddress","type":"address"}],"name":"ReturnRequested","type":"event"}];
var chooseWHGReturnAddress = web3.eth.contract(chooseWHGReturnAddressAbi).at('0x3abe5285ED57c8b028D62D30c456cA9eb3E74105');


const fillReturnAddress = (txs, cb) => {
  async.each(txs, (_tx, cb2) => {
    const tx = _tx;
    chooseWHGReturnAddress.isReturnRequested(tx.newWallet, (err, res) => {
      if (err) {
        cb2(err);
        return;
      }
      if (!res) {
        tx.returnAddress = '';
        cb2();
        return;
      }
      chooseWHGReturnAddress.getReturnAddress(tx.newWallet, (err2, res2) => {
        if (err2) {
          cb2(err);
          return;
        }
        tx.returnAddress = res2;
        cb2();
      });
    });
  }, cb);
};

const fillNewAddress = (_txs, cb) => {
  const txs = _txs;
  const mapping = {};
  csv.load('./walletMapping.csv', (err, res) => {
    if (err) {
      cb(err);
      return;
    }
    for (let i = 0; i < res.length; i += 1) {
      if (typeof res[i].oldWallet === 'string') {
        mapping[res[i].oldWallet.toLowerCase()] = res[i].newWallet.toLowerCase();
      }
    }
    for (let i = 0; i < txs.length; i += 1) {
      txs[i].newWallet = mapping[txs[i].oldWallet];
    }
    cb();
  });
};


let txs = [];
async.series([
  (cb) => {
    csv.load('./ether.csv', (err, _res) => {
      if (err) {
        cb(err);
        return;
      }
      const res = _res;
      for (let i = 0; i < res.length; i += 1) {
        res[i].tokenAddr = '0x0000000000000000000000000000000000000000';
        res[i].tokenSymbol = 'ETH';
      }
      txs = txs.concat(res);
      cb();
    });
  },
  (cb) => {
    csv.load('./tokens.csv', (err, res) => {
      if (err) {
        cb(err);
        return;
      }
      txs = txs.concat(res);
      cb();
    });
  },
  (cb) => {
    fillNewAddress(txs, cb);
  },
  (cb) => {
    fillReturnAddress(txs, cb);
  },
  (cb) => {
    txs = txs.sort((a, b) => (a.newWallet > b.newWallet ? 1 : -1));
    csv.save('out.csv', ['returnAddress', 'amount', 'tokenSymbol', 'tokenAddr', 'oldWallet', 'newWallet'], txs, cb);
  },
  (cb) => {
    let acc = 0;
    for (let i = 0; i < txs.length; i += 1) {
      if (txs[i].returnAddress) acc += 1;
    }
    console.log('Total TXs:', acc);
    cb();
  },
], (err) => {
  if (err) {
    console.log('ERROR:', err);
  }
});
