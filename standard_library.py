# standard_library.py


def prob1(L):
    """Return the minimum, maximum, and average of the entries of L
    (in that order, separated by a comma).
    """
    return min(L),max(L),sum(L)/len(L) #min,max,average
    

def prob2():
    """Determine which Python objects are mutable and which are immutable.
    Test integers, strings, lists, tuples, and sets. Print your results.
    """
    i = 31
    w = i
    w += 1
    if i == w: #check if int is mutable
        print('integers')
    s = 'hi'
    x = s
    x += 'gh'
    if s == x:#check if str is mutable
        print('strings')
    l = [0,1]
    y = l
    y += [2]
    if l == y:#check if list is mutable
        print('lists')
    t = (0,1)
    z = t 
    z += (1,)
    if t == z:#check if tuple is mutable
        print('tuples')
    my_set = {0,1}
    set2 = my_set
    set2.add(2)
    if my_set == set2: #check if set is mutable
        print('sets')
    

def hypot(a, b):
    """Calculate and return the length of the hypotenuse of a right triangle.
    Do not use any functions other than sum(), product() and sqrt() that are
    imported from your 'calculator' module.

    Parameters:
        a: the length one of the sides of the triangle.
        b: the length the other non-hypotenuse side of the triangle.
    Returns:
        The length of the triangle's hypotenuse.
    """
    #calculate hypotenuse
    c = calculator.sqrt(calculator.sum(calculator.product(a,a),calculator.product(b,b)))
    return c


def power_set(A):
    """Use itertools to compute the power set of A.

    Parameters:
        A (iterable): a str, list, set, tuple, or other iterable collection.

    Returns:
        (list(sets)): The power set of A as a list of sets.
    """
    from itertools import combinations
    powerset = []
    for i in range(len(A)+1): 
        powerset += list(combinations(A,i))#do all combinations of the input
    for j in range(len(powerset)):#change it to a list of sets
        powerset[j] = set(powerset[j])
    return powerset
    

def shut_the_box(player, timelimit):
    """Play a single game of shut the box."""
    timelimit = float(timelimit)
    start = time.time()
    dice = [1,2,3,4,5,6]
    remaining = [1,2,3,4,5,6,7,8,9]

    while time.time() - start < timelimit:
        if sum(remaining) > 6:
            #remaining
            print('Numbers left: ',remaining)
            #roll
            roll = random.randint(1,6)+random.randint(1,6)
            print('Roll: ',roll)
            #time left
            print('Seconds left: ',round(start+timelimit-time.time()))
            # check if they lost
            if not box.isvalid(roll,remaining):
                print('You lose.')
                break
            #input
            playerinput = input('Numbers to eliminate: ')
            input_parsed = box.parse_input(playerinput,remaining)
            # make sure they input a valid input
            while sum(input_parsed) != roll:
                playerinput = input('Error try again: ')
                input_parsed = box.parse_input(playerinput,remaining)
            # change into sets to subtract them to get the new remaining
            remaining = list(set(remaining) - set(input_parsed))
        else:
            #remaining
            print('Numbers left: ',remaining)
            #roll
            roll = random.randint(1,6)
            print('Roll: ',roll)
            #time left
            print('Seconds left: ',round(start+timelimit-time.time()))
            # check if they lost
            if not box.isvalid(roll,remaining):
                print('You lose.')
                break
            #input
            playerinput = input('Numbers to eliminate: ')
            input_parsed = box.parse_input(playerinput,remaining)
            # make sure they input a valid input
            while sum(input_parsed) != roll:
                playerinput = input('Error try again: ')
                input_parsed = box.parse_input(playerinput,remaining)
            # change into sets to subtract them to get the new remaining
            remaining = list(set(remaining) - set(input_parsed))
    return print('Times up :(')
        
    
import calculator
import box
import time
import random
import sys
if __name__=='__main__':
    if len(sys.argv) == 3:
        shut_the_box(sys.argv[1],sys.argv[2])

