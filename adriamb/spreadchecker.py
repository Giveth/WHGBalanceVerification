import web3
import eth_utils
import solc
import time
import urllib
import re
import locale
import sys
import yaml

erc20decimals = {
	'eth'  : 18, 'fst'  : 18, 'gno'  : 18, 'crb'  : 8,
	'icn'  : 18, 'fun'  : 8,  'ndc'  : 18, 'storj': 8,
	'gnt'  : 18, 'bnt'  : 18, 'rlc'  : 9,  'gup'  : 3,
	'dgd'  : 9,  'trst' : 6,  'wings': 18, 'mtl'  : 8,
	'pay'  : 18, 'cat'  : 18, 'swt'  : 18, 'cfi'  : 18,
	'cvc'  : 8,  'bat'  : 18, 'dice' : 16, 'eos'  : 18,
	'mln'  : 18, 'rep'  : 18, 'mco'  : 8
}

ETH_TOKEN           = 'eth'
HWG_ADDR            = '0x1dba1131000664b884a1ba238464159892252d3a'
TOPIC_ERC20TRANSFER = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
NEWMULTISIG_SHA3    = '0x92a0d09eb2bae4c35688dfce7de824fe4683e3ec8fb22f30c7e8035f5223a4c9'
OLDMULTISIG_SHA3    = '0x793e18e375582d7b3bdee748fcc58ff89d79913bef9b55070f2f96b29ed99245'

web3 = web3.Web3(web3.HTTPProvider('http://localhost:8546'))

def readTokensFromPage1(csvUrlPage1):

	checkedoldwallets = {}
	checkednewwallets = {}
	newwalletof = {}
	uniquetrnid = {}

	tokens = {}
	content = urllib.urlopen(csvUrlPage1).read()
	csvlines = content.split('\r\n')
	del csvlines[0]
	for line in csvlines:
	   	[_return,_amount,_tokensym,_token,_old,_new] = line.split(",")

		_tokensym = _tokensym.strip().lower()

	   	if not _tokensym in tokens:
	   		tokens[_tokensym] = _token
	   	#	if web3.eth.getCode(_token)<3:
	   	#		print "Bad code in TOKEN "+_tokensym+" "+_token
	   	else:
	   		if tokens[_tokensym] != _token:
	   			print "Mistake in TOKEN "+_tokensym+" "+tokens[_tokensym]+" "+_token

	   	#if not _new in checkednewwallets:
		#   	if not web3.sha3(web3.eth.getCode(_new)) == NEWMULTISIG_SHA3:
		#   		raise Exception(_new+": new contract has bad bash")
		#	checkednewwallets[_new]=1

	   	#if not _old in checkedoldwallets:
		#	code = web3.eth.getCode(_old)
	   	#	sha3 = web3.sha3(code)
		#	if code != '0x' and sha3 != OLDMULTISIG_SHA3:
		#		raise Exception(_old+": new contract has bad bash "+sha3)
		#	checkedoldwallets[_old]=1

		if not _old in newwalletof:
			newwalletof[_old] = _new
		else:
			if newwalletof[_old] != _new:
		   		raise Exception(_old+": has two different new wallets")

		trnid = _old + _new + _token + _tokensym
		if not trnid in uniquetrnid:
			uniquetrnid[trnid] = 1
		else:
			raise Exception(trnid+": already exists")

	return tokens


def checkAddrFormat(addr):

	if not re.search('^0x[0-9a-f]{40}$',addr):
		raise Exception("invalid address "+addr)

