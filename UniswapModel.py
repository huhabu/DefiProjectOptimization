import numpy as np

class Tick:
    def __init__(self, prev, next, idx, grossL, netL, decimal0, decimal1):
        self.idx = idx
        self.val = np.sqrt(pow(1.0001, idx) / 10**(decimal1 - decimal0))
        self.prev = np.sqrt(pow(1.0001, prev))
        self.next = np.sqrt(pow(1.0001, next))
        self.grossL = grossL / 10**((decimal0 + decimal1)/2)
        self.netL = netL / 10**((decimal0 + decimal1)/2)

    def __repr__(self):
        return f"Idx: {self.idx}, Val: {self.val}, Prev: {self.prev}, Next: {self.next}, GrossL: {self.grossL}, NetL: {self.netL}"
            
class UniswapModel:
    def __init__(self, liquidity_concentration, sqrtPrice, liquidity, curTick, fee=0.003):
        self.liquidity_concentration = liquidity_concentration
        self.sqrtPrice = sqrtPrice
        self.liquidity = liquidity
        self.tick = curTick
        self.fee = fee
        
    def amount_out(self, deltaX):
        liquidity = self.liquidity
        sqrtPrice = self.sqrtPrice
        tick = self.tick
        virtualX = liquidity/sqrtPrice
        tickX = liquidity/self.liquidity_concentration[tick].prev-virtualX
        deltaY = 0
        while deltaX > tickX:
            virtualY = liquidity**2/virtualX
            deltaX -= tickX
            sqrtPrice = self.liquidity_concentration[tick].prev
            tick -= 1
            virtualX = liquidity/sqrtPrice
            deltaY += virtualY - liquidity**2/virtualX
            liquidity -= self.liquidity_concentration[tick].netL
            
        virtualX += deltaX
        virtualY = liquidity**2/virtualX
        deltaY += virtualY - liquidity**2/virtualX