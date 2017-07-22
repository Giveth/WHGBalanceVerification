const csv = require('./csv');
const async = require('async');

const usedAddr = {};
async.series([
  (cb) => {
    csv.load('ether.csv', (err, addrs) => {
      if (err) {
        cb(err);
        return;
      }
      for (let i = 0; i < addrs.length; i += 1) {
        if (addrs[i].Wallet) {
          usedAddr[addrs[i].Wallet] = true;
        }
      }
      cb();
    });
  },
  (cb) => {
    csv.load('tokens.csv', (err, addrs) => {
      if (err) {
        cb(err);
        return;
      }
      for (let i = 0; i < addrs.length; i += 1) {
        if (addrs[i].Wallet) {
          usedAddr[addrs[i].Wallet] = true;
        }
      }
      cb();
    });
  },
], (err) => {
  if (err) {
    console.log('ERROR: ', err);
  } else {
    console.log(JSON.stringify(Object.keys(usedAddr)));
  }
});
