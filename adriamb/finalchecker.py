import web3
import eth_utils
import urllib
import locale

ETH                 = 'ETH'
CSVURL              = 'https://raw.githubusercontent.com/Giveth/WHGBalanceVerification/76a7ddbd5e30e7c649591b510b35fb5edaf07645/WHGMultisigReturnTxs.csv'
TOKENDEF_ABI        = [{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"type":"function"}]
HWG_ADDRS           = ['0xd1f27c48b948d49f3d098f499b8a1830d8a7e229','0x1dba1131000664b884a1ba238464159892252d3a']
TOPIC_ERC20TRANSFER = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
NEWMULTISIG_SHA3    = '0x92a0d09eb2bae4c35688dfce7de824fe4683e3ec8fb22f30c7e8035f5223a4c9'

w3 = web3.Web3(web3.HTTPProvider('http://localhost:8545'))

checkedoldwallets = {}
checkednewwallets = {}
tokens = {
	ETH    : { 'sum' : 0, 'decimals' : 18, 'symbol': ETH },
	'DGD'  : { 'sum' : 0, 'address' : '0xe0b7927c4af23765cb51314a0e0521a9645f0e2a', 'decimals' : 0 , 'symbol' : 'DGD' },
	'EOS'  : { 'sum' : 0, 'address' : '0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0', 'decimals' : 18, 'symbol' : 'EOS' },
	'REP'  : { 'sum' : 0, 'address' : '0x48c80f1f4d53d5951e5d5438b54cba84f29f32a5', 'decimals' : 18, 'symbol' : 'REP' },
	'FST'  : { 'sum' : 0, 'symbol'  : '1ST' },
	'DICE' : { 'sum' : 0, 'symbol'  : 'ROL' }
}

def checkNewMultisig(address):
	if not address in checkednewwallets:
		code = w3.eth.getCode(address)
	   	sha3 = w3.sha3(code)
		if sha3 != NEWMULTISIG_SHA3:
			raise Exception(address+": new contract has bad bash "+sha3)
		else:
			print "+ multisig "+address
		checkedoldwallets[address]=True

def checkToken(address,symbol):

	if symbol == ETH:
		return

	expectedSymbol = symbol

	if symbol in tokens:
		if 'address' in tokens[symbol]:
			if tokens[symbol]['address'] != address:
				raise Exception("Address mismatch for symbol "+symbol)
		if 'symbol' in tokens[symbol]:
			expectedSymbol = tokens[symbol]['symbol']

	if (not symbol in tokens) or (not 'address' in tokens[symbol]):
		contract_factory = web3.contract.construct_contract_factory(
			web3=w3,
			abi=TOKENDEF_ABI
		)
		token = contract_factory(address)
		if token.call().symbol() != expectedSymbol:
			raise Exception(address+" "+expectedSymbol+" bad symbol "+token.call().symbol())
		else:
			print "+ symbol "+symbol

		if not symbol in tokens:
			tokens[symbol]={}

		tokens[symbol]['decimals']=token.call().decimals()
		tokens[symbol]['symbol']=expectedSymbol
		tokens[symbol]['address']=address
		tokens[symbol]['sum']=0

def format(amount, symbol):
	return "{:,}".format(amount/float(pow(10,tokens[symbol]['decimals'])))+" "+tokens[symbol]['symbol']

def check(csvoldaddr,csvnewaddr,csvretaddr,csvamount,csvsymbol,csvtxid,csvfromaddr):

	checkNewMultisig(csvnewaddr)

	receipt = w3.eth.getTransactionReceipt(csvtxid)
	tx = w3.eth.getTransaction(csvtxid)

	ethFrom = tx['from']
	ethTo = tx['to']
	ethValue = tx['value']

	tokenFrom = 0
	tokenTo = "0x"
	token = "NONE"
	tokenValue = 0

	for log in receipt['logs']:
		if log['topics'][0] == TOPIC_ERC20TRANSFER:
			tokenFrom = '0x'+log['topics'][1][26:].lower()
			tokenTo = '0x'+log['topics'][2][26:].lower()
			tokenaddr = log['address']
			tokenValue = int(log['data'][2:], 16)

	if csvsymbol == ETH:

		if not ethFrom in HWG_ADDRS:
			raise Exception('ERROR '+csvtxid+' ethFrom('+ethFrom+')!='+str(HWG_ADDRS))
		if ethTo != csvretaddr:
			raise Exception('ERROR '+csvtxid+' ethTo!='+csvretaddr)
		if ethValue != int(csvamount):
			raise Exception('ERROR '+csvtxid+' ethValue('+ethValue+')!='+csvamount)
		if tokenValue > 0:
			raise Exception('ERROR '+csvtxid+' tokenValue>0')

	else:

		checkToken(tokenaddr,csvsymbol)

		if not tokenFrom in HWG_ADDRS:
			raise Exception('ERROR '+csvtxid+' tokenFrom('+tokenFrom+')!='+str(HWG_ADDRS))
		if tokenTo != csvretaddr:
			raise Exception('ERROR '+csvtxid+' tokenTo('+tokenTo+')!='+csvretaddr)
		if tokenValue != int(csvamount):
			raise Exception('ERROR '+csvtxid+' tokenValue('+str(tokenValue)+')!='+csvamount)
		if ethValue > 0:
			raise Exception('ERROR '+csvtxid+' ethValue>0')

	print "+ transfer to "+csvretaddr+" "+format(int(csvamount),csvsymbol)
	tokens[csvsymbol]['sum']+=int(csvamount)

content = urllib.urlopen(CSVURL).read()
csvlines = content.split('\r\n')
del csvlines[0]

for line in csvlines:
	[oldaddr,newaddr,retaddr,amount,symbol,txid,fromaddr] = line.split(",")
	check(oldaddr,newaddr,retaddr,amount,symbol,txid,fromaddr)

for symbol in tokens:
	print "TOTAL "+format(tokens[symbol]['sum'],symbol)

