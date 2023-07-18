# profiling.py


import numpy as np
from numba import jit
import time
import matplotlib.pyplot as plt


def max_path(filename="triangle.txt"):
    """Find the maximum vertical path in a triangle of values."""
    with open(filename, 'r') as infile:
        data = [[int(n) for n in line.split()]
                        for line in infile.readlines()]
    def path_sum(r, c, total):
        """Recursively compute the max sum of the path starting in row r
        and column c, given the current total.
        """
        total += data[r][c]
        if r == len(data) - 1:          # Base case.
            return total
        else:                           # Recursive case.
            return max(path_sum(r+1, c,   total),   # Next row, same column
                       path_sum(r+1, c+1, total))   # Next row, next column

    return path_sum(0, 0, 0)            # Start the recursion from the top.


def max_path_fast(filename="triangle_large.txt"):
    """Find the maximum vertical path in a triangle of values."""
    # load in data and initialize variables
    with open(filename, 'r') as infile:
        data = [[int(n) for n in line.split()]
                for line in infile.readlines()]
    n = len(data)
    domain = np.arange(0, n - 1, 1)[::-1]

    # loop through each row starting at n-2 and working backwards
    for i in domain:  # sum the larger child entry
        for j in range(len(data[i])):
            m = max(data[i+1][j], data[i+1][j+1])
            data[i][j] += m

    return data[0][0]  # return the final sum


def primes(N):
    """Compute the first N primes."""
    primes_list = []
    current = 2
    while len(primes_list) < N:
        isprime = True
        for i in range(2, current):     # Check for nontrivial divisors.
            if current % i == 0:
                isprime = False
        if isprime:
            primes_list.append(current)
        current += 1
    return primes_list


def primes_fast(N):
    """Compute the first N primes."""
    primes_list = [2]
    current = 3
    integer = 0
    while len(primes_list) < N:  # get N primes
        isprime = True
        for i in primes_list[1:integer]:  # Check for nontrivial divisors.
            if current % i == 0:
                isprime = False
                break
        if isprime:  # if prime add to list
            primes_list.append(current)
        current += 2
        if primes_list[integer]**2 <= current:
            integer += 1
    return primes_list


def nearest_column(A, x):
    """Find the index of the column of A that is closest to x.

    Parameters:
        A ((m,n) ndarray)
        x ((m, ) ndarray)

    Returns:
        (int): The index of the column of A that is closest in norm to x.
    """
    distances = []
    for j in range(A.shape[1]):  # loop through all the columns
        distances.append(np.linalg.norm(A[:,j] - x))
    return np.argmin(distances)


def nearest_column_fast(A, x):
    """Find the index of the column of A that is closest in norm to x.
    Refrain from using any loops or list comprehensions.

    Parameters:
        A ((m,n) ndarray)
        x ((m, ) ndarray)

    Returns:
        (int): The index of the column of A that is closest in norm to x.
    """
    # vind the min of the norms
    return np.argmin(np.linalg.norm(A - x.reshape(-1, 1), axis=0))


def name_scores(filename="names.txt"):
    """Find the total of the name scores in the given file."""
    with open(filename, 'r') as infile:
        names = sorted(infile.read().replace('"', '').split(','))
    total = 0
    for i in range(len(names)):
        name_value = 0
        for j in range(len(names[i])):
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            for k in range(len(alphabet)):
                if names[i][j] == alphabet[k]:
                    letter_value = k + 1
            name_value += letter_value
        total += (names.index(names[i]) + 1) * name_value
    return total


def name_scores_fast(filename='names.txt'):
    """Find the total of the name scores in the given file."""
    with open(filename, 'r') as infile:
        names = sorted(infile.read().replace('"', '').split(','))
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alph = {alphabet[i-1]: i for i in range(1,27)}

    # sum each name using list comp
    return sum([(i+1) * sum([alph[names[i][j]] for j in range(len(names[i]))]) for i in range(len(names))])


def fibonacci():
    """Yield the terms of the Fibonacci sequence with F_1 = F_2 = 1."""
    n = 1
    F_ = 1
    F = 1

    while True:  # code the fib sequence
        if n > 2:
            Fn = F + F_
            F_ = F
            F = Fn
            yield Fn  # yield the nth fib number
        else:
            yield 1
        n += 1


def fibonacci_digits(N=1000):
    """Return the index of the first term in the Fibonacci sequence with
    N digits.

    Returns:
        (int): The index.
    """
    # loop through using generator object
    # Enumerate to track the index when the N-length fib num is reached
    for i, x in enumerate(fibonacci()):
        if len(str(x)) >= N:
            return i + 1


def prime_sieve(N):
    """Yield all primes that are less than N."""
    int_list = np.arange(2, N+1)
    while len(int_list) > 0:  # loop while there are still elements in the array
        yield int_list[0]
        int_list = int_list[int_list % int_list[0] != 0]  # create a mask for values that are nonzero


def matrix_power(A, n):
    """Compute A^n, the n-th power of the matrix A."""
    product = A.copy()
    temporary_array = np.empty_like(A[0])
    m = A.shape[0]
    for power in range(1, n):
        for i in range(m):
            for j in range(m):
                total = 0
                for k in range(m):
                    total += product[i,k] * A[k,j]
                temporary_array[j] = total
            product[i] = temporary_array
    return product


@jit
def matrix_power_numba(A, n):
    """Compute A^n, the n-th power of the matrix A, with Numba optimization."""
    product = A.copy()  # initialize variables
    temporary_array = np.empty_like(A[0])
    m = A.shape[0]
    for power in range(1, n):  #loop through all powers
        for i in range(m):
            for j in range(m):
                total = 0
                for k in range(m):
                    total += product[i, k] * A[k, j]
                temporary_array[j] = total
            product[i] = temporary_array  # store the matrix product
    return product


def prob7(n=10):
    """Time matrix_power(), matrix_power_numba(), and np.linalg.matrix_power()
    on square matrices of increasing size. Plot the times versus the size.
    """
    # run once to compile
    a = matrix_power_numba(np.random.random((2,2)), 2)

    # initialize lists to store times
    m_list = 2**np.arange(2, 8)
    mp = []
    mpn = []
    npmp = []

    for m in m_list:  # loop through each matrix size
        A = np.random.random((m, m))

        # Time each function separately and store the times in a list
        start = time.perf_counter()
        matrix_power(A, n)
        end = time.perf_counter()
        mp.append(end - start)

        start = time.perf_counter()
        matrix_power_numba(A, n)
        end = time.perf_counter()
        mpn.append(end - start)

        start = time.perf_counter()
        np.linalg.matrix_power(A, n)
        end = time.perf_counter()
        npmp.append(end - start)

    # Plot the results
    fig, ax = plt.subplots()

    plt.loglog(m_list, mp, label="Naive")
    plt.loglog(m_list, mpn, label="Numba")
    plt.loglog(m_list, npmp, label="Numpy")
    plt.title(f"Matrix Power timing for power n={n}")
    plt.xlabel("m")
    plt.ylabel("Time (seconds)")
    ax.set_xscale('log', base=2)
    ax.set_yscale('log', base=2)

    plt.legend()
    plt.tight_layout()
    plt.show()
