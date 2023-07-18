# condition_stability.py


import numpy as np
import sympy as sy
import scipy.linalg as la
import matplotlib.pyplot as plt


def matrix_cond(A):
    """Calculate the condition number of A with respect to the 2-norm."""
    sig_max = la.svdvals(A)[0] # get the singular vals
    sig_min = la.svdvals(A)[-1]
    if sig_min == 0: # check if 0
        return np.inf
    return sig_max / sig_min # compute


def prob2():
    """Randomly perturb the coefficients of the Wilkinson polynomial by
    replacing each coefficient c_i with c_i*r_i, where r_i is drawn from a
    normal distribution centered at 1 with standard deviation 1e-10.
    Plot the roots of 100 such experiments in a single figure, along with the
    roots of the unperturbed polynomial w(x).

    Returns:
        (float) The average absolute condition number.
        (float) The average relative condition number.
    """
    w_roots = np.arange(1, 21)

    # Get the exact Wilkinson polynomial coefficients using SymPy.
    x, i = sy.symbols('x i')
    w = sy.poly_from_expr(sy.product(x-i, (i, 1, 20)))[0]
    w_coeffs = np.array(w.all_coeffs())

    # initialize the arrays
    reals = np.array(())
    imags = np.array(())
    abs_cond = np.array(())
    rel_cond = np.array(())


    for i in range(100):
        # create perturbation
        r = np.random.normal(1,10**-10,21)
        p_coeffs = r * w_coeffs
        p_roots = np.roots(np.poly1d(p_coeffs))

        # sort the roots by size
        p_roots = np.sort(p_roots)
        w_roots = np.sort(w_roots)

        # split complex number
        reals = np.append(reals, np.real(p_roots))
        imags = np.append(imags, np.imag(p_roots))

        # calculate condition numbers
        abs_cond = np.append(abs_cond, la.norm(w_roots - p_roots,np.inf)/la.norm(r,np.inf))
        rel_cond = np.append(rel_cond, abs_cond[i] * la.norm(w_coeffs, np.inf) / la.norm(w_roots, np.inf))


    # plt.plot the thang
    plt.scatter(np.arange(1,21), np.imag(np.arange(1,21)),c='b',label='original')
    plt.scatter(reals,imags, c='k', marker=',', s=1, label='perturbed')
    plt.legend()
    plt.title('Problem 2')
    plt.ylabel('Imaginary Axis')
    plt.xlabel('Real Axis')
    plt.show()

    return np.mean(abs_cond), np.mean(rel_cond)


# Helper function
def reorder_eigvals(orig_eigvals, pert_eigvals):
    """Reorder the perturbed eigenvalues to be as close to the original eigenvalues as possible.
    
    Parameters:
        orig_eigvals ((n,) ndarray) - The eigenvalues of the unperturbed matrix A
        pert_eigvals ((n,) ndarray) - The eigenvalues of the perturbed matrix A+H
        
    Returns:
        ((n,) ndarray) - the reordered eigenvalues of the perturbed matrix
    """
    n = len(pert_eigvals)
    sort_order = np.zeros(n).astype(int)
    dists = np.abs(orig_eigvals - pert_eigvals.reshape(-1,1))
    for _ in range(n):
        index = np.unravel_index(np.argmin(dists), dists.shape)
        sort_order[index[0]] = index[1]
        dists[index[0],:] = np.inf
        dists[:,index[1]] = np.inf
    return pert_eigvals[sort_order]


def eig_cond(A):
    """Approximate the condition numbers of the eigenvalue problem at A.

    Parameters:
        A ((n,n) ndarray): A square matrix.

    Returns:
        (float) The absolute condition number of the eigenvalue problem at A.
        (float) The relative condition number of the eigenvalue problem at A.
    """
    # code they gave us to create matrix perturbation
    reals = np.random.normal(0, 1e-10, A.shape)
    imags = np.random.normal(0, 1e-10, A.shape)
    H = reals + 1j * imags

    # original and perturbed eigvals
    o_eigs = la.eigvals(A)
    p_eigs = la.eigvals(A+H)
    p_eigs = reorder_eigvals(o_eigs, p_eigs)

    # use formulas to get condition numbers
    abs_cond = la.norm( o_eigs - p_eigs, 2) / la.norm( H, 2)
    rel_cond = la.norm( A, 2) * abs_cond / la.norm( o_eigs, 2)

    return abs_cond, rel_cond


