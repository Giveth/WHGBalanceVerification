import json
import csv
import string

from ethereum.abi import ContractTranslator, decode_abi
from pyethapp.rpc_client import JSONRPCClient
from pyethapp.jsonrpc import quantity_encoder

from constants import wallet_abi, results_file, BIG_WHITEHAT, SMALL_WHITEHATS

host = "127.0.0.1"
port = 8545
printable = set(string.printable)


class TokenHolder():

    def __init__(self, filename):
        self.tokens = self.load_tokens(filename)

    def load_tokens(self, filename):
        with open(filename, 'r') as f:
            tokens = json.loads(f.read())

        self.tokens_list = tokens
        cleaned_tokens = dict()
        for token in tokens:
            cleaned_tokens[token['address'].lower()] = token

        return cleaned_tokens

    def address_is_token(self, address):
        if not address.startswith('0x'):
            address = '0x' + address

        address = address.lower()
        token_name = None
        if address in self.tokens:
            token_name = self.tokens[address]['symbol']

        return token_name


def address_is_whitehat(address):
    if not address.startswith('0x'):
        address = '0x' + address

    if address == BIG_WHITEHAT:
        return 'BIG_WHITEHAT'
    if address in SMALL_WHITEHATS:
        return 'SMALL_WHITEHATS'

    return None


class Mapping():

    def __init__(self, tokens):
        self.big_mapping = dict()
        self.small_mapping = dict()
        self.tokens = tokens

    def _add_eth(self, mapping, address, value):
        if address not in mapping:
            mapping[address] = dict()
            mapping[address]['ether'] = value
        else:
            mapping[address]['ether'] = mapping[address]['ether'] + value

    def _add_token(self, mapping, address, token_address, value):
        if not token_address.startswith('0x'):
            token_address = '0x' + token_address
        if address not in mapping:
            mapping[address] = dict()
            mapping[address][token_address] = value
        else:
            prev_value = mapping[address].get(token_address, 0)
            mapping[address][token_address] = prev_value + value

    def add_eth(self, target, address, value):
        if target == 'BIG_WHITEHAT':
            self._add_eth(self.big_mapping, address, value)
        elif target == 'SMALL_WHITEHATS':
            self._add_eth(self.small_mapping, address,  value)
        else:
            raise ValueError('Unknown whitehat type: {}'.format(target))

    def add_token(self, target, address, token_address, value):
        if target == 'BIG_WHITEHAT':
            self._add_token(self.big_mapping, address, token_address, value)
        elif target == 'SMALL_WHITEHATS':
            self._add_token(self.small_mapping, address, token_address, value)
        else:
            raise ValueError('Unknown whitehat type: {}'.format(target))

    def _output_to_csv(self, name, mapping):
        with open(name, 'wb') as f:
            w = csv.writer(f)
            header_row = ['multisig_address', 'amount_in_wei']
            for token_data in self.tokens.tokens_list:
                # need to get rid of unicode chars in some token symbols.
                header_row.append(filter(
                    lambda x: x in printable, token_data['symbol']
                ))

            w.writerow(header_row)
            data = list()
            for multisigaddress, map_data in mapping.iteritems():
                entry = [multisigaddress, map_data.get('ether', 0)]
                for token_data in self.tokens.tokens_list:
                    token_address = token_data['address'].lower()
                    if token_address in mapping[multisigaddress]:
                        # No need to calculate decimal value
                        value = mapping[multisigaddress][token_address]
                        entry.append(value)
                    else:
                        entry.append(0)
                data.append(tuple(entry))

            # sort by ETH value
            sorted_data = sorted(data, key=lambda tup: tup[1], reverse=True)
            w.writerows(sorted_data)

    def output_to_csv(self, name):
        self._output_to_csv('big_' + name, self.big_mapping)
        self._output_to_csv('small_' + name, self.small_mapping)


class Client():

    def __init__(self, tokens):
        self.client = JSONRPCClient(
            privkey=None,
            host=host,
            port=port,
            print_communication=False,
        )
        self.wallet_translator = ContractTranslator(wallet_abi)
        self.tokens = tokens

    def get_block(self, num):
        return self.client.call(
            'eth_getBlockByNumber',
            quantity_encoder(num),
            True
        )

    def get_transaction(self, hash):
        return self.client.eth_getTransactionByHash(hash)

    def decode_token_transfer(self, txdata, to_address):
        if len(txdata) < 8 or txdata[:8] != 'a9059cbb':
            return None

        # get rid of signature
        txdata = txdata[8:]

        # here we got ourselves a token transfer
        # transfer(address _from, uint256 _value)
        token_name = self.tokens.address_is_token(to_address)
        if token_name is None:
            print('WARNING: Unknown token {} transferred'.format(to_address))
            token_name = 'UNKNOWN'

        hexdata = txdata.decode('hex')
        transfer_to = decode_abi(['address'], hexdata[:32])[0]
        transfer_value = decode_abi(['uint256'], hexdata[32:])[0]

        if address_is_whitehat(transfer_to) is None:
            print('WARNING: {} token sent to non-whitehat address?'.format(token_name))

        return transfer_value

    def decode_execute(self, txdata):
        # get rid of signature and 0x
        txdata = txdata[10:]

        # unfortunately the pyethapp way does not work
        # fndata = c.wallet_translator.function_data['execute']
        # return decode_abi(fndata['encode_types'], txdata.decode('hex'))

        # ... but decoding each arg individually does work
        sent_to = decode_abi(['address'], txdata.decode('hex')[:32])[0]
        amount_in_wei = decode_abi(['uint256'], txdata.decode('hex')[32:64])[0]

        token_value = self.decode_token_transfer(txdata[256:], sent_to)

        return sent_to, amount_in_wei, token_value


if __name__ == "__main__":
    tokens = TokenHolder('tokens.json')
    c = Client(tokens)
    mapping = Mapping(tokens)

    start_block = 4044976
    end_block = 4048770
    blocknum = start_block
    print('Verification Started')
    while blocknum <= end_block:
        print('Processing block: {}'.format(blocknum))

        transactions = c.get_block(blocknum)['transactions']
        for tx in transactions:
            whitehat_type = address_is_whitehat(tx['from'])
            is_whitehat_execute = (
                whitehat_type is not None and
                tx['input'].startswith('0xb61d27f6')
            )
            if is_whitehat_execute:
                sent_to, wei, token_value = c.decode_execute(tx['input'])
                if token_value is None:
                    mapping.add_eth(whitehat_type, tx['to'], wei)
                else:
                    mapping.add_token(
                        whitehat_type,
                        tx['to'],
                        sent_to,
                        token_value
                    )

        blocknum += 1

    mapping.output_to_csv(results_file)
    print('Verification ended. Written files: big_{} and small_{}'.format(
        results_file, results_file)
    )
