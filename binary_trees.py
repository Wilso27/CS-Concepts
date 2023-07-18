# binary_trees.py


# These imports are used in BST.draw().
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from matplotlib import pyplot as plt
import random
import time


class SinglyLinkedListNode:
    """A node with a value and a reference to the next node."""
    def __init__(self, data):
        self.value, self.next = data, None


class SinglyLinkedList:
    """A singly linked list with a head and a tail."""
    def __init__(self):
        self.head, self.tail = None, None

    def append(self, data):
        """Add a node containing the data to the end of the list."""
        n = SinglyLinkedListNode(data)
        if self.head is None:
            self.head, self.tail = n, n
        else:
            self.tail.next = n
            self.tail = n

    def iterative_find(self, data):
        """Search iteratively for a node containing the data.
        If there is no such node in the list, including if the list is empty,
        raise a ValueError.

        Returns:
            (SinglyLinkedListNode): the node containing the data.
        """
        current = self.head
        while current is not None:
            if current.value == data:
                return current
            current = current.next
        raise ValueError(str(data) + " is not in the list")
       
    def recursive_find(self, data):
        """Search recursively for the node containing the data.
        If there is no such node in the list, including if the list is empty,
        raise a ValueError.

        Returns:
            (SinglyLinkedListNode): the node containing the data.
        """
        current = self.head
        def node_check(node):
            '''Checks if a node matches the data'''
            #first base case if data not found
            if node is None:
                raise ValueError('Data could not be found')
            #second base case if data found
            if node.value == data:
                return node
            #start recursion
            else:
                return node_check(node.next)
        return node_check(current)


class BSTNode:
    """A node class for binary search trees. Contains a value, a
    reference to the parent node, and references to two child nodes.
    """
    def __init__(self, data):
        """Construct a new node and set the value attribute. The other
        attributes will be set when the node is added to a tree.
        """
        self.value = data
        self.prev = None        # A reference to this node's parent node.
        self.left = None        # self.left.value < self.value
        self.right = None       # self.value < self.right.value


class BST:
    """Binary search tree data structure class.
    The root attribute references the first node in the tree.
    """
    def __init__(self):
        """Initialize the root attribute."""
        self.root = None

    def find(self, data):
        """Return the node containing the data. If there is no such node
        in the tree, including if the tree is empty, raise a ValueError.
        """

        # Define a recursive function to traverse the tree.
        def _step(current):
            """Recursively step through the tree until the node containing
            the data is found. If there is no such node, raise a Value Error.
            """
            if current is None:                     # Base case 1: dead end.
                raise ValueError(str(data) + " is not in the tree.")
            if data == current.value:               # Base case 2: data found!
                return current
            if data < current.value:                # Recursively search left.
                return _step(current.left)
            else:                                   # Recursively search right.
                return _step(current.right)

        # Start the recursion on the root of the tree.
        return _step(self.root)

    def insert(self, data):
        """Insert a new node containing the specified data.

        Raises:
            ValueError: if the data is already in the tree.

        Example:
            >>> tree = BST()                    |
            >>> for i in [4, 3, 6, 5, 7, 8, 1]: |            (4)
            ...     tree.insert(i)              |            / \
            ...                                 |          (3) (6)
            >>> print(tree)                     |          /   / \
            [4]                                 |        (1) (5) (7)
            [3, 6]                              |                  \
            [1, 5, 7]                           |                  (8)
            [8]                                 |
        """
        #check if empty
        if self.root is None:
            self.root = BSTNode(data)
        else:
            current = self.root
            new_node = BSTNode(data)
            #loop through the tree until you reach the end of a branch
            while current is not None:
                #check if data is less than
                if current.value > data:
                    #base case when it reaches the last node
                    if current.left is None:
                        current.left = new_node
                        new_node.prev = current
                        return current
                    #try again with the next node
                    else:
                        current = current.left
                #check if data is greater than
                elif current.value < data:
                    #base case when it reaches the last node
                    if current.right is None:
                        current.right = new_node
                        new_node.prev = current
                        return current
                    #try again with the next node
                    else:
                        current = current.right
                #if data matches a current node throw error
                elif current.value == data:
                    raise ValueError('Node already in BST')
                
    def remove(self, data):
        """Remove the node containing the specified data.

        Raises:
            ValueError: if there is no node containing the data, including if
                the tree is empty.

        Examples:
            >>> print(12)                       | >>> print(t3)
            [6]                                 | [5]
            [4, 8]                              | [3, 6]
            [1, 5, 7, 10]                       | [1, 4, 7]
            [3, 9]                              | [8]
            >>> for x in [7, 10, 1, 4, 3]:      | >>> for x in [8, 6, 3, 5]:
            ...     t1.remove(x)                | ...     t3.remove(x)
            ...                                 | ...
            >>> print(t1)                       | >>> print(t3)
            [6]                                 | [4]
            [5, 8]                              | [1, 7]
            [9]                                 |
                                                | >>> print(t4)
            >>> print(t2)                       | [5]
            [2]                                 | >>> t4.remove(1)
            [1, 3]                              | ValueError: <message>
            >>> for x in [2, 1, 3]:             | >>> t4.remove(5)
            ...     t2.remove(x)                | >>> print(t4)
            ...                                 | []
            >>> print(t2)                       | >>> t4.remove(5)
            []                                  | ValueError: <message>
        """
        target = self.find(data)
        target_val = target.value
        parent = target.prev
        #if target is the root
        if parent is None:
            #two children, pass it to the other case since parent is not needed
            if target.right is not None and target.left is not None:
                swap_node = target.left
                #find the left-right most node
                while swap_node.right is not None:
                    swap_node = swap_node.right
                swap_node_val = swap_node.value
                #swap the nodes
                swap_node.value = target_val
                target.value = swap_node_val
                #remove the new target node if the predecessor is a leaf
                if swap_node.left is None:
                    if swap_node.prev.left is not None:
                        if swap_node.prev.left.value == target_val:
                            swap_node.prev.left = None
                        else:
                            swap_node.prev.right = None
                    else:
                        swap_node.prev.right = None
                #remove the new target node if the predecessor has a left child
                else:
                    if swap_node.prev.left is not None:
                        if swap_node.prev.left.value == target_val:
                            swap_node.prev.left = swap_node.left
                        else:
                            swap_node.prev.right = swap_node.left
                    else:
                        swap_node.prev.right = swap_node.left
            #right child
            elif target.right is not None:
                self.root = target.right
                target.right.prev = None
            #left child
            elif target.left is not None:
                self.root = target.left
                target.left.prev = None
            #no children
            else:
                self.root = None
        #if target has no children
        elif target.right is None and target.left is None:
            if parent.right is not None:
                if parent.right.value == data:
                    parent.right = None
                else:
                    parent.left = None
            else:
                parent.left = None
        #if target only has a left child
        elif target.right is None:
            if parent.right is not None:
                if parent.right.value == data:
                    parent.right = target.left
                    target.left.prev = parent
                else:
                    parent.left = target.left
                    target.left.prev = parent
            else:
                parent.left = target.left
                target.left.prev = parent
        #if target only has a right child
        elif target.left is None:
            if parent.right is not None:
                if parent.right.value == data:
                    parent.right = target.right
                    target.right.prev = parent
                else:
                    parent.left = target.right
                    target.right.prev = parent
            else:
                parent.left = target.right
                target.right.prev = parent
        #if target has two children
        else:
            swap_node = target.left
            #find the left-right most node
            while swap_node.right is not None:
                swap_node = swap_node.right
            swap_node_val = swap_node.value
            #swap the nodes
            swap_node.value = target_val
            target.value = swap_node_val
            #remove the new target node if the predecessor is a leaf
            if swap_node.left is None:
                if swap_node.prev.left is not None:
                    if swap_node.prev.left.value == target_val:
                        swap_node.prev.left = None
                    else:
                        swap_node.prev.right = None
                else:
                    swap_node.prev.right = None
            #remove the new target node if the predecessor has a left child
            else:
                if swap_node.prev.left is not None:
                    if swap_node.prev.left.value == target_val:
                        swap_node.prev.left = swap_node.left
                    else:
                        swap_node.prev.right = swap_node.left
                else:
                    swap_node.prev.right = swap_node.left

    def __str__(self):
        """String representation: a hierarchical view of the BST.

        Example:  (3)
                  / \     '[3]          The nodes of the BST are printed
                (2) (5)    [2, 5]       by depth levels. Edges and empty
                /   / \    [1, 4, 6]'   nodes are not printed.
              (1) (4) (6)
        """
        if self.root is None:                       # Empty tree
            return "[]"
        out, current_level = [], [self.root]        # Nonempty tree
        while current_level:
            next_level, values = [], []
            for node in current_level:
                values.append(node.value)
                for child in [node.left, node.right]:
                    if child is not None:
                        next_level.append(child)
            out.append(values)
            current_level = next_level
        return "\n".join([str(x) for x in out])

    def draw(self):
        """Use NetworkX and Matplotlib to visualize the tree."""
        if self.root is None:
            return

        # Build the directed graph.
        G = nx.DiGraph()
        G.add_node(self.root.value)
        nodes = [self.root]
        while nodes:
            current = nodes.pop(0)
            for child in [current.left, current.right]:
                if child is not None:
                    G.add_edge(current.value, child.value)
                    nodes.append(child)

        # Plot the graph. This requires graphviz_layout (pygraphviz).
        nx.draw(G, pos=graphviz_layout(G, prog="dot"), arrows=True,
                with_labels=True, node_color="C1", font_size=8)
        plt.show()


class AVL(BST):
    """Adelson-Velsky Landis binary search tree data structure class.
    Rebalances after insertion when needed.
    """
    def insert(self, data):
        """Insert a node containing the data into the tree, then rebalance."""
        BST.insert(self, data)      # Insert the data like usual.
        n = self.find(data)
        while n:                    # Rebalance from the bottom up.
            n = self._rebalance(n).prev

    def remove(*args, **kwargs):
        """Disable remove() to keep the tree in balance."""
        raise NotImplementedError("remove() is disabled for this class")

    def _rebalance(self,n):
        """Rebalance the subtree starting at the specified node."""
        balance = AVL._balance_factor(n)
        if balance == -2:                                   # Left heavy
            if AVL._height(n.left.left) > AVL._height(n.left.right):
                n = self._rotate_left_left(n)                   # Left Left
            else:
                n = self._rotate_left_right(n)                  # Left Right
        elif balance == 2:                                  # Right heavy
            if AVL._height(n.right.right) > AVL._height(n.right.left):
                n = self._rotate_right_right(n)                 # Right Right
            else:
                n = self._rotate_right_left(n)                  # Right Left
        return n

    @staticmethod
    def _height(current):
        """Calculate the height of a given node by descending recursively until
        there are no further child nodes. Return the number of children in the
        longest chain down.
                                    node | height
        Example:  (c)                  a | 0
                  / \                  b | 1
                (b) (f)                c | 3
                /   / \                d | 1
              (a) (d) (g)              e | 0
                    \                  f | 2
                    (e)                g | 0
        """
        if current is None:     # Base case: the end of a branch.
            return -1           # Otherwise, descend down both branches.
        return 1 + max(AVL._height(current.right), AVL._height(current.left))

    @staticmethod
    def _balance_factor(n):
        return AVL._height(n.right) - AVL._height(n.left)

    def _rotate_left_left(self, n):
        temp = n.left
        n.left = temp.right
        if temp.right:
            temp.right.prev = n
        temp.right = n
        temp.prev = n.prev
        n.prev = temp
        if temp.prev:
            if temp.prev.value > temp.value:
                temp.prev.left = temp
            else:
                temp.prev.right = temp
        if n is self.root:
            self.root = temp
        return temp

    def _rotate_right_right(self, n):
        temp = n.right
        n.right = temp.left
        if temp.left:
            temp.left.prev = n
        temp.left = n
        temp.prev = n.prev
        n.prev = temp
        if temp.prev:
            if temp.prev.value > temp.value:
                temp.prev.left = temp
            else:
                temp.prev.right = temp
        if n is self.root:
            self.root = temp
        return temp

    def _rotate_left_right(self, n):
        temp1 = n.left
        temp2 = temp1.right
        temp1.right = temp2.left
        if temp2.left:
            temp2.left.prev = temp1
        temp2.prev = n
        temp2.left = temp1
        temp1.prev = temp2
        n.left = temp2
        return self._rotate_left_left(n)

    def _rotate_right_left(self, n):
        temp1 = n.right
        temp2 = temp1.left
        temp1.left = temp2.right
        if temp2.right:
            temp2.right.prev = temp1
        temp2.prev = n
        temp2.right = temp1
        temp1.prev = temp2
        n.right = temp2
        return self._rotate_right_right(n)


def prob4():
    """Compare the build and search times of the SinglyLinkedList, BST, and
    AVL classes. For search times, use SinglyLinkedList.iterative_find(),
    BST.find(), and AVL.find() to search for 5 random elements in each
    structure. Plot the number of elements in the structure versus the build
    and search times. Use log scales where appropriate.
    """
    with open('english.txt','r') as file:
        w = file.readlines()
    n_val = [2**i for i in range(3,11)]
    T1 = []
    T2 = []
    T3 = []
    T4 = []
    T5 = []
    T6 = []
    for n in n_val:
        samp = random.sample(w,n)

        start1 = time.perf_counter()
        S = SinglyLinkedList()
        for j in range(n):
            S.append(samp[j])
        end1 = time.perf_counter() - start1
        start2 = time.perf_counter()
        B = BST()
        for j in range(n):
            B.insert(samp[j])
        end2 = time.perf_counter() - start2
        start3 = time.perf_counter()
        A = AVL()
        for j in range(n):
            A.insert(samp[j])
        end3 = time.perf_counter() - start3

        T1.append(end1)
        T2.append(end2)
        T3.append(end3)

        find_samp = random.sample(samp,5)
        
        start4 = time.perf_counter()
        for k in range(5):
            S.iterative_find(find_samp[k])
        end4 = time.perf_counter() - start4
        start5 = time.perf_counter()
        for k in range(5):
            B.find(find_samp[k])
        end5 = time.perf_counter() - start5
        start6 = time.perf_counter()
        for k in range(5):
            A.find(find_samp[k])
        end6 = time.perf_counter() - start6

        T4.append(end4)
        T5.append(end5)
        T6.append(end6)
    D = [i for i in range(len(n_val))]
    plt.subplot(121)
    plt.loglog(D,T1)
    plt.loglog(D,T2)
    plt.loglog(D,T3)
    plt.subplot(122)
    plt.loglog(D,T4)
    plt.loglog(D,T5)
    plt.loglog(D,T6)
    
    plt.show()