def prob4(domain=[-100, 100, -100, 100], res=50):
    """Create a grid [x_min, x_max] x [y_min, y_max] with the given resolution. For each
    entry (x,y) in the grid, find the relative condition number of the
    eigenvalue problem, using the matrix   [[1, x], [y, 1]]  as the input.
    Use plt.pcolormesh() to plot the condition number over the entire grid.

    Parameters:
        domain ([x_min, x_max, y_min, y_max]):
        res (int): number of points along each edge of the grid.
    """
    # create the grid
    x_min, x_max, y_min, y_max = domain[0], domain[1], domain[2], domain[3]
    x_ = np.linspace(x_min, x_max, res)  # Real parts.
    y_ = np.linspace(y_min, y_max, res)  # Imaginary parts.
    X_grid, Y_grid = np.meshgrid(x_, y_)

    REL = np.array(())
    A = lambda x,y: np.array([[1,x],[y,1]])
    for x in range(res):
        rel_cond = np.array(())
        for y in range(res):
            rel_cond = np.append(rel_cond, eig_cond(A(X_grid[x,y], Y_grid[x,y]))[1])
        REL = np.append(REL, rel_cond)


    # plot the result
    plt.pcolormesh(X_grid, Y_grid, np.reshape(REL,(res,res)),cmap='gray_r')
    plt.title('Relative Condition Numbers')
    plt.colorbar()
    plt.tight_layout()
    plt.show()


def prob5(n):
    """Approximate the data from "stability_data.npy" on the interval [0,1]
    with a least squares polynomial of degree n. Solve the least squares
    problem using the normal equation and the QR decomposition, then compare
    the two solutions by plotting them together with the data. Return
    the mean squared error of both solutions, ||Ax-b||_2.

    Parameters:
        n (int): The degree of the polynomial to be used in the approximation.

    Returns:
        (float): The forward error using the normal equations.
        (float): The forward error using the QR decomposition.
    """
    #import data
    x_data, y_data = np.load('stability_data.npy').T
    # create a vandermonde matrix
    A = np.vander(x_data, n+1)

    #Do the two different methods
    x_inv = la.inv(A.T@A) @ A.T @ y_data
    Q,R = la.qr(A,mode="economic")
    x_qr = la.solve_triangular(R,Q.T @ y_data)

    #plot it
    domain = np.linspace(0,1,1000)
    plt.plot(domain,np.polyval(x_inv,domain), label='inverse')
    plt.plot(domain,np.polyval(x_qr,domain), label='QR')
    plt.scatter(x_data, y_data, label='original data')
    plt.title('Best Fit')
    plt.ylim((0,4))
    plt.legend()
    plt.show()

    # return the forward errors
    return la.norm( A@x_inv - y_data, 2), la.norm( A@x_qr - y_data, 2)


def prob6():
    """For n = 5, 10, ..., 50, compute the integral I(n) using SymPy (the
    true values) and the subfactorial formula (may or may not be correct).
    Plot the relative forward error of the subfactorial formula for each
    value of n. Use a log scale for the y-axis.
    """
    n,x = sy.symbols('n x')

    # create domain
    domain = np.arange(5,55,5)
    rel_forward = np.array(())

    # loop through each value of n
    for d in domain:
        I_true = sy.integrate(x**d * sy.exp(x - 1),(x,0,1))
        I = (-1) ** d * (sy.subfactorial(d) - sy.factorial(d) / np.e)
        rel_forward = np.append(rel_forward, np.abs(float(I) - I_true) / np.abs(I_true))

    #plot the results of error
    plt.title('Relative Forward Errors')
    plt.xlabel('n values')
    plt.ylabel('Error Value')
    plt.yscale('log')
    plt.plot(domain,rel_forward)
    plt.show()
