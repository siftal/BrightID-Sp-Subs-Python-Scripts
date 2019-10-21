from . import utils
from . import config


def sp_price():
    func = utils.contracts['sp_minter'].functions.price()
    price = utils.send_eth_call(func)
    return price


def owner():
    func_owner = utils.contracts['sp_minter'].functions.owner()
    owner = utils.send_eth_call(func_owner)
    return owner


def finance():
    func_finance = utils.contracts['sp_minter'].functions.finance()
    finance = utils.send_eth_call(func_finance)
    return finance


def set_purchase_token(private_key, addr):
    addr = utils.w3.toChecksumAddress(addr)
    func = utils.contracts['sp_minter'].functions.setPurchaseToken(addr)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


def set_finance(private_key, addr):
    addr = utils.w3.toChecksumAddress(addr)
    func = utils.contracts['sp_minter'].functions.setFinance(addr)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


def set_price(private_key, price):
    func = utils.contracts['sp_minter'].functions.setPrice(int(price))
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


def purchase(private_key, amount):
    utils.approve(
        config.ADDRESSES['sp_minter'], 'f_dai', amount, private_key)
    func = utils.contracts['sp_minter'].functions.purchase()
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


def reclaim(private_key, token_addr):
    func = utils.contracts['sp_minter'].functions.reclaimTokens(token_addr)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


def transfer_ownership(private_key, account):
    func = utils.contracts['sp_minter'].functions.transferOwnership(account)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


def remove_minter(private_key):
    func = utils.contracts['sp_minter'].functions.renounceMinterRole()
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash
