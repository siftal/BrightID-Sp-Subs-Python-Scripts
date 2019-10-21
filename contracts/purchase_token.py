from . import utils
from . import config


def totalSupply():
    func_totalSupply = utils.contracts['f_dai'].functions.totalSupply()
    totalSupply = utils.send_eth_call(func_totalSupply)
    return totalSupply


def balance(account):
    account = utils.w3.toChecksumAddress(account)
    func = utils.contracts['f_dai'].functions.balanceOf(account)
    result = utils.send_eth_call(func, account)
    return result


def mint(private_key, account, amount):
    account = utils.w3.toChecksumAddress(account)
    amount = int(amount * 10**18)
    func = utils.contracts['f_dai'].functions.mint(account, amount)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


def allowance(owner, spender):
    func = utils.contracts['f_dai'].functions.allowance(owner, spender)
    allowance = utils.send_eth_call(func)
    return allowance