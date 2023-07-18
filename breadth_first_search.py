# breadth_first_search.py


from collections import deque
import networkx as nx
from matplotlib import pyplot as plt


class Graph:
    """A graph object, stored as an adjacency dictionary. Each node in the
    graph is a key in the dictionary. The value of each key is a set of
    the corresponding node's neighbors.

    Attributes:
        d (dict): the adjacency dictionary of the graph.
    """
    def __init__(self, adjacency={}):
        """Store the adjacency dictionary as a class attribute"""
        self.d = dict(adjacency)

    def __str__(self):
        """String representation: a view of the adjacency dictionary."""
        return str(self.d)

    def add_node(self, n):
        """Add n to the graph (with no initial edges) if it is not already
        present.

        Parameters:
            n: the label for the new node.
        """
        if n not in self.d:
            self.d[n] = set()

    def add_edge(self, u, v):
        """Add an edge between node u and node v. Also add u and v to the graph
        if they are not already present.

        Parameters:
            u: a node label.
            v: a node label.
        """
        if u not in self.d:
            self.d[u] = set()
        if v not in self.d:
            self.d[v] = set()
        self.d[u].add(v)
        self.d[v].add(u)

    def remove_node(self, n):
        """Remove n from the graph, including all edges adjacent to it.

        Parameters:
            n: the label for the node to remove.

        Raises:
            KeyError: if n is not in the graph.
        """
        if n not in self.d:
            raise KeyError('Node not in graph')
        self.d.pop(n)
        for i in self.d:
            if n in self.d[i]:
                self.d[i].remove(n)

    def remove_edge(self, u, v):
        """Remove the edge between nodes u and v.

        Parameters:
            u: a node label.
            v: a node label.

        Raises:
            KeyError: if u or v are not in the graph, or if there is no
                edge between u and v.
        """
        if u not in self.d:
            raise KeyError('Node \'u\' not in graph')
        if v not in self.d:
            raise KeyError('Node \'v\' not in graph')
        if u not in self.d[v] or v not in self.d[u]:
            raise KeyError('Edge does not exist')
        self.d[u].remove(v)
        self.d[v].remove(u)

    def traverse(self, source):
        """Traverse the graph with a breadth-first search until all nodes
        have been visited. Return the list of nodes in the order that they
        were visited.

        Parameters:
            source: the node to start the search at.

        Returns:
            (list): the nodes in order of visitation.

        Raises:
            KeyError: if the source node is not in the graph.
        """
        if source not in self.d:
            raise KeyError('Source node not in graph')
        #create deque, list and set
        current = source
        Q = deque()
        order = []
        M = set()
        Q.append(current)
        M.add(current)
        #loop through Q removing first element until empty
        while len(Q) != 0:
            #if node is already in the order remove it
            current = Q.popleft()
            order.append(current)
            #
            for val in self.d[current]:
                if val not in M:
                    M.add(val)
                    Q.append(val)
        return order

    def shortest_path(self, source, target):
        """Begin a BFS at the source node and proceed until the target is
        found. Return a list containing the nodes in the shortest path from
        the source to the target, including endoints.

        Parameters:
            source: the node to start the search at.
            target: the node to search for.

        Returns:
            A list of nodes along the shortest path from source to target,
                including the endpoints.

        Raises:
            KeyError: if the source or target nodes are not in the graph.
        """
        #raise appropriate errors
        if source not in self.d:
            raise KeyError('Source node not in graph')
        if target not in self.d:
            raise KeyError('Target node not in graph')
        
        queue = deque()
        marked = set()
        queue.append((source,list(source)))
        marked.add(source)
        #loop through Q removing first element until empty
        while len(queue) != 0:
            #if node is already in the order remove it
            current,current_path = queue.popleft()
            #
            if current == target:
                return current_path
            #
            for val in self.d[current]:
                if val not in marked:
                    marked.add(val)
                    queue.append((val,current_path + list(val)))


class MovieGraph:
    """Class for solving the Kevin Bacon problem with movie data from IMDb."""

    def __init__(self, filename="movie_data.txt"):
        """Initialize a set for movie titles, a set for actor names, and an
        empty NetworkX Graph, and store them as attributes. Read the speficied
        file line by line, adding the title to the set of movies and the cast
        members to the set of actors. Add an edge to the graph between the
        movie and each cast member.

        Each line of the file represents one movie: the title is listed first,
        then the cast members, with entries separated by a '/' character.
        For example, the line for 'The Dark Knight (2008)' starts with

        The Dark Knight (2008)/Christian Bale/Heath Ledger/Aaron Eckhart/...

        Any '/' characters in movie titles have been replaced with the
        vertical pipe character | (for example, Frost|Nixon (2008)).
        """
        self.movies = set()
        self.actors = set()
        self.nxg = nx.Graph()


        with open(filename, encoding='utf-8', mode='r') as file:
            lines = file.readlines()
        for line in lines:
            #making line a list split by name
            line = line.strip()
            line = line.split('/')
            line0 = line[0]
            #Adding elements to class attributes
            self.movies.add(line0)
            line_set = [(i,line0) for i in line[1:]]
            for j in range(len(line_set)):
                self.actors.add(line_set[j][0])
            #add edges to nx Graph
            self.nxg.add_edges_from(line_set)

    def path_to_actor(self, source, target):
        """Compute the shortest path from source to target and the degrees of
        separation between source and target.

        Returns:
            (list): a shortest path from source to target, including endpoints and movies.
            (int): the number of steps from source to target, excluding movies.
        """
        #compute shortest path
        short_path = list(nx.shortest_path(self.nxg,source,target))
        return short_path, len(short_path)//2

    def average_number(self, target):
        """Calculate the shortest path lengths of every actor to the target
        (not including movies). Plot the distribution of path lengths and
        return the average path length.

        Returns:
            (float): the average path length from actor to target.
        """
        #find shortest paths between every acter and the target
        data = nx.shortest_path_length(self.nxg, target)
        bins = [i-.5 for i in range(8)]

        #save the numbers for actors only
        lengths = [data[j] // 2 for j in self.actors]
        avg = sum(lengths) / len(lengths)

        #plot the histogram
        plt.hist(lengths,bins)
        plt.title('Distribution of ' + target + ' Numbers')
        plt.xlabel('Path Lengths')
        plt.ylabel('Frequency')
        plt.show()

        return avg
