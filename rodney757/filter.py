import csv
import ast
import json

mult_f = open('rodney757/multisig_wallets.csv.array')
data = [ast.literal_eval(r) for r in mult_f]

ether_f = open('BokkyPoobah/ethers.tsv')
tkn_f = open('BokkyPoobah/tokens.tsv')
eth_reader = csv.reader(ether_f, delimiter='\t')
tkn_reader = csv.reader(tkn_f, delimiter='\t')

ether_addrs = [r[0] for r in eth_reader]
ether_addrs = ether_addrs[1:]

tkn_addrs = [r[2] for r in tkn_reader]
tkn_addrs = tkn_addrs[1:]

addrs = ether_addrs

for a in tkn_addrs:
    if a not in addrs:
        addrs.append(a)

filtered_data = []

for i in data:
    if i[0] in addrs:
        filtered_data.append(i)

o_file = open('rodney757/multisig_wallets_filtered.csv', 'w')

for i in filtered_data:
    o_file.write("{}\n".format(i))

o_file.close()
