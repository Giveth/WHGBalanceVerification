from main import Client, TokenHolder

# Test transfer for token data
#https://etherscan.io/tx/0x18da4595227551470aa625a8e909649f28bfa2a2879efa48b56dc672ff6de352


def test_token_movement_detection():
    tokens = TokenHolder('tokens.json')
    c = Client(tokens)
    tx = c.get_transaction('18da4595227551470aa625a8e909649f28bfa2a2879efa48b56dc672ff6de352'.decode('hex'))
    eth_sent_to, wei, token_value = c.decode_execute(tx['input'])
    assert token_value == 78550342580000000000
