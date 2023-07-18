# linked_lists.py


class Node:
    """A basic node class for storing data."""
    def __init__(self, data):
        """Store the data in the value attribute. Only accepts int, float, or str
                
        Raises:
            TypeError: if data is not of type int, float, or str.
        """
        #check each acceptable data type
        if type(data) != str and type(data) != int and type(data) != float:
            raise TypeError('Input must be int, float, or str')
        self.value = data


class LinkedListNode(Node):
    """A node class for doubly linked lists. Inherits from the Node class.
    Contains references to the next and previous nodes in the linked list.
    """
    def __init__(self, data):
        """Store the data in the value attribute and initialize
        attributes for the next and previous nodes in the list.
        """
        Node.__init__(self, data)       # Use inheritance to set self.value.
        self.next = None                # Reference to the next node.
        self.prev = None                # Reference to the previous node.

    
class LinkedList:
    """Doubly linked list data structure class.

    Attributes:
        head (LinkedListNode): the first node in the list.
        tail (LinkedListNode): the last node in the list.
    """
    def __init__(self):
        """Initialize the head and tail attributes by setting
        them to None, since the list is empty initially.
        """
        #initialize attributes
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, data):
        """Append a new node containing the data to the end of the list."""
        # Create a new node to store the input data.
        new_node = LinkedListNode(data)
        if self.head is None:
            # If the list is empty, assign the head and tail attributes to
            # new_node, since it becomes the first and last node in the list.
            self.head = new_node
            self.tail = new_node
        else:
            # If the list is not empty, place new_node after the tail.
            self.tail.next = new_node               # tail --> new_node
            new_node.prev = self.tail               # tail <-- new_node
            # Now the last node in the list is new_node, so reassign the tail.
            self.tail = new_node
        #create length function
        self.length += 1

    def find(self, data):
        """Return the first node in the list containing the data.

        Raises:
            ValueError: if the list does not contain the data.

        Examples:
            >>> l = LinkedList()
            >>> for x in ['a', 'b', 'c', 'd', 'e']:
            ...     l.append(x)
            ...
            >>> node = l.find('b')
            >>> node.value
            'b'
            >>> l.find('f')
            ValueError: <message>
        """
        #check if empty
        if self.head is None:
            raise ValueError('LinkedList is empty')
        node = self.head
        search = LinkedListNode(data)
        #check each node in the list
        while node is not search:
            #if they are equal we're done
            if node.value == search.value:
                return node
            #check if it's at the end of the list
            else:
                if node.next.value == self.tail.value:
                    if node.next.value is search.value:
                        return node.next
                    #error if it isn't in the list
                    else:
                        raise ValueError('Data is not in LinkedList')
                #loop to the next node
                else:
                    node = node.next
        return node

    def get(self, i):
        """Return the i-th node in the list.

        Raises:
            IndexError: if i is negative or greater than or equal to the
                current number of nodes.

        Examples:
            >>> l = LinkedList()
            >>> for x in ['a', 'b', 'c', 'd', 'e']:
            ...     l.append(x)
            ...
            >>> node = l.get(3)
            >>> node.value
            'd'
            >>> l.get(5)
            IndexError: <message>
        """
        #check if index is in range
        if i < 0 or i >= len(self):
            raise IndexError('LinkedList index out of range')
        node = self.head
        #loop to the i-th entry and return it
        for j in range(i):
            node = node.next
        return node

    def __len__(self):
        """Return the number of nodes in the list.

        Examples:
            >>> l = LinkedList()
            >>> for i in (1, 3, 5):
            ...     l.append(i)
            ...
            >>> len(l)
            3
            >>> l.append(7)
            >>> len(l)
            4
        """
        #return attribute length
        return self.length

    def __str__(self):
        """String representation: the same as a standard Python list.

        Examples:
            >>> l1 = LinkedList()       |   >>> l2 = LinkedList()
            >>> for i in [1,3,5]:       |   >>> for i in ['a','b',"c"]:
            ...     l1.append(i)        |   ...     l2.append(i)
            ...                         |   ...
            >>> print(l1)               |   >>> print(l2)
            [1, 3, 5]                   |   ['a', 'b', 'c']
        """
        #assign head to variable
        node = self.head
        string = ''
        #check length for empty
        if len(self) == 0:
            return '[]'
        else: 
            #append the comma and space to a single string
            for i in range(len(self)-1):
                string += repr(node.value)+', '
                node = node.next
            #add brackets
            return '['+string+repr(self.tail.value)+']'

    def remove(self, data):
        """Remove the first node in the list containing the data.

        Raises:
            ValueError: if the list is empty or does not contain the data.

        Examples:
            >>> print(l1)               |   >>> print(l2)
            ['a', 'e', 'i', 'o', 'u']   |   [2, 4, 6, 8]
            >>> l1.remove('i')          |   >>> l2.remove(10)
            >>> l1.remove('a')          |   ValueError: <message>
            >>> l1.remove('u')          |   >>> l3 = LinkedList()
            >>> print(l1)               |   >>> l3.remove(10)
            ['e', 'o']                  |   ValueError: <message>
        """
        #find target node
        target = self.find(data)
        #check if it is the first or last node in LinkedList
        if target.next is None:
            #check if it is the first and last
            if target.prev is None:
                target = None
                self.head = None
                self.tail = None
            #reassign tail if last
            else:
                target.prev.next = None
                self.tail = target.prev
        #otherwise check if it is the first
        elif target.prev is None:
            target.next.prev = None
            self.head = target.next
        #if it isn't first or last then do this
        else:
            target.next.prev = target.prev
            target.prev.next = target.next
            target = None
        
        self.length -= 1

    def insert(self, index, data):
        """Insert a node containing data into the list immediately before the
        node at the index-th location.

        Raises:
            IndexError: if index is negative or strictly greater than the
                current number of nodes.

        Examples:
            >>> print(l1)               |   >>> len(l2)
            ['b']                       |   5
            >>> l1.insert(0, 'a')       |   >>> l2.insert(6, 'z')
            >>> print(l1)               |   IndexError: <message>
            ['a', 'b']                  |
            >>> l1.insert(2, 'd')       |   >>> l3 = LinkedList()
            >>> print(l1)               |   >>> l3.insert(1, 'a')
            ['a', 'b', 'd']             |   IndexError: <message>
            >>> l1.insert(2, 'c')       |
            >>> print(l1)               |
            ['a', 'b', 'c', 'd']        |
        """
        #check index
        if index > len(self) or index < 0:
            raise IndexError('Invalid index')
        
        new = LinkedListNode(data)
        #if inserting at end just append
        if index == len(self):
            self.append(data)
        #if beginning then change the head
        elif index == 0:
            self.length += 1
            temphead = self.head
            self.head = new
            self.head.next = temphead
            temphead.prev = new
        #if the middle then change all prev and next
        else:
            self.length += 1
            target = self.get(index)
            new.prev = target.prev
            new.next = target
            target.prev.next = new
            target.prev = new
        

class Deque(LinkedList):
    '''Deque data structure class.

    Attributes:
        head (LinkedListNode): the first node in the list.
        tail (LinkedListNode): the last node in the list.'''
    def __init__(self):
        """From LinkedList: Initialize the head and tail attributes by setting
        them to None, since the list is empty initially.
        """
        LinkedList.__init__(self)
    
    def pop(self):
        '''Removes last element from a LinkedList'''
        #check length
        if len(self) == 0:
            raise ValueError('LinkedList is empty')
        #reassign the tail and head if it is the only element
        if len(self) == 1:
            data = self.tail.value
            self.tail = None
            self.head = None
            self.length -= 1
            return data
        #if it is more than one element just remove element on the end and reassign
        else:
            data = self.tail.value
            self.tail = self.tail.prev
            self.tail.next = None
            self.length -= 1
            return data

    def popleft(self):
        '''Removes first element from a LinkedList'''
        #raise error if empty
        if len(self) == 0:
            raise ValueError('LinkedList is empty')
        #check if length 1 and reassign head and tail
        if len(self) == 1:
            data = self.head.value
            self.tail = None
            self.head = None
            self.length -= 1
            return data
        #reassign head and assign previous element
        else:
            data = self.head.value
            self.head = self.head.next
            self.head.prev = None
            self.length -= 1
            return data

    def appendleft(self, new):
        '''appends to the first part of the deque'''
        #use insert in the 0th position
        LinkedList.insert(self, 0, new)

    def remove(*args, **kwargs):
        #disable remove
        raise NotImplementedError("Use pop() or popleft() for removal")
    
    def insert(*args, **kwargs):
        #disable insert
        raise NotImplementedError("Use append() or appendleft() for removal")


def prob7(infile, outfile):
    """Reverse the contents of a file by line and write the results to
    another file.

    Parameters:
        infile (str): the file to read from.
        outfile (str): the file to write to.
    """
    #open file for reading
    with open(infile,'r') as file:
        #split it by newlines
        rfile = file.read().split('\n')
        stack = Deque()
        #loop through each line and append it to a deque
        for line in rfile:
            stack.append(line)
    #open outfile and writed each line by popping
    with open(outfile, 'w') as wfile:
        for i in rfile:
            wfile.write(stack.pop() + '\n')
