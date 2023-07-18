# sympy_intro.py


import sympy as sy
import numpy as np
import matplotlib.pyplot as plt


def prob1():
    """Return an expression for

        (2/5)e^(x^2 - y)cosh(x+y) + (3/7)log(xy + 1).

    Make sure that the fractions remain symbolic.
    """
    # create symbols and the expression
    x,y = sy.symbols('x y')
    return sy.Rational(2,5) * sy.exp(x**2 - y) * sy.cosh(x + y) + sy.Rational(3,7) * sy.log(x*y + 1)


def prob2():
    """Compute and simplify the following expression.

        product_(i=1 to 5)[ sum_(j=i to 5)[j(sin(x) + cos(x))] ]
    """
    # create symbols and the expression
    x,y,i,j = sy.symbols('x y i j')
    return sy.simplify(sy.product(sy.summation( j*(sy.sin(x) + sy.cos(x)), (j,i,5)), (i,1,5)))


def prob3(N):
    """Define an expression for the Maclaurin series of e^x up to order N.
    Substitute in -y^2 for x to get a truncated Maclaurin series of e^(-y^2).
    Lambdify the resulting expression and plot the series on the domain
    y in [-2,2]. Plot e^(-y^2) over the same domain for comparison.
    """
    #create the sympy expression
    x,n,y = sy.symbols('x n y')
    mac = sy.summation( x**n/sy.factorial(n), (n,0,N))

    # create the domain and lambdify
    domain = np.linspace(-2,2,100)
    mac_lamb = sy.lambdify(y,mac.subs(x, -(y**2)),"numpy")

    #plot the functions
    plt.title('Maclaurin Series')
    plt.plot(domain,mac_lamb(domain),label='Maclaurin')
    plt.plot(domain,np.exp(-(domain)**2),label='Original')
    plt.legend()
    plt.show()


def prob4():
    """The following equation represents a rose curve in cartesian coordinates.

    0 = 1 - [(x^2 + y^2)^(7/2) + 18x^5 y - 60x^3 y^3 + 18x y^5] / (x^2 + y^2)^3

    Construct an expression for the nonzero side of the equation and convert
    it to polar coordinates. Simplify the result, then solve it for r.
    Lambdify a solution and use it to plot x against y for theta in [0, 2pi].
    """
    # create the symbols and expressions then simplify
    x,y,r,t = sy.symbols('x y r t')
    f = 1 - (((x**2 + y**2)**(sy.Rational(7,2)) + 18*x**5*y - 60*x**3*y**3 + 18*x*y**5)/((x**2 + y**2)**3))
    f = f.subs(x, r*sy.cos(t))
    f = f.subs(y, r*sy.sin(t))
    simp = sy.simplify(f)
    
    #solve for r and lambdify it with respect to t.
    r = sy.lambdify(t,sy.solve(simp,r)[0],'numpy')
    theta = np.linspace(0,2*np.pi,1000)

    #plot x(theta) against y(theta)
    plt.title('Rose Curve')
    plt.plot(r(theta)*np.cos(theta),r(theta)*np.sin(theta))
    plt.show()


def prob5():
    """Calculate the eigenvalues and eigenvectors of the following matrix.

            [x-y,   x,   0]
        A = [  x, x-y,   x]
            [  0,   x, x-y]

    Returns:
        (dict): a dictionary mapping eigenvalues (as expressions) to the
            corresponding eigenvectors (as SymPy matrices).
    """
    #create symbols and Matrix
    x,y,L = sy.symbols('x y L')
    A = sy.Matrix([[x - y, x, 0],[x, x - y, x],[0, x, x - y]])
    D = dict()

    #find Eigenvalues
    eigvals = sy.solve(sy.det(A-L*sy.eye(3)),L)

    #find Eigenvectors and add to dictionary
    for i in range(3):
        D[eigvals[i]] = (A-eigvals[i]*sy.eye(3)).nullspace()

    return D


def prob6():
    """Consider the following polynomial.

        p(x) = 2*x^6 - 51*x^4 + 48*x^3 + 312*x^2 - 576*x - 100

    Plot the polynomial and its critical points over [-5,5]. Determine which
    points are maxima and which are minima. Plot the maxima in one color and the
    minima in another color. Return the minima and maxima (x values) as two
    separate sets.

    Returns:
        (set): the local minima.
        (set): the local maxima.
    """
    # create the function
    x = sy.symbols('x')
    f = 2*x**6 - 51*x**4 + 48*x**3 + 312*x**2 - 576*x - 100
    p = sy.lambdify(x,f, 'numpy')

    # find the zeros using the derivative
    Df = sy.diff(f,x)
    DDf = sy.diff(Df,x)
    crit_points = np.array(sy.solve(Df,x))

    # do the second derivative test
    DDp = sy.lambdify(x,DDf, 'numpy')
    DDf_test = DDp(crit_points)
    mask_min = DDf_test > 0
    mask_max = DDf_test < 0
    
    # plot the function with the max and mins
    domain = np.linspace(-5,5,1000)
    plt.title('Mins and Maxes')
    plt.plot(domain,p(domain))
    plt.plot(crit_points[mask_min], p(crit_points[mask_min]), '.', markersize=15, label='min')
    plt.plot(crit_points[mask_max], p(crit_points[mask_max]), '.', markersize=15, label='max')
    plt.legend()
    plt.show()

    return set(crit_points[mask_min]),set(crit_points[mask_max])


def prob7():
    """Calculate the volume integral of f(x,y,z) = (x^2 + y^2 + z^2)^2 over the
    sphere of radius r. Lambdify the resulting expression and plot the integral
    value for r in [0,3]. Return the value of the integral when r = 2.

    Returns:
        (float): the integral of f over the sphere of radius 2.
    """
    #create h
    x,y,z,r = sy.symbols('x y z r')
    rho,phi,theta = sy.symbols('rho phi theta')
    h1 = rho*sy.sin(phi)*sy.cos(theta)
    h2 = rho*sy.sin(phi)*sy.sin(theta)
    h3 = rho*sy.cos(phi)
    h = sy.Matrix([h1,h2,h3])

    #create f
    f = (x**2 + y**2 + z**2)**2
    f = sy.lambdify((x,y,z),f)

    #find the jacobian and det of h
    J = h.jacobian([rho,phi,theta])
    integrand = sy.simplify(f(h1,h2,h3)*((J.det())))

    #calculate the integral symbolically
    integral = sy.integrate(integrand, (rho,0,r), (theta,0,2*sy.pi), (phi,0,sy.pi))

    int_lamb = sy.lambdify(r, integral,'numpy')

    #plot the function
    domain = np.linspace(0,3,100)
    plt.title('Plot of the Integral')
    plt.plot(domain,int_lamb(domain))
    plt.show()

    return int_lamb(2)