def checkTransfer(transfer):

 	if not transfer['tokensym'] in tokens:
		raise Exception("Token "+transfer['tokensym']+"' not known.")

	if len(transfer['return'])>0 and len(transfer['txid'])<10:
		isnormalized = eth_utils.is_normalized_address(transfer['return'])
		ischecksum   = eth_utils.is_checksum_address(transfer['return'])

	#	if not isnormalized and not ischecksum:
	#		print "ERROR BadAddess "+transfer['return']
	#	elif isnormalized and not ischecksum:
	#		print "WARN NotChecksumed "+transfer['return']

		balance = web3.eth.getBalance(transfer['return'])
		if balance == 0:
			print "WARN ReturnAddr "+transfer['return']+" has "+str(balance)+" eth"

	if len(transfer['return'])>0 and len(transfer['txid'])>10:

   		tokenFrom = 0
   		tokenTo = "0x"
   		token = "NONE"
   		tokenValue = 0

   		# get ERC20 transfer and amount
		receipt = web3.eth.getTransactionReceipt(transfer['txid'])
		if receipt is None:
			print "TXID recipt "+transfer['txid']+" is not ready"
			time.sleep(1)
			checkTransfer(transfer)
			return

		for log in receipt['logs']:
			if log['topics'][0] == TOPIC_ERC20TRANSFER:
				tokenFrom = '0x'+log['topics'][1][26:].lower()
				checkAddrFormat(tokenFrom)
				tokenTo = '0x'+log['topics'][2][26:].lower()
				checkAddrFormat(tokenTo)
				token = log['address']
				tokenValue = int(log['data'][2:], 16)

   		# get ETH transfer value and amount
		tx = web3.eth.getTransaction(transfer['txid'])
		if tx is None:
			print "TXID "+transfer['txid']+" is not ready"
			time.sleep(1)
			checkTransfer(transfer)
			return

		ethFrom = tx['from']
		ethTo = tx['to']
		ethValue = tx['value']

		block = web3.eth.getBlock(receipt['blockNumber'])
		timestamp = int(block['timestamp'])
		elapsed = str(round((time.time() - timestamp)/60))

		# check transfers from HWG_ADDR to destination
		if transfer['tokensym'] == ETH_TOKEN:
	   		if ethFrom != HWG_ADDR:
	   			print 'WARN '+transfer['txid']+' tokenTo!='+transfer['token']
	   		if ethTo != transfer['return']:
	   			print 'WARN '+transfer['txid']+' ethTo!='+transfer['return']
	   		if ethValue != int(transfer['amount']):
	   			print 'WARN '+transfer['txid']+' ethValue('+ethValue+')!='+transfer['amount']
	   		if tokenValue > 0:
	   			print 'WARN '+transfer['txid']+' tokenValue>0'
	   		print elapsed+"m ago\t> "+transfer['return']+" "+ \
	   			"{:,}".format(ethValue/1000000000000000000.0)+" ETH"
	   	else:
	   		decimals = erc20decimals[transfer['tokensym']]

	   		if tokenFrom != HWG_ADDR:
	   			print 'WARN '+transfer['txid']+' tokenFrom!='+HWG_ADDR
	   		if token != tokens[transfer['tokensym']]:
	   			print 'WARN '+transfer['txid']+' token!='+tokens[transfer['tokensym']]
	   		if tokenTo != transfer['return']:
	   			print 'WARN '+transfer['txid']+' tokenTo('+tokenTo+')!='+transfer['return']
	   		if tokenValue != int(transfer['amount']):
	   			print 'WARN '+transfer['txid']+' tokenValue('+str(tokenValue)+')!='+transfer['amount']
			if ethValue > 0:
				print 'WARN '+transfer['txid']+' ethValue>0'
	   		print elapsed+"m ago\t> "+transfer['return']+" "+\
	   			"{:,}".format(int(transfer['amount'])/float(pow(10,decimals)))+\
	   			" "+transfer['tokensym'].upper()+" d="+str(decimals)


def checkTransfers(csvUrlPage2,returnaddr):

	content = urllib.urlopen(csvUrlPage2).read()
	csvlines = content.split('\r\n')
	del csvlines[0]

	transfers = []

	for line in csvlines:

		if '"' in line:
			spl = line.split('"')
			line = spl[0]+spl[2]

		[_return,_amount,_tokensym,_tokenpric,_txid,_onwer,_comments,_value,_extra] = line.split(",")
		transfers.append({
	       'return':_return.strip(),
	       'amount':_amount.strip().lower(),
	       'tokensym':_tokensym.strip().lower(),
	       'txid':_txid.strip().lower()
	    })

	for transfer in transfers:
		if len(returnaddr)==0 or transfer['return']==returnaddr:
			checkTransfer(transfer)

with open(".spreadchecker.yaml", 'r') as stream:
    config = yaml.load(stream)
    tokens = readTokensFromPage1(config['csvpage1'])
    if len(sys.argv) == 2:
	    checkTransfers(config['csvpage2'],sys.argv[1])
    else:
	    checkTransfers(config['csvpage2'],"")

