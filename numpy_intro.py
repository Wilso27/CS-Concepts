# numpy_intro.py


import numpy as np


def prob1():
    """ Define the matrices A and B as arrays. Return the matrix product AB. """
    A = np.array(([3,-1,4],[1,5,-9])) # define 2 arrays
    B = np.array(([2,6,-5,3],[5,-8,9,7],[9,-3,-2,-3]))
    return A@B # multiply them


def prob2():
    """ Define the matrix A as an array. Return the matrix -A^3 + 9A^2 - 15A. """
    A = np.array(([3,1,4],[1,5,9],[-5,3,1]))
    return -1*A@A@A+9*A@A-15*A #define the array and plug it into the equation


def prob3():
    """ Define the matrices A and B as arrays using the functions presented in
    this section of the manual (not np.array()). Calculate the matrix product ABA,
    change its data type to np.int64, and return it.
    """
    #create 7x7 array with ones
    Ap = np.full((7,7),1)
    #take the triangle of that
    A = np.triu(Ap)
    #Create a matrix of -6's
    Bp = np.full((7,7),-6)
    #add a triangle matrix to a full 5 to get desired matrix
    B = np.tril(Bp)+np.full((7,7),5)
    return np.int64(A@B@A)


def prob4(A):
    """ Make a copy of 'A' and use fancy indexing to set all negative entries of
    the copy to 0. Return the resulting array.

    Example:
        >>> A = np.array([-3,-1,3])
        >>> prob4(A)
        array([0, 0, 3])
    """
    #copy it
    B = A.copy()
    #Create a variable of all neg entries
    mask = B < 0
    #set them equal to 0
    B[mask] = 0
    return B


def prob5():
    """ Define the matrices A, B, and C as arrays. Use NumPy's stacking functions
    to create and return the block matrix:
                                | 0 A^T I |
                                | A  0  0 |
                                | B  0  C |
    where I is the 3x3 identity matrix and each 0 is a matrix of all zeros
    of the appropriate size.
    """
    #create arrays of desired size
    A = np.array(([0,2,4],[1,3,5]))
    B = np.array(([3,0,0],[3,3,0],[3,3,3]))
    C = np.array(([-2,0,0],[0,-2,0],[0,0,-2]))
    I = np.eye(3)
    z1 = np.zeros((3,3))
    z2 = np.zeros((2,2))
    z3 = np.zeros((2,3))
    z4 = np.zeros((3,2))
    #stack them in the way the question asked as columns
    c1 = np.vstack((z1,A,B))
    c2 = np.vstack((A.T,z2,z4))
    c3 = np.vstack((I,z3,C))
    #stack them the other way and return
    return np.hstack((c1,c2,c3))
    


def prob6(A):
    """ Divide each row of 'A' by the row sum and return the resulting array.
    Use array broadcasting and the axis argument instead of a loop.

    Example:
        >>> A = np.array([[1,1,0],[0,1,0],[1,1,1]])
        >>> prob6(A)
        array([[ 0.5       ,  0.5       ,  0.        ],
               [ 0.        ,  1.        ,  0.        ],
               [ 0.33333333,  0.33333333,  0.33333333]])
    """
    #find the sum of each row and divide by broadcasting
    x = A.sum(axis=1).reshape(A.shape[0],1)
    return A/x


def prob7():
    """ Given the array stored in grid.npy, return the greatest product of four
    adjacent numbers in the same direction (up, down, left, right, or
    diagonally) in the grid. Use slicing, as specified in the manual.
    """
    #load in grid file
    grid = np.load("grid.npy")
    #create arrays of all the possibilities 
    #right left
    RL = np.max(grid[:,:-3] * grid[:,1:-2] * grid[:,2:-1] * grid[:,3:])
    #up down
    UD = np.max(grid[:-3,:] * grid[1:-2,:] * grid[2:-1,:] * grid[3:,:])
    #diagonal right
    DR = np.max(grid[:-3,:-3] * grid[1:-2,1:-2] * grid[2:-1,2:-1] * grid[3:,3:])
    #diagonal left
    DL = np.max(grid[:-3,3:] * grid[1:-2,2:-1] * grid[2:-1,1:-2] * grid[3:,:-3])
    #take the max of the total matrix of combinations
    return max([RL,UD,DR,DL])
