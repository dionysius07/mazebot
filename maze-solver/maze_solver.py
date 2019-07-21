import requests
import json

class MazeSolver(object):
    """
    This class contains methods used to solve a grid maze. 
    Arguments: grid maze (nxn list)
    Calling execute() will return a string with directions from
    start to finish.
    """
    def __init__(self,maze):
        # Set up data members containing the map, row & column limits, 
        # start & end positions:
        self.maze_map = maze["map"]
        self.R = len(maze["map"])
        self.C = len(maze["map"][0])
        self.start_row = maze["startingPosition"][1]
        self.start_col = maze["startingPosition"][0]
        self.end_row = maze["endingPosition"][1]
        self.end_col = maze["endingPosition"][0]

        # Row and Column queues for BFS:
        self.rq = []
        self.cq = []

        # Step tracking for BFS:
        self.moves = 0
        self.nodes_upcoming = 0
        self.nodes_left = 1

        # Check flag for if we have reached the end:
        self.reached = False

        # Check if we already visited a node:
        self.visited = [[False for col in range(self.C)] for row in range(self.R)]

        # Track which node we came from:
        self.tracker = [[None for col in range(self.C)] for row in range(self.R)]

        # Direction vectors for exploring relative to current node:
        self.dr = [-1,1,0,0]
        self.dc = [0,0,-1,1]

        # Variables to store the path and directions to get to the end:
        self.path = []
        self.directions = []

    def explore(self,rowindex,colindex):
        """
        With respect to current node, check up, down, left right
        """
        for i in range(4):
            # Get index of node to check:
            rr = self.dr[i] + rowindex
            cc = self.dc[i] + colindex
            # If node being checked is out of bounds, skip:
            if rr < 0 or cc < 0: continue
            if rr >= self.R or cc >= self.C: continue
            # If node being checked is a wall or already visited, skip:
            if self.visited[rr][cc]: continue
            if self.maze_map[rr][cc] == "X": continue
            # Save valid nodes to queue:
            self.rq.append(rr)
            self.cq.append(cc)
            # Mark node as visited and update the tracker to record where we came from:
            self.visited[rr][cc] = True
            self.tracker[rr][cc] = [rowindex,colindex]
            self.nodes_upcoming += 1
    
    def solve(self):
        """
        Execute a breadth-first search over the grid to find the shortest path
        """
        # Seed queue with start position:
        self.rq.append(self.start_row)
        self.cq.append(self.start_col)
        self.visited[self.start_row][self.start_col] = True
        # Add a unique tracker for the start position for use by the path generator:
        self.tracker[self.start_row][self.start_col] = ["H","H"]

        # Iteratively check all nodes of the grid till goal is reached or all nodes are sampled:
        while len(self.rq) > 0:
            r = self.rq.pop(0)
            c = self.cq.pop(0)

            if self.maze_map[r][c] == "B":
                self.reached = True
                break
            self.explore(r,c)
            self.nodes_left -= 1

            if self.nodes_left == 0:
                self.nodes_left = self.nodes_upcoming
                self.nodes_upcoming = 0
                self.moves += 1
        
        if self.reached:
            return self.moves
        
        return -1

    def path_generator(self):
        """
        Start at the end and work backwards to the start to record the path
        """
        backwards = [self.end_row,self.end_col]
        self.path.insert(0,backwards)
        # Keep recording the path till unique start marker is reached:
        while backwards != ["H","H"]:
            step = self.tracker[backwards[0]][backwards[1]]
            self.path.insert(0,step)
            backwards = step
        self.path = self.path[1:]

    def direction_generator(self):
        """
        Make a string holding the cardinal directions to follow from start to end
        """
        # Check subsequent steps in the path against the previous one to find out which way we went:
        for i in range(len(self.path)):
            now = self.path[i]
            prev = self.path[i-1]
            if now[0]>prev[0] and now[1]==prev[1]:
                self.directions.append("S")
            elif now[0]<prev[0] and now[1]==prev[1]:
                self.directions.append("N")
            elif now[1]>prev[1] and now[0]==prev[0]:
                self.directions.append("E")
            elif now[1]<prev[1] and now[0]==prev[0]:
                self.directions.append("W")

    def execute(self):
        """
        Runs the solver and returns directions
        """
        # First check if goal was reached:
        moves = self.solve()
        if moves != -1:
            self.path_generator()
            self.direction_generator()
        else:
            return "Could not find goal!"
        return ''.join(self.directions)
