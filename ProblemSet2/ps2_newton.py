# 6.00 Problem Set 2
#
# Successive Approximation
#

def evaluate_poly(poly, x):
    """
    Computes the polynomial function for a given value x. Returns that value.

    Example:
    >>> poly = (0.0, 0.0, 5.0, 9.3, 7.0)    # f(x) = 7x^4 + 9.3x^3 + 5x^2
    >>> x = -13
    >>> print evaluate_poly(poly, x)  # f(-13) = 7(-13)^4 + 9.3(-13)^3 + 5(-13)^2
    180339.9

    poly: tuple of numbers, length > 0
    x: number
    returns: float
    """
    
    # Define variables for answer sum and exponent
    ans = 0
    exp = 0
    
    for constant in poly:
        new_val = constant * x ** exp
        ans += new_val
        exp += 1
        
    return ans
        
def compute_deriv(poly):
    """
    Computes and returns the derivative of a polynomial function. If the
    derivative is 0, returns (0.0,).

    Example:
    >>> poly = (-13.39, 0.0, 17.5, 3.0, 1.0)    # x^4 + 3x^3 + 17.5x^2 - 13.39
    >>> print compute_deriv(poly)        # 4x^3 + 9x^2 + 35^x
    (0.0, 35.0, 9.0, 4.0)

    poly: tuple of numbers, length > 0
    returns: tuple of numbers
    """
    # TO DO ... 
    
    # c x ^ 4 + c x ^ 3 + c x ^ 2 + c x ^ 1 + c x ^ 0
    # 4cx ^ 3 + 3cx ^ 2 + 2cx ^ 1 + cx 
    
    exp = 0
    new_poly = ()
    
    for constant in poly:
        new_constant = exp * constant
        new_exp = exp - 1
        if exp > 0:
            new_poly += (new_constant,)
        exp += 1
        
    return new_poly

def compute_root(poly, x_0, epsilon):
    """
    Uses Newton's method to find and return a root of a polynomial function.
    Returns a tuple containing the root and the number of iterations required
    to get to the root.

    Example:
    >>> poly = (-13.39, 0.0, 17.5, 3.0, 1.0)    #x^4 + 3x^3 + 17.5x^2 - 13.39
    >>> x_0 = 0.1
    >>> epsilon = .0001
    >>> print compute_root(poly, x_0, epsilon)
    (0.80679075379635201, 8.0)

    poly: tuple of numbers, length > 1.
         Represents a polynomial function containing at least one real root.
         The derivative of this polynomial function at x_0 is not 0.
    x_0: float
    epsilon: float > 0
    returns: tuple (float, int)
    """
    # TO DO ... 
    
    # Check if x_0 is a root by calculating f(x_0)
    
    #Set a current_x based on input polynomial and x
    current_x = x_0
    
    # Set a count
    count = 1
    
    # Check to see if x is a root. If not, enter loop
    while abs(evaluate_poly(poly, current_x)) > epsilon:
        count += 1
        # If x is not a root, set a new current_x equal to:  x_0 - f(x_0) / f'(x_0)
        # print 'Evaluate poly (f(x)) is: ',evaluate_poly(poly,current_x)
        # print 'Derivative is: ',evaluate_poly(compute_deriv(poly),x_0)
        if current_x == 0:
            break
        current_x = current_x - (evaluate_poly(poly,current_x) / evaluate_poly(compute_deriv(poly),current_x))
    
    return current_x, count
    
# Test answers
evaluate_poly((0.0,0.0,5.0,9.3,7.0), -13)
compute_deriv((-13.39, 0.0, 17.5, 3.0, 1.0))
print compute_root( (-13.39, 0.0, 17.5, 3.0, 1.0),0.1,.0001)