from . import utils


def tokenInfo():
    func_name = utils.contracts['sp'].functions.name()
    name = utils.send_eth_call(func_name)

    func_symbol = utils.contracts['sp'].functions.symbol()
    symbol = utils.send_eth_call(func_symbol)

    decimals_symbol = utils.contracts['sp'].functions.decimals()
    decimals = utils.send_eth_call(decimals_symbol)

    return {'name': name, 'symbol': symbol, 'decimals': decimals}


def owner():
    func_owner = utils.contracts['sp'].functions.owner()
    owner = utils.send_eth_call(func_owner)
    return owner


def finance():
    func_finance = utils.contracts['sp'].functions.finance()
    finance = utils.send_eth_call(func_finance)
    return finance


def total_supply():
    func_total_supply = utils.contracts['sp'].functions.totalSupply()
    total_supply = utils.send_eth_call(func_total_supply)
    return total_supply


def balance(account):
    account = utils.w3.toChecksumAddress(account)
    func = utils.contracts['sp'].functions.balanceOf(account)
    result = utils.send_eth_call(func, account)
    return result


def unassigned_balance(account):
    func = utils.contracts['sp'].functions.unassignedBalance(account)
    balance = utils.send_eth_call(func, account)
    return balance


def context_balance(account, contextName):
    b_contextName = utils.str2bytes32(contextName)
    func = utils.contracts['sp'].functions.contextBalance(
        account, b_contextName)
    balance = utils.send_eth_call(func)
    return balance


def total_context_balance(contextName):
    b_contextName = utils.str2bytes32(contextName)
    func = utils.contracts['sp'].functions.totalContextBalance(
        b_contextName)
    balance = utils.send_eth_call(func)
    return balance


def mint(private_key, account, amount):
    account = utils.w3.toChecksumAddress(account)
    func = utils.contracts['sp'].functions.mint(account, amount)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


def set_finance(private_key, addr):
    addr = utils.w3.toChecksumAddress(addr)
    func = utils.contracts['sp'].functions.setFinance(addr)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


def assign_context(private_key, contextName, amount):
    b_contextName = utils.str2bytes32(contextName)
    func = utils.contracts['sp'].functions.assignContext(
        b_contextName, amount)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


def is_minter(account):
    func = utils.contracts['sp'].functions.isMinter(account)
    flag = utils.send_eth_call(func)
    return flag


def add_minter(private_key, account):
    func = utils.contracts['sp'].functions.addMinter(account)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


def remove_minter(private_key):
    func = utils.contracts['sp'].functions.renounceMinter()
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


def transfer_ownership(private_key, account):
    func = utils.contracts['sp'].functions.transferOwnership(account)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash


def reclaim(private_key, token_addr):
    func = utils.contracts['sp'].functions.reclaimTokens(token_addr)
    tx_hash = utils.send_transaction(func, 0, private_key)
    return tx_hash
