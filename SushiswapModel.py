class SushiswapModel:
    def __init__(self, K, y, x):
        self.K = K
        self.y = y
        self.x = x
        
    def cost(self, amount_in):
        return self.y - (self.K / (self.x + amount_in))


