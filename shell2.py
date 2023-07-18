# shell2.py

from glob import glob
import os
import numpy as np
import subprocess


def grep(target_string, file_pattern):
    """Find all files in the current directory or its subdirectories that
    match the file pattern, then determine which ones contain the target
    string.

    Parameters:
        target_string (str): A string to search for in the files whose names
            match the file_pattern.
        file_pattern (str): Specifies which files to search.

    Returns:
        matched_files (list): list of the filenames that matched the file
               pattern AND the target string.
    """
    #get all files with specified file pattern
    files = glob('**/'+file_pattern,recursive=True)
    F = []
    for file in files: #loop through each file from glob
        with open(file,'r') as wfile:
            rfile = wfile.read() #read file to search through string
            if target_string in rfile:
                F.append(file) #add file path to list
    return F


def largest_files(n):
    """Return a list of the n largest files in the current directory or its
    subdirectories (from largest to smallest).
    """
    #get all files
    options = glob('**/*.*',recursive=True)
    files = []
    sizes = []
    file_sizes = []
   
    for i in options: #get the size of each file
        sizes.append(os.path.getsize(i))

    while np.size(files) != n:
        #get max index
        index = np.argmax(sizes)

        #add it to new lists
        files.append(options[index])
        file_sizes.append(sizes[index])

        #remove them and search again
        sizes.remove(sizes[index])
        options.remove(options[index])

        if len(sizes) == 0:
            break

    smallest_file = files[-1]

    #use unix commands to write a new file
    args = ["wc -l < "+str(smallest_file)+" > smallest.txt"]
    line_count = subprocess.Popen(args, shell=True)

    return files
    

def prob6(n = 10):
   """this problem counts to or from n three different ways, and
      returns the resulting lists each integer
   
   Parameters:
       n (int): the integer to count to and down from
   Returns:
       integerCounter (list): list of integers from 0 to the number n
       twoCounter (list): list of integers created by counting down from n by two
       threeCounter (list): list of integers created by counting up to n by 3
   """
   #print what the program is doing
   integerCounter = list()
   twoCounter = list()
   threeCounter = list()
   counter = n
   for i in range(n+1):
       integerCounter.append(i)
       if (i % 2 == 0):
           twoCounter.append(counter - i)
       if (i % 3 == 0):
           threeCounter.append(i)
   #return relevant values
   return integerCounter, twoCounter, threeCounter
