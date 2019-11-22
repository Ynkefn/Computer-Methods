import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def LeastSquares(x, y, power):
    A = np.zeros((power+1, power+1))
    sumx = np.zeros(power*2+1)
    sumxy = np.zeros(power+1)

    for pow in range(power*2+1):
        for j in range(len(x)):
            sumx[pow] += x[j]**pow

    for pow in range(power+1):
        for j in range(len(x)):
            sumxy[pow] += y[j]*x[j]**pow

    for row in range(power+1):
        for col in range(power+1):
            A[row][col] = sumx[row+col]

    a = np.linalg.solve(A, sumxy)
    return a

def Horner(x, coeffs):
    n = len(coeffs)
    sum = coeffs[n-1]
    for i in range(n-2, -1, -1):
        sum = sum*x+coeffs[i]

    return sum

def LeastSquaresData(x, y, power, npoints=500):
    a = LeastSquares(x, y, power)

    minx = min(x)
    maxx = max(x)
    xvals = np.linspace(minx, maxx, npoints)
    yvals = np.zeros_like(xvals)

    for i in range(len(xvals)):
        yvals[i] = Horner(xvals[i], a)

    return xvals, yvals

def PlotLeastSquares(x, y, power, showpoints=True, npoints=500):
    a = LeastSquares(x, y, power)

    minx = min(x)
    maxx = max(x)
    xvals = np.linspace(minx, maxx, npoints)
    yvals = np.zeros_like(xvals)

    for i in range(len(xvals)):
        yvals[i] = Horner(xvals[i], a)

    plt.plot(xvals, yvals)
    if showpoints: plt.plot(x, y, 'ro')
    plt.title("Least Squares Curve Fitting")
    plt.show()

def myfunc(x, n):
    return n[0] + n[1]*np.exp(n[2]*x)       # Define the function with n array being the guesses

def Exp(x, y, n):                           # Create function which calls needed values
    def error(n):                           # Create error function to calculate error which takes only the guesses
        penalties = 0
        for i in range(len(x)):             # Loop through and calculate penalties
            penalties += (myfunc(x[i], n) - y[i]) ** 2
        return penalties
    ans = minimize(error, n, method='Powell')       # Call minimize
    return ans.x                            # Return values