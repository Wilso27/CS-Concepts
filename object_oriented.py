# object_oriented.py


class Backpack:
    """A Backpack object class. Has a name and a list of contents.

    Attributes:
        name (str): the name of the backpack's owner.
        contents (list): the contents of the backpack.
        color (str): color of the backpack.
        max_size (int): the max number of items in the backpack. Defaults to 5.
    """

    def __init__(self, name, color, max_size=5):
        """Set the name and initialize an empty list of contents.

        Parameters:
            name (str): the name of the backpack's owner.
            color (str): the color of the backpack.
            max_size (int): the max number of items in the backpack. Defaults to 5.
        """
        self.name = name
        self.contents = []
        self.color = color
        self.max_size = max_size

    def put(self, item):
        """Add an item to the backpack's list of contents. Tells you if there is no room."""
        #checks if 
        if len(self.contents) < self.max_size:
            self.contents.append(item)
        else:
            print('No Room!')

    def dump(self):
        '''Removes the contents of the backpack.'''
        self.contents.clear()

    def take(self, item):
        """Remove an item from the backpack's list of contents.
        Parameters:
            item (str): an item to remove.
        """
        self.contents.remove(item)

    # Magic Methods -----------------------------------------------------------

    def __add__(self, other):
        """Add the number of contents of each Backpack.
        """
        return len(self.contents) + len(other.contents)

    def __lt__(self, other):
        """Compare two backpacks. If 'self' has fewer contents
        than 'other', return True. Otherwise, return False.
        """
        return len(self.contents) < len(other.contents)
    
    def __eq__(self, backpack):
        '''Compares if two backpacks are equal.
        
        Parameters: 
            backpack: Input a backpack object.
        '''
        # compares number of elements in each backpack
        if len(self.contents) == len(backpack.contents):
            if self.name == backpack.name:
                if self.color == backpack.color:
                    return True
        else:
            return False
    
    def __str__(self):
        # concatenated strings to format the way the book does
        return 'Owner:' + '\t' + self.name + '\n' + 'Color:' + '\t' + self.color + '\n' + 'Size:' + '\t' + str(len(self.contents)) + '\n' + 'Max Size:' + '\t' + str(self.max_size) + '\n' + 'Contents:' + '\t' + str(self.contents)


class Knapsack(Backpack):
    """A Knapsack object class. Inherits from the Backpack class.
    A knapsack is smaller than a backpack and can be tied closed.

    Attributes:
        name (str): the name of the knapsack's owner.
        color (str): the color of the knapsack.
        max_size (int): the maximum number of items that can fit inside.
        contents (list): the contents of the backpack.
        closed (bool): whether or not the knapsack is tied shut.
    """
    def __init__(self, name, color):
        """Use the Backpack constructor to initialize the name, color,
        and max_size attributes. A knapsack only holds 3 item by default.

        Parameters:
            name (str): the name of the knapsack's owner.
            color (str): the color of the knapsack.
            max_size (int): the maximum number of items that can fit inside.
        """
        Backpack.__init__(self, name, color, max_size=3)
        self.closed = True

    def put(self, item):
        """If the knapsack is untied, use the Backpack.put() method."""
        if self.closed:
            print("I'm closed!")
        else:
            Backpack.put(self, item)

    def take(self, item):
        """If the knapsack is untied, use the Backpack.take() method."""
        if self.closed:
            print("I'm closed!")
        else:
            Backpack.take(self, item)

    def weight(self):
        """Calculate the weight of the knapsack by counting the length of the
        string representations of each item in the contents list.
        """
        return sum(len(str(item)) for item in self.contents)


class Jetpack(Backpack):
    """A Backpack object class. Has a name and a list of contents.

    Attributes:
        name (str): the name of the backpack's owner.
        contents (list): the contents of the backpack.
    """
    def __init__(self, name, color, max_size=2, fuel=10):
        """Set the name and initialize an empty list of contents.

        Parameters:
            name (str): the name of the backpack's owner.
            color (str): the color of the backpack.
            max_size (int): the max number of items in the backpack. Defaults to 5.
            fuel (int): the amount of fuel.
        """
        self.name = name
        self.contents = []
        self.color = color
        self.max_size = max_size
        self.fuel = fuel

    def fly(self, burnt_fuel):
        '''Removes fuel from the jetpack.

        Attributes:
            burnt_fuel (int): amount of fuel burned.
        '''
        #checks if burnt fuel exceeds total fuel
        if burnt_fuel > self.fuel:
            print('Not enough fuel!')
        else:
            self.fuel -= burnt_fuel
    
    def dump(self):
        '''Resets the contents of the jetpack and the fuel.'''
        self.contents = []
        self.fuel = 0


class ComplexNumber:
    '''Allows you to work with complex numbers by putting a real
    and imaginary part in for the 2 arguments in that order.
    
    Attributes:
        real (int): real part of the complex number
        imag (int): imaginary part of the complex number
    '''

    def __init__(self, real, imag):
        '''Input complex number as the real part and imaginary part.
        
        Paramters:
            real (int): real part of the complex number
            imag (int): imaginary part of the complex number
        '''

        self.real = real
        self.imag = imag

    def conjugate(self):
        '''Gives the conjugate of a complex number.'''
        return ComplexNumber(self.real, -1*self.imag)
    
    def __str__(self):
        '''Prints the complex number in the form (a+bj)'''
        if self.imag < 0:
            return '('+ str(self.real) + str(self.imag) + 'j' + ')'
        else:
            return '('+ str(self.real) + '+' + str(self.imag) + 'j' + ')'
    
    def __abs__(self):
        '''finds the magnitude of a complex number'''
        from math import sqrt
        return sqrt(self.real**2+self.imag**2)

    def __eq__(self, other):
        '''checks if both the real and imaginary parts of a complex
        number are equivalent.'''
        if self.real == other.real and self.imag == other.imag:
            return True
        else:
            return False
    
    def __add__(self, other):
        '''adds two complex numbers.'''
        return ComplexNumber(self.real+other.real,self.imag+other.imag)

    def __sub__(self, other):
        '''subtracts two complex numbers.'''
        return ComplexNumber(self.real-other.real,self.imag-other.imag)
    
    def __mul__(self, other):
        '''multiplies two complex numbers.'''
        return ComplexNumber(self.real*other.real-self.imag*other.imag,self.real*other.imag+self.imag*other.real)

    def __truediv__(self, other):
        '''divides two complex numbers.'''
        return ComplexNumber((self.real*other.real+self.imag*other.imag)/(other.real**2+other.imag**2),((self.imag*other.real-self.real*other.imag)/(other.real**2+other.imag**2)))
