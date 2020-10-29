"""
Oliver Stappas, 1730124
Wednesday, February 20
R. Vincent, instructor
Assignment 2
"""


# Main program for assignment 2. Your job here is to finish the
# Solver class's __init__ method to solve the puzzle as described
# in the handout.
#
from MinPQ import MinPQ
from Board import Board

import functools
@functools.total_ordering
class Node(object):
    def __init__(self, bd, moves, node):
        '''Construct a new node object.'''
        self.board = bd         # save the board
        self.moves = moves      # number of moves to reach this board.
        self.cost = bd.distance() # save the distance metric.
        self.previous = node      # save the previous node.
    def __gt__(self, other):
        '''A node is 'greater' than another if the cost plus the
        number of moves is larger. Note that this code will fail
        if 'other' is None.'''
        return (self.cost + self.moves) > (other.cost + other.moves)
    def __eq__(self, other):
        '''Two nodes are equal if the sum of the cost and moves are
        the same. The board itself is ignored.'''
        if self is other:       # comparing to itself?
            return True
        if other is None:       # comparing to None
            return False
        return (self.cost + self.moves) == (other.cost + other.moves)
  
class Solver(object):
    def __init__(self, initial):
        '''Initialize the object by finding the solution for the
        puzzle.'''
        self.__solvable = False # Is the board solvable?
        self.__trace = [] # List of all boards checked
        # This is where your code to solve the puzzle will go!
        queue = MinPQ() # Creating a MinPQ
        initial_node = Node(initial, 0, None) # Creating a node based on the initial Board ( initial is th board, 0 moves, no node)
        queue.insert(initial_node) # Inserting the initial node on the queue
        self.number_of_boards_checked = 0 # Initialize a value for the number of boards checked for solutions
        while not queue.isEmpty(): # While the queue isn't empty
            best_node = queue.delMin() # Remove the "best" Node from the priority queue
            best_board = best_node.board # Get the board associated with a node
            self.number_of_boards_checked += 1 # Increase the number of boards checked by one
            if best_board.solved(): # If the board (node) is solved
                self.__solvable = True # It must be solvable
                current_node = best_node # The current node is the best node
                while current_node: # While there still a node to check
                    self.__trace.append(current_node.board) # Append a board to the list of boards checked
                    current_node = current_node.previous # Make the new node to check the node before the current one
                self.__trace.reverse() # Reverse the list of boards checked to make it the proper order
                break
            else:
                for neighbor_board in best_board.neighbors(): # For every neighbor of every board
                    if not best_node.previous or neighbor_board != best_node.previous.board: # If there isn't a previous board (back to start) or a neighbor board isn't one we've already checked previously
                        neighbor_node = Node(neighbor_board, best_node.moves + 1, best_node) # Creating a node based on a neighbor Board (1 more move than the current move, previous is best_node)
                        queue.insert(neighbor_node) # Inserting the neighbor node node on the queue 

    def solvable(self):
        '''Returns True if this puzzle can be solved.'''
        return self.__solvable;
  
    def moves(self):
        '''Returns the number of moves in the solution, or -1 if
        not solvable.'''
        return len(self.__trace) - 1 if self.__solvable else -1
  
    def solution(self):
        '''Returns the list of board positions in the solution.'''
        return self.__trace.copy()

# Add your main program here. It should prompt for a file name, read
# the file, and create and run the Solver class to find the solution
# for the puzzle. Then it should print the result (see the example output
# file for details).
#

file_name = 'puzzles/' + input('Please enter a puzzle file name: ') # Ask user to input the puzzle file name with the puzzles/ path already included
file = open(file_name) # Open the the puzzle file
board_string = file.read().replace('\n', '') # Read the file and replace all the '\n' by empty spaces
file.close() # Close the file
initial_board = Board(board_string) # Create an initial board object from the Board class and the board string
solver = Solver(initial_board) # Make a solver object based on the initial board
if solver.solvable(): # If the solver object is solvable:
    print('Minimum number of moves = {}'.format(solver.moves()))
    #print('Number of boards checked = {}'.format(solver.number_of_boards_checked))#       # This code was used to check the total number of boards checked for Part 2 
    for i, b in enumerate(solver.solution()): # Use i to count how many different moves are made through b, which is each different board associated with each move
        print('Move # {}'.format(i)) # Prints how many moves were needed to find the solution
        print(b) # Prints all the boards associated with each move



