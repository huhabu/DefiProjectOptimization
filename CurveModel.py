#based on vyper smart contracts made for CurveCrypto tricrypto pool: https://github.com/curvefi/curve-crypto-contract/tree/master/contracts/tricrypto 

from functools import reduce

class CurveModel:
    

    def __init__(self, N, A, gamma, D, balances, price_scale, fee):
        self.A = A
        self.N = N
        self.D = D
        self.gamma = gamma
        self.balances = balances
        self.price_scale = price_scale
        self.fee = fee
        self.PRECISION = 10**18
        self.precisions = [10**12, 10**10, 1]
        
    def amount_out(self, amount_in, sell=2, buy=1):
        price_scale = [p for p in self.price_scale]
        xp = [self.balances[i] for i in range(self.N)]
        xp[sell] += amount_in
        xp[0] *= self.precisions[0]
        for i in range(self.N-1):
            xp[i+1] = int(xp[i+1] * price_scale[i] *self.precisions[i+1] / self.PRECISION)
        print(xp)
        y = self.newton_y(xp, buy)
        print(xp[buy]-y)
        print(y)
        dy = xp[buy] - y - 1
        xp[buy] = y
        if buy > 0:
            print(dy)
            dy = dy * self.PRECISION / price_scale[buy-1]
        dy /= self.precisions[buy]
        dy *= (10**10-self.fee)/(10**10)
        return dy
    
    def newton_y(self, x, i):
        y = self.D/self.N
        K0_i = 10**18
        S_i = 0
        x_sorted = [b for b in x]
        x_sorted[i] = 0
        x_sorted.sort(reverse=True)
        convergence_limit = max(max(x_sorted[0] / 10**14, self.D / 10**14), 100)
        print(x_sorted)
        print(convergence_limit)
        for j in range(2, self.N+1):
            _x = x_sorted[self.N-j]
            y = y * self.D / (_x * self.N)
            S_i += _x
        for j in range(self.N-1):
            K0_i = K0_i * x_sorted[j] * self.N / self.D
        for j in range(255):
            y_prev = y
            K0 = K0_i * y * self.N / self.D
            S = S_i + y
            _g1k0  = self.gamma + 10**18
            if _g1k0 > K0:
                _g1k0 = _g1k0 - K0 + 1
            else:
                _g1k0 = K0 - _g1k0 + 1

            mul1 = 10**18 * self.D / self.gamma * _g1k0 / self.gamma * _g1k0 * 10000 / self.A
            mul2 = 10**18 + (2 * 10**18) * K0 / _g1k0

            yfprime = 10**18 * y + S * mul2 + mul1
            _dyfprime  = self.D * mul2
            
            if yfprime < _dyfprime:
                y = y_prev / 2
                continue
            else:
                yfprime -= _dyfprime
            fprime = yfprime / y
            y_minus = mul1 / fprime
            y_plus = (yfprime + 10**18 * self.D) / fprime + y_minus * 10**18 / K0
            y_minus += 10**18 * S / fprime

            if y_plus < y_minus:
                y = y_prev / 2
            else:
                y = y_plus - y_minus

            diff = 0
            if y > y_prev:
                diff = y - y_prev
            else:
                diff = y_prev - y
            if diff < max(convergence_limit, y / 10**14):
                return y