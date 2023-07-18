import numpy as np
import matplotlib.pyplot as plt


def var_of_means(n):
    """ Create an (n x n) array of values randomly sampled from the standard
    normal distribution. Compute the mean of each row of the array. Return the
    variance of these means.

    Parameters:
        n (int): The number of rows and columns in the matrix.

    Returns:
        (float) The variance of the means of each row.
    """
    #create random array
    A = np.random.normal(size=(n,n))
    #compute mean and variance
    Am = np.mean(A,axis=0)
    return np.var(Am)


def prob1():
    """ Create an array of the results of var_of_means() with inputs
    n = 100, 200, ..., 1000. Plot and show the resulting array.
    """
    #create the set from n = 100 to 1000
    L = []
    for i in range(1,11):
        L.append(var_of_means(i*100))
    y = L
    x = np.arange(1,11)
    #plot them
    plt.title("Problem 1", fontsize=18)
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    plt.plot(x,y)
    plt.show()


def prob2():
    """ Plot the functions sin(x), cos(x), and arctan(x) on the domain
    [-2pi, 2pi]. Make sure the domain is refined enough to produce a figure
    with good resolution.
    """
    #set up x and y
    y = np.arange(-5,6)**2
    x = np.linspace(-2*np.pi, 2*np.pi, 50)
    #create the functions
    y = np.sin(x)
    z = np.cos(x)
    u = np.arctan(x)
    plt.title("Problem 2", fontsize=18)
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    #plot the 3 lines
    plt.plot(x, y)
    plt.plot(x, z)
    plt.plot(x, u)
    plt.xlim(-2*np.pi, 2*np.pi)
    plt.show()
    return


def prob3():
    """ Plot the curve f(x) = 1/(x-1) on the domain [-2,6].
        1. Split the domain so that the curve looks discontinuous.
        2. Plot both curves with a thick, dashed magenta line.
        3. Set the range of the x-axis to [-2,6] and the range of the
           y-axis to [-6,6].
    """
    #separate the domain
    x1 = np.linspace(-2, .99999, 100)
    x2 = np.linspace(1.00001, 6, 100)
    plt.xlim(-2, 6)
    plt.ylim(-6,6)
    #plot both sides separately
    y1 = 1/(x1-1)
    y2 = 1/(x2-1)
    plt.title("Problem 3", fontsize=18)
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    #change the color and width line
    plt.plot(x1,y1,'m--', linewidth=4)
    plt.plot(x2,y2,'m--', linewidth=4)
    plt.show()


def prob4():
    """ Plot the functions sin(x), sin(2x), 2sin(x), and 2sin(2x) on the
    domain [0, 2pi], each in a separate subplot of a single figure.
        1. Arrange the plots in a 2 x 2 grid of subplots.
        2. Set the limits of each subplot to [0, 2pi]x[-2, 2].
        3. Give each subplot an appropriate title.
        4. Give the overall figure a title.
        5. Use the following line colors and styles.
              sin(x): green solid line.
             sin(2x): red dashed line.
             2sin(x): blue dashed line.
            2sin(2x): magenta dotted line.
    """
    #subplot 1
    plt.suptitle('Variations') 
    x = np.linspace(0, 2*np.pi)
    plt.subplot(221)
    plt.plot(x,np.sin(x),'g')
    plt.title('sin(x)')
    plt.axis([0,2*np.pi,-2,2])
    #subplot 2
    plt.subplot(222)
    plt.plot(x,np.sin(2*x),'r--')
    plt.title('sin(2x)')
    plt.axis([0,2*np.pi,-2,2])
    #subplot 3
    plt.subplot(223)
    plt.plot(x,2*np.sin(x),'b--')
    plt.title('2sin(x)')
    plt.axis([0,2*np.pi,-2,2])
    #subplot 4
    plt.subplot(224)
    plt.plot(x,2*np.sin(2*x),'m:')
    plt.title('2sin(2x)')
    plt.axis([0,2*np.pi,-2,2])
    plt.tight_layout()
    plt.show()


def prob5():
    """ Visualize the data in FARS.npy. Use np.load() to load the data, then
    create a single figure with two subplots:
        1. A scatter plot of longitudes against latitudes. Because of the
            large number of data points, use black pixel markers (use "k,"
            as the third argument to plt.plot()). Label both axes.
        2. A histogram of the hours of the day, with one bin per hour.
            Label and set the limits of the x-axis.
    """
    plt.figure(figsize=(10,5))
    #separate the data
    FARS = np.load("FARS.npy")
    x = FARS[:,1]
    y = FARS[:,2]
    z = FARS[:,0]
    #scatter plot using longitude to latitude data
    plt.subplot(121)
    plt.title('\'Merica')
    plt.plot(x,y,"k,")
    plt.axis("equal")
    plt.ylabel('y-axis')
    plt.xlabel('x-axis')
    #histogram using the hours of the day agains the amount of crashes
    ax2 = plt.subplot(122)
    ax2.hist(z,bins=24,color='y')
    plt.title('\'Merica Histogram')
    plt.tight_layout()
    plt.ylabel('y-axis')
    plt.xlabel('x-axis')
    plt.show()


def prob6():
    """ Plot the function g(x,y) = sin(x)sin(y)/xy on the domain
    [-2pi, 2pi]x[-2pi, 2pi].
        1. Create 2 subplots: one with a heat map of g, and one with a contour
            map of g. Choose an appropriate number of level curves, or specify
            the curves yourself.
        2. Set the limits of each subplot to [-2pi, 2pi]x[-2pi, 2pi].
        3. Choose a non-default color scheme.
        4. Include a color scale bar for each subplot.
    """
    # Create a 2-D domain with np.meshgrid().
    x = np.linspace(-2*np.pi, 2*np.pi, 100)
    y = x.copy()
    X, Y = np.meshgrid(x, y)
    Z = (np.sin(X)*np.sin(Y))/(X*Y) # Calculate g(x,y) = sin(x)sin(y).
    # Plot the heat map of f over the 2-D domain.
    plt.subplot(131)
    plt.ylabel('y-axis')
    plt.xlabel('x-axis')
    plt.title('Heat Map')
    plt.pcolormesh(X, Y, Z, cmap="viridis")
    plt.colorbar()
    plt.xlim(-2*np.pi, 2*np.pi)
    plt.ylim(-2*np.pi, 2*np.pi)
    # Plot a contour map of f with 10 level curves.
    plt.subplot(132)
    plt.ylabel('y-axis')
    plt.xlabel('x-axis')
    plt.title('Contour Map')
    plt.contour(X, Y, Z, 10, cmap="coolwarm")
    plt.colorbar()
    plt.tight_layout()
    plt.show()
    