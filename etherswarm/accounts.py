from etherswarm.utils import env
from hashlib import sha256
import web3
from etherswarm.provider import provider as P


def privates(num: int, seed=env("SK_SEED")) -> bytes:
    if type(seed) is not bytes:
        seed = seed.encode()
    n = str(num).encode()
    return sha256(sha256(seed + n).digest() + n).digest()


def accounts(num: int):
    return web3.eth.Account.privateKeyToAccount(privates(num))


def list_accounts(s, e):
    ret = []
    for i in range(s, e):
        ret.append((i, accounts(i).address, get_balance(i)))
    return ret

def get_balance(num):
    return float(P.fromWei(P.eth.getBalance(accounts(num).address), "ether"))