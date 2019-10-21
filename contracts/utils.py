import os
import sys
from eth_keys import keys
from web3 import Web3, HTTPProvider
from . import config
# from web3.auto import w3


def get_contracts():
    global contracts
    contracts = {
        's_coin':
        w3.eth.contract(
            address=config.ADDRESSES['s_coin'], abi=config.ABIES['s_coin']),
        'f_dai':
        w3.eth.contract(
            address=config.ADDRESSES['f_dai'], abi=config.ABIES['f_dai']),
        'sp_minter':
        w3.eth.contract(
            address=config.ADDRESSES['sp_minter'],
            abi=config.ABIES['sp_minter']),
        'sp':
        w3.eth.contract(
            address=config.ADDRESSES['sp'],
            abi=config.ABIES['sp']),
        'subs_minter':
        w3.eth.contract(
            address=config.ADDRESSES['subs_minter'],
            abi=config.ABIES['subs_minter']),
        'subs':
        w3.eth.contract(
            address=config.ADDRESSES['subs'],
            abi=config.ABIES['subs'])
    }
    return contracts


def approve(spender, token, amount, private_key):
    # print('Approving {0} {1} transfer from your account by the contract'.
    #       format(amount, token))
    spender = w3.toChecksumAddress(spender)
    func = contracts[token].functions.approve(spender, int(amount * 10**18))
    tx_hash = send_transaction(func, 0, private_key)
    rec = w3.eth.waitForTransactionReceipt(tx_hash['tx_hash'])
    print('approve', {'status': rec['status'], 'tx_hash': tx_hash['tx_hash']})
    return {'status': rec['status'], 'tx_hash': tx_hash}


def send_erc20(receiver, token, amount, private_key):
    # print('Sending {0} {1} to {2}'.
    #       format(amount, token))
    receiver = w3.toChecksumAddress(receiver)
    func = contracts[token].functions.send(receiver, int(amount * 10**18))
    tx_hash = send_transaction(func, 0, private_key)
    rec = w3.eth.waitForTransactionReceipt(tx_hash)
    return {'status': rec['status'], 'tx_hash': tx_hash}


def send_eth(receiver, amount, private_key):
    # print('Send {0} Eth to {1}'.
    #       format(amount, receiver))
    receiver = w3.toChecksumAddress(receiver)
    signed_txn = w3.eth.account.signTransaction(
        dict(
            nonce=w3.eth.getTransactionCount(priv2addr(private_key)),
            gasPrice=w3.eth.gasPrice,
            gas=100000,
            to=receiver,
            value=Web3.toWei(amount, 'ether')
        ),
        private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    rec = w3.eth.waitForTransactionReceipt(tx_hash)
    return {'status': rec['status'], 'tx_hash': tx_hash}


def eth_balance(account):
    balance = w3.eth.getBalance(account)
    return balance


def check_account(ctx, param, value):
    if not value and 'CROWDSALE_PRIVATEKEY' in os.environ:
        value = os.environ['CROWDSALE_PRIVATEKEY']
    if not value:
        print(
            'Run:\n\texport CROWDSALE_PRIVATEKEY="your ethereum private key"')
        sys.exit()
    if value.startswith('0x'):
        value = value[2:]
    return value


def priv2addr(private_key):
    pk = keys.PrivateKey(bytes.fromhex(private_key))
    return pk.public_key.to_checksum_address()


def send_transaction(func, value, private_key):
    transaction = func.buildTransaction({
        'nonce':
        w3.eth.getTransactionCount(priv2addr(private_key)),
        'from':
        priv2addr(private_key),
        'value':
        value,
        'gas':
        config.GAS,
        'gasPrice':
        config.GAS_PRICE
    })
    signed = w3.eth.account.signTransaction(transaction, private_key)
    raw_transaction = signed.rawTransaction.hex()
    tx_hash = w3.eth.sendRawTransaction(raw_transaction).hex()
    rec = w3.eth.waitForTransactionReceipt(tx_hash)
    return {'status': rec['status'], 'tx_hash': tx_hash}

    # if rec['status']:
    #     print('tx: {}'.format(tx_hash))
    # else:
    #     print('Reverted!\nError occured during contract execution')
    #     print(rec)
    # return tx_hash


def send_eth_call(func, sender=None):
    if not sender:
        sender = current_user()
    result = func.call({
        'from': sender,
    })
    return result


def current_user():
    return priv2addr(config.pk1)


def str2bytes32(s):
    assert len(s) <= 32
    padding = (2 * (32 - len(s))) * '0'
    return (bytes(s, 'utf-8')).hex() + padding


def start():
    global contracts, w3
    w3 = Web3(HTTPProvider(config.INFURA_URL))
    get_contracts()


# we are initalizing some variables here
contracts = w3 = None
start()

# FIXME: infura not supports filtering of events.
# Here we are hacking web3.py filters to use getLogs rpc endpoint instead.


def dummy(*args, **argsdic):
    if len(args) > 0 and args[0] == 'eth_newFilter':
        return 0
    else:
        return original_request_blocking(*args, **argsdic)


original_request_blocking = w3.manager.request_blocking
w3.manager.request_blocking = dummy
