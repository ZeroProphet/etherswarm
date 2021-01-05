import os
import web3
from etherswarm.contract import load_contract

FACTORY = load_contract(
    "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
    "%s/abis/IUniswapV2Factory.json" % os.path.dirname(__file__)
)


ROUTER = load_contract(
    "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
    "%s/abis/IUniswapV2Router02.json" % os.path.dirname(__file__)
)

def as_erc20(addr):
    return load_contract(addr, "%s/abis/ERC20.json" % os.path.dirname(__file__))


class ERC20:
    def __init__(self, addr):
        addr = web3.Web3.toChecksumAddress(addr)
        self.token = as_erc20(addr)

    def __getattr__(self, name):
        if hasattr(self.token, name):
            return getattr(self.token, name)
        else:
            raise AttributeError

    def __repr__(self):
        return "<ERC20 %s>" % self.token.address

    @property
    def decimals(self):
        if not hasattr(self, "_decimals"):
            self._decimals = self.token.functions.decimals().call()
        return self._decimals


class Pair:
    def __init__(self, addr_0, addr_1):
        addr_0 = web3.Web3.toChecksumAddress(addr_0)
        addr_1 = web3.Web3.toChecksumAddress(addr_1)
        pair_addr = FACTORY.functions.getPair(addr_1, addr_0).call()
        self.pair = load_contract(pair_addr, "%s/abis/IUniswapV2Pair.json" % os.path.dirname(__file__))
        self.path = [self.token0.address, self.token1.address]

    @property
    def token0(self):
        if not hasattr(self, "_token0"):
            addr = self.pair.functions.token0().call()
            self._token0 = ERC20(addr)
        return self._token0

    @property
    def token1(self):
        if not hasattr(self, "_token1"):
            addr = self.pair.functions.token1().call()
            self._token1 = ERC20(addr)
        return self._token1

    @property
    def ask_price(self):
        return ROUTER.functions.getAmountsOut(
            1 * 10 ** self.token0.decimals,
            self.path[::-1]
        ).call()[-1] / (10 ** self.token1.decimals)

    @property
    def bid_price(self):
        return ROUTER.functions.getAmountsOut(
            1 * 10 ** self.token0.decimals,
            self.path
        ).call()[-1] / (10 ** self.token1.decimals)

    def ask(self, amount, cid, ttl=5, rate=0.01, speed="standard"):
        tx = uniswap.ROUTER.functions.swapExactTokensForTokens(
            int(amount * 10 ** self.token0.decimals),
            int(amount * self.ask_price * (1-rate) * 10 ** self.token1.decimals),
            self.path[::-1],
            accounts(cid).address,
            int(time.time() + (ttl * 60))
        ).buildTransaction({
            "from": accounts(cid).address,
            "chainId": 1,
            "nonce": P.eth.getTransactionCount(accounts(cid).address),
            'gas': 2000,
            "value": 0,
            "gasPrice": gasPrice(speed)
        })
        return send(sign(tx, cid)).hex()


    def bid(self, amount, cid, ttl=5, rate=0.01, speed="standard"):
        tx = uniswap.ROUTER.functions.swapExactTokensForTokens(
            int(amount * 10 ** self.token1.decimals),
            int(amount * self.bid_price * (1-rate) * 10 ** self.token0.decimals),
            self.path,
            accounts(cid).address,
            int(time.time() + (ttl * 60))
        ).buildTransaction({
            "from": accounts(cid).address,
            "chainId": 1,
            "nonce": P.eth.getTransactionCount(accounts(cid).address),
            'gas': 2000,
            "value": 0,
            "gasPrice": gasPrice(speed)
        })
        return send(sign(tx, cid)).hex()
