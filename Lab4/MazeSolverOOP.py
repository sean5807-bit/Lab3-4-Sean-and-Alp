"""
CS 1301 Robotics Track - Lab 4
Maze Solver
Spring - 2026
"""

# DO NOT MODIFY THESE LINES OF CODE
##################################################################################
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note
from collections import deque

import math as m # Math module is imported for your use
##################################################################################

# robot is the instance of the robot that will allow us to call its methods.
robot = Create3(Bluetooth())

"""
Helpful Reminders:
Refer to the following Canvas pages for initial help with this assignment:
    - IR Sensors
    - Global Variables
    - Asynchronus Functions
    - Robot Navigation
    - Boolean Flag Variables (I, II, & III)

Work on the Autograded functions in LabX_Aux.py and check them before implementing
them here.

Stop by Office Hours or make a post on Ed Discussion for additional help!
(Refer to the Ed Discussion Guidelines)

My Notes:
"""

# === FLAG VARIABLES
HAS_COLLIDED = False
HAS_ARRIVED = False

# === MAZE CONSTANTS
N_X_CELLS = 3
N_Y_CELLS = 3
CELL_DIM = 50

# === ROBOT STATE VARIABLES
PREV_CELL = None
START = (0,1)
CURR_CELL = START
DESTINATION = (1,0)

# === PROXIMITY TOLERANCES
WALL_THRESHOLD = 80

# ==========================================================
# Object-Oriented Maze Representation

class Cell:
    # Represents a single cell in the maze's grid
    def __init__(self, x, y):
        # Initializes a cell with its coordinates and default attributes
        pass

class Maze:
    # Manages the grid of Cells and handles maze-wide algorithms
    def __init__(self, nXCells, nYCells):
        # Initializes the maze grid with Cell objects
        pass

    def get_cell(self, coords):
        # Safely retrieves a cell object from the grid
        pass

    def add_all_neighbors(self, nXCells, nYCells):
        # Initializes all potential neighbors for every cell
        pass

    def update_neighbors(self, current_coords, navigable_neighbors):
        # Updates the neighbors for a cell based on wall detection
        pass

    def update_costs(self, goal_coords):
        # Runs the flood-fill algorithm to update the cost for every cell
        for cell in self.grid.values():
            cell.flooded = False

        goal_cell = self.get_cell(goal_coords)
        if not goal_cell: return

        queue = deque([goal_cell])
        goal_cell.cost = 0
        goal_cell.flooded = True

        while queue:
            current = queue.popleft()
            for neighbor_coords in current.neighbors:
                neighbor_cell = self.get_cell(neighbor_coords)
                if neighbor_cell and not neighbor_cell.flooded:
                    neighbor_cell.flooded = True
                    neighbor_cell.cost = current.cost + 1
                    queue.append(neighbor_cell)

    def get_next_cell(self, current_coords):
        # Determines the best neighboring cell to move to
        pass

# ==========================================================
# FAIL SAFE MECHANISMS

@event(robot.when_touched, [True, True])
async def when_either_button_touched(robot):
    pass

@event(robot.when_bumped, [True, True])
async def when_either_bumped(robot):
    pass

# ==========================================================
# Helper Functions

def getRobotOrientation(heading):
    pass

def getPotentialNeighbors(currCell, orient):
    pass

def getWallConfiguration(IR0, IR3, IR6, threshold):
    pass

def getNavigableNeighbors(wallsAroundCell, possibleNeighbors, prevCell, nXCells, nYCells):
    pass

def checkCellArrived(currentCell, dest):
    pass

# ==========================================================
# INITIALIZE MAZE OBJECT

# Create an instance of the Maze class
maze = Maze(N_X_CELLS, N_Y_CELLS)

# Mark the starting cell as visited within the maze object
maze.get_cell(CURR_CELL).visited = True

# ==========================================================
# EXPLORATION AND NAVIGATION

async def navigateToNextCell(robot, nextCell, orient):
    global maze, PREV_CELL, CURR_CELL, CELL_DIM
    pass

@event(robot.when_play)
async def navigateMaze(robot):
    global HAS_COLLIDED, HAS_ARRIVED
    global PREV_CELL, CURR_CELL, START, DESTINATION
    global maze, N_X_CELLS, N_Y_CELLS, CELL_DIM, WALL_THRESHOLD
    # DO NOT MODIFY THESE LINES OF CODE
    # DO NOT PUT ANY CODE BEFORE THIS SECTION
    ##################################################################################
    # Check the battery level and return a warning message
    battery = await robot.get_battery_level()
    print('Battery:', battery[0], 'mV; ', battery[1], '%')
    if battery[1] <= 30:
        print("Low battery. Charge the robot, otherwise it may not behave as intended.")
    ##################################################################################
    
    # The main loop will now call methods on the 'maze' object
    pass

robot.play()