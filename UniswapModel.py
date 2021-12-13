class UniswapModel:
    def __init__(self, L, pb, pa, x, y):
        self.L = L
        self.pb = pb
        self.pa = pa
        self.x = x
        self.y = y
        
    def cost(self, amount_in):