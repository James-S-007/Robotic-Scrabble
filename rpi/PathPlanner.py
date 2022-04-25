'''
    A* algorithm implementation
    Taken from: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
    All credit goes to the original creators
'''

import os.path
from pprint import pprint

from scrabble.Board import Board


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class PathPlanner():
    def __init__(self, board, human_rack, ai_rack, storage1, storage2, offsets, grid_size_rows=23, grid_size_cols=23):
        self.board = board
        self.human_rack = human_rack
        self.ai_rack = ai_rack
        self.storage1 = storage1
        self.storage2 = storage2
        self.offsets = offsets
        self.grid = [[0 for _ in range(grid_size_cols)] for _ in range(grid_size_rows)]  #
        self.init_grid_obstacles()
        self.update_global_grid()

    def init_grid_obstacles(self):
        # self.grid[18][16] = 1  # ai camera
        return # no grid obstacles rn with elevated camera

    # updates grid with current board, human_rack, ai_rack, storage1, storage2
    def update_global_grid(self):
        # set game board tiles
        offset = self.offsets['board']
        for i in range(0, len(self.board.board)):
            for j in range(0, len(self.board.board)):
                # emptys denoted by '-'
                if self.board.board[i][j] == '-':
                    self.grid[i+offset[0]][j+offset[1]] = 0
                else:
                    self.grid[i+offset[0]][j+offset[1]] = 1
        # set rack1
        offset = self.offsets['ai_rack']
        for i in range(0, len(self.ai_rack)):
            if not self.grid[i]:
                self.grid[offset[0]][i+offset[1]] = 0
            else:
                self.grid[offset[0]][i+offset[1]] = 1
        # set rack2
        offset = self.offsets['human_rack']
        for i in range(0, len(self.human_rack)):
            if not self.grid[i]:
                self.grid[offset[0]][i+offset[1]] = 0
            else:
                self.grid[offset[0]][i+offset[1]] = 1
        # set storage1
        offset = self.offsets['storage1']
        for i in range(0, len(self.storage1.letters)):
            for j in range(0, len(self.storage1.letters[0])):
                if self.storage1.letters[i][j] == 0:
                    self.grid[i+offset[0]][j+offset[1]] = 0
                else:
                    self.grid[i+offset[0]][j+offset[1]] = 1
        # set storage 2
        offset = self.offsets['storage2']
        for i in range(0, len(self.storage2.letters)):
            for j in range(0, len(self.storage2.letters[0])):
                if self.storage2.letters[i][j] == 0:
                    self.grid[i+offset[0]][j+offset[1]] = 0
                else:
                    self.grid[i+offset[0]][j+offset[1]] = 1


    def astar(self, start, end):
        """Returns a list of tuples as a path from the given start to the given end in the given board"""
        # This is very jank but need a quick solution, will assume start/end are unoccupied for planning and reset after
        initial_start_state = self.grid[start[0]][start[1]]
        initial_end_state = self.grid[end[0]][end[1]]
        self.grid[start[0]][start[1]] = 0
        self.grid[end[0]][end[1]] = 0
        # Create start and end node
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                # reset grid start and end points before returning
                self.grid[start[0]][start[1]] = initial_start_state
                self.grid[end[0]][end[1]] = initial_end_state
                return path[::-1] # Return reversed path

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(self.grid) - 1) or node_position[0] < 0 or node_position[1] > (len(self.grid[len(self.grid)-1]) -1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if self.grid[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)


    # Reduces path from every point to manhattan
    def simplify_path(self, path):
        if len(path) <= 2:
            return path  # start and end node
        simplified_path = []
        simplified_path.append(path[0])
        curr_path_axis = 0 if path[0][0] == path[0][0] else 1  # 0 if traveling along x-axis, 1 if traveling along y-axis
        for i in range(1, len(path) - 1):
            if path[i+1][curr_path_axis] == path[i][curr_path_axis]:
                continue
            simplified_path.append(path[i])
            curr_path_axis = 1 - curr_path_axis  # toggle axis travling
        simplified_path.append(path[-1])  # add end node
        return simplified_path


# Test function : DEPRECATED, test with Gantry class that encapsulated PathPlanner
def main():
    board = Board()
    board.import_board(os.path.join(os.path.dirname(__file__), 'scrabble', 'board.csv'))
    pathplanner = PathPlanner(board, None, None, None, None, None)
    print('Current Board')
    pprint(pathplanner.board.board)
    path = pathplanner.astar((0, 0), (4, 7))
    print(f'Complete Path: {path}')
    print(f'Simplified Path: {pathplanner.simplify_path(path)}')

if __name__ == '__main__':
    main()