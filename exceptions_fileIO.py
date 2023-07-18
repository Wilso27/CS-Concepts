# exceptions_fileIO.py


from random import choice
import numpy as np


def arithmagic():
    """
    Takes in user input to perform a magic trick and prints the result.
    Verifies the user's input at each step and raises a
    ValueError with an informative error message if any of the following occur:

    The first number step_1 is not a 3-digit number.
    The first number's first and last digits differ by less than $2$.
    The second number step_2 is not the reverse of the first number.
    The third number step_3 is not the positive difference of the first two numbers.
    The fourth number step_4 is not the reverse of the third number.
    """

    step_1 = input("Enter a 3-digit number where the first and last "
                                           "digits differ by 2 or more: ")
    #check if its a 3 digit number
    if len(str(step_1)) != 3:
        raise ValueError("Input must be 3 digits")
    #check if the first and last digits differ by two or more
    if abs(int(step_1[0]) - int(step_1[2])) < 2:
        raise ValueError("First and last didgits must differ by 2 or more")
    step_2 = input("Enter the reverse of the first number, obtained "
                                              "by reading it backwards: ")
    #check if it is the reverse of the first number
    if int(step_1[2])*100 + int(step_1[1])*10 + int(step_1[0]) != int(step_2[0])*100 + int(step_2[1])*10 + int(step_2[2]):
        raise ValueError("This number must be the reverse of the first number")
    step_3 = input("Enter the positive difference of these numbers: ")
    #check if it is the positive difference
    if abs(int(step_1) - int(step_2)) != int(step_3):
        raise ValueError("This is not the positive difference")
    step_4 = input("Enter the reverse of the previous result: ")
    #check if they input the reverse of teh previous number
    if int(step_3[2])*100 + int(step_3[1])*10 + int(step_3[0]) != int(step_4[0])*100 + int(step_4[1])*10 + int(step_4[2]):
        raise ValueError("This is not the reverse of the previous number")

    print(str(step_3), "+", str(step_4), "= 1089 (ta-da!)")


def random_walk(max_iters=1e12):
    """
    If the user raises a KeyboardInterrupt by pressing ctrl+c while the
    program is running, the function should catch the exception and
    print "Process interrupted at iteration $i$".
    If no KeyboardInterrupt is raised, print "Process completed".

    Return walk.
    """
    #try the while loop
    try:
        walk = 0
        directions = [1, -1]
        for i in range(int(max_iters)):
            walk += choice(directions)
    #accept a keyboard interrupt and return the iterations
    except(KeyboardInterrupt):
        print('Process interrupted at iteration',i)
    #if there is no interrupt the process was completed
    else:
        print('Process completed')
    return walk


class ContentFilter(object):
    """Class for reading in file

    Attributes:
        filename (str): The name of the file
        contents (str): the contents of the file

    """

    def __init__(self, filename):
        """ Read from the specified file. If the filename is invalid, prompt
        the user until a valid filename is given.
        """
        #keep running until input is valid
        while True:
            try:
                #try opening and if it doesn't work raise errors
                with open(filename,'r') as outfile:
                    self.filename = filename
                    rfile = outfile.read()
                    #define variables to track info for __str__() magic method
                    char = 0
                    alph = 0
                    num = 0
                    whit = 0
                    a = (rfile.split('\n'))
                    a.pop()
                    lin = len(a)
                    #creat alphabet upper and lower to find alph
                    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
                    #count how many characters of each kind are in the file for the str magic method
                    for line in rfile:
                        for k in range(len(line)):
                            char +=1
                        if line[k] in alphabet:
                            alph += 1
                        if line[k] in [0,1,2,3,4,5,6,7,8,9]:
                            num += 1
                        if(line[k]==' '):
                            whit+=1
                        if(line[k]=='\n'):
                            whit+=1
                        if line[k] == '\t':
                            whit+=1
                    #make them all attributes so they can be accessed in other functions
                    self.char = char
                    self.alph = alph
                    self.num = num
                    self.whit = whit
                    self.lin = lin
                    self.rfile = rfile
                    break
            #except each of the possible errors and loop around
            except(FileNotFoundError):
                print(('FileNotFoundError. Try again: '))
                filename = input()
            except(TypeError):
                print(('TypeError. Try again: '))
                filename = input()
            except(OSError):
                print(('OSError. Try again: '))
                filename = input()
        
    def check_mode(self, mode):
        """ Raise a ValueError if the mode is invalid. """
        #check if mode is valid
        if mode not in ['w','x','a']:
            raise ValueError

    def uniform(self, outfile, mode='w', case='upper'):
        """ Write the data to the outfile with uniform case. Include an additional
        keyword argument case that defaults to "upper". If case="upper", write
        the data in upper case. If case="lower", write the data in lower case.
        If case is not one of these two values, raise a ValueError. """
        self.check_mode(mode)
        #check which case it is
        #if upper change it to uppercase
        if case == 'upper':
            with open(outfile,mode) as woutfile:
                woutfile.writelines(self.rfile.upper())
            return 
        #for lower make it all lowercase
        elif case == 'lower':
            with open(outfile,mode) as woutfile:
                woutfile.writelines(self.rfile.lower())
            return 
        else:
            #raise error if neither
            raise ValueError
        
    def reverse(self, outfile, mode='w', unit='word'):
        """ Write the data to the outfile in reverse order. Include an additional
        keyword argument unit that defaults to "line". If unit="word", reverse
        the ordering of the words in each line, but write the lines in the same
        order as the original file. If units="line", reverse the ordering of the
        lines, but do not change the ordering of the words on each individual
        line. If unit is not one of these two values, raise a ValueError. """
        self.check_mode(mode)
        #check the unit using if and elif
        if unit == 'word':
            #list comprehension to split the list by lines and switching each word in each line
            a = [self.rfile.split('\n')[i].split()[::-1] for i in range(len(self.rfile.split('\n')))]
            L = []
            #format it correctly with newlines at the end
            for k in range(len(a)):
                s = ''
                for l in range(len(a[k])):
                    s += str(a[k][l]) + ' '
                s += '\n'
                L.append(s)
            with open(outfile,mode) as woutfile:
                woutfile.writelines(L)
            return a
        #split by newlines and switch lines instead of words
        elif unit == 'line':
            a = self.rfile.split('\n')[::-1]
            b = [j+'\n' for j in a]
            with open(outfile,mode) as woutfile:
                woutfile.writelines(b)
            return b
        else:
            #raise error if unit is not either
            raise ValueError
        
    def transpose(self, outfile, mode='w'):
        """ Write a transposed version of the data to the outfile. That is, write
        the first word of each line of the data to the first line of the new file,
        the second word of each line of the data to the second line of the new
        file, and so on. Viewed as a matrix of words, the rows of the input file
        then become the columns of the output file, and viceversa. You may assume
        that there are an equal number of words on each line of the input file. """
        #check mode
        self.check_mode(mode)
        #split into a list of the rows
        a = (self.rfile.split('\n'))
        #split each row into words
        L = []
        for i in range(len(a)):
            L.append(a[i].split())
        L.pop() 
        #recreate the list switching the row and column indices thus transposing
        T = []
        for p in range(len(L[0])):
            X = []
            for j in range(len(L)):
                X.append(L[j][p])
            T.append(X)
        #make each row a list of strings so writelines works with it
        #also add new lines in the right places
        F = []
        for k in range(len(T)):
            s = ''
            for l in range(len(T[k])):
                s += str(T[k][l]) + ' '
            s += '\n'
            F.append(s)
        with open(outfile,mode) as woutfile:
                woutfile.writelines(F)
        
    def __str__(self):
        """ Printing a ContentFilter object yields the following output:

        Source file:            <filename>
        Total characters:       <The total number of characters in file>
        Alphabetic characters:  <The number of letters>
        Numerical characters:   <The number of digits>
        Whitespace characters:  <The number of spaces, tabs, and newlines>
        Number of lines:        <The number of lines>
        """
        #print each thing using tabs and newlines
        return 'Source file:' + '\t' + str(self.filename) + '\n' + 'Total characters:' + '\t' + str(self.char) + '\n' + 'Alphabetic characters:' + '\t' + str(self.alph) + '\n' + 'Numerical characters:' + '\t' + str(self.num) + '\n' + 'Whitespace characters:' + '\t' + str(self.whit) + '\n' + 'Number of lines:' + '\t' + str(self.lin)
