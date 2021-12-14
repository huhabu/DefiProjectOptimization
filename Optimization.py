from scipy.optimize import minimize
from UniswapModel import UniswapModel
from CurveModel import CurveModel
from SushiswapModel import SushiswapModel

class Optimization:
    """
    We are given 3 DeFi exchanges, each with a different AMM formula. We want to achieve a return of y,
    which is provided as input to the user. We want to find the least amount of x we can sell to achieve
    y. So, we want to minimize x_1 + x_2 + x_3 given that AMM_return_1(x_1) + AMM_return_2(x_2) + AMM_return_3(x_3) = y
    """

    def __init__(self, curve, sushi, uniswap, y):
        self.curve = curve
        self.sushi = sushi
        self.uniswap = uniswap
        self.y = y
    
    """
    We are attempting to minimize the amount of token that we require
    """
    def cost_function(self, arr):
        return arr[0] + arr[1] + arr[2]

    """
    We ensure that x1, x2, and x3 sum to our desired return
    """
    def constraint1(self, arr):
        return self.curve(arr[0]) + self.sushi(arr[1]) + self.uniswap(arr[2]) - self.y

    """
    We ensure that the system paramters are positive
    """
    def contraint2(self, arr):
        return arr[0]

    def contraint3(self, arr):
        return arr[1]

    def contraint4(self, arr):
        return arr[2]


    """
    Use scipy's minimize function with the given constraints and objective function to find the best x1, x2, x3
    """
    def optimize_cost(self):

        # our starting guess
        x0 = [1, 1, 1]

        # A dictionary of the contraints
        constraints = ({'type': 'eq', 'fun': self.constraint1},
        {'type': 'ineq',
       'fun': self.constraint2},
       {'type': 'ineq',
       'fun': self.contstraint3},
       {'type': 'ineq',
       'fun': self.constraint4},)

        res = minimize(self.cost_function, x0, constraints=constraints, method='SLSQP')
        return res

"""
main entry point for program
"""
def main():
    curve = CurveModel() # add arguments
    curve = curve.amount_out
    uniswap = UniswapModel() # add arguments
    uniswap = uniswap.amount_out
    sushi = SushiswapModel() # add arguments
    sushi = sushi.amount_out

    DESIRED_RETURN = 20
    optimization = Optimization(curve, sushi, uniswap, DESIRED_RETURN)
    print(optimization.optimize_cost())

if __name__ == "__main__": main()
