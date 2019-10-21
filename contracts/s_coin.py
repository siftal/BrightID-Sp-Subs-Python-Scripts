from . import utils


def totalSupply():
    func_totalSupply = utils.contracts['s_coin'].functions.totalSupply()
    totalSupply = utils.send_eth_call(func_totalSupply)
    return totalSupply


def balance(account):
    account = utils.w3.toChecksumAddress(account)
    func = utils.contracts['s_coin'].functions.balanceOf(account)
    result = utils.send_eth_call(func, account)
    return result


def mint(private_key, account, amount):
    account = utils.w3.toChecksumAddress(account)
    amount = int(amount * 10**18)
    func = utils.contracts['s_coin'].functions.mint(account, amount)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


def transfer(private_key, recipient, amount):
    func = utils.contracts['s_coin'].functions.transfer(recipient, amount)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash
