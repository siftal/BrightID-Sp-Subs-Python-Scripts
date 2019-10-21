from . import utils
from . import config
from . import purchase_token


def subs_price():
    func = utils.contracts['subs_minter'].functions.price()
    price = utils.send_eth_call(func)
    return price


def owner():
    func_owner = utils.contracts['subs_minter'].functions.owner()
    owner = utils.send_eth_call(func_owner)
    return owner


def finance():
    func_finance = utils.contracts['subs_minter'].functions.finance()
    finance = utils.send_eth_call(func_finance)
    return finance


def set_finance(private_key, addr):
    addr = utils.w3.toChecksumAddress(addr)
    func = utils.contracts['subs_minter'].functions.setFinance(addr)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


def purchase(private_key, fdai_amount):
    utils.approve(
        config.ADDRESSES['subs_minter'], 'f_dai', fdai_amount, private_key)
    allowance = purchase_token.allowance(utils.priv2addr(
        private_key), config.ADDRESSES['subs_minter'])
    print('allowance amount: ', allowance / 10**18)
    func = utils.contracts['subs_minter'].functions.purchase()
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


def reclaim(private_key, token_addr):
    func = utils.contracts['subs_minter'].functions.reclaimTokens(token_addr)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


def transfer_ownership(private_key, account):
    func = utils.contracts['subs_minter'].functions.transferOwnership(account)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


def remove_minter(private_key):
    func = utils.contracts['subs_minter'].functions.renounceMinterRole()
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


def claim(private_key):
    func = utils.contracts['subs_minter'].functions.claim()
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash
