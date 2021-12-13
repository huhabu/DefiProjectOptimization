from scipy.optimize import minimize

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
    def cost_function(arr):
        return arr[0] + arr[1] + arr[2]

    """
    We ensure that x1, x2, and x3 sum to our desired return
    """
    def constraint1(arr):
        return self.curve(arr[0]) + self.sushi(arr[1]) + self.uniswap(arr[2]) - self.y

    """
    We ensure that the system paramters are positive
    """
    def contraint2(arr):
        return arr[0]

    def contraint3(arr):
        return arr[1]

    def contraint4(arr):
        return arr[2]


    """
    Use scipy's minimize function with the given constraints and objective function to find the best x1, x2, x3
    """
    def optimize_cost():

        # our starting guess
        x0 = [1, 1, 1]

        # A dictionary of the contraints
        constraints = ({'type': 'eq', 'fun': constraint1},
        {'type': 'ineq',
       'fun': constraint2},
       {'type': 'ineq',
       'fun': contstraint3},
       {'type': 'ineq',
       'fun': constraint4},)

        res = minimize(cost_function, x0, constraints=constraints, method='SLSQP')
        return res

"""
main entry point for program
"""
def main():
    curve = CurveModel() # add arguments
    curve = curve.cost
    uniswap = UniswapModel() # add arguments
    uniswap = uniswap.cost
    sushi = SushiswapModel() # add arguments
    sushi = sushi.cost

    DESIRED_RETURN = 20
    optimization = Optimization(curve, sushi, uniswap, DESIRED_RETURN)
    print(optimization.optimize_cost())

if __name__ == "__main__": main()
