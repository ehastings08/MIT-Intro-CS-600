# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random
import numpy

import ps6_visualize
import pylab

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)
    def __str__(self):
        """Prints a string representation of the Position object"""
        return '<Position at (%.2f, %.2f)>' % (self.x, self.y)

# Added function
def get_min_distance(pos, dict_of_pos):
    '''Accepts a Position object and a dictionary with (x,y) coordinate tuples as keys.
    Calculates the minimum distance between each available coordinate and returns that coordinate Position as the best match'''
    
    distance_list = []
    min_dist = 0
    
    for key in dict_of_pos:
        dist = math.hypot(key[0] - pos.getX(), key[1] - pos.getY())
        if len(distance_list) == 0:
            distance_list.append(dist)
            min_dist = dist
            coord = key
        elif dist < min(distance_list):
            min_dist = dist
            coord = key
            distance_list.append(dist)
                
    return coord
        
# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.
        width: an integer > 0
        height: an integer > 0
        """
        # Initialize a width, height, and a mapping of tiles. Map coordinate to clean/dirty flag.
        self.width = width
        self.height = height
        # Now create a dict with coordinates and flags.
        self.room_dict = {}
        for w in range(width):
            for h in range(height):
                self.room_dict[(w, h)] = False   # False = dirty, True = clean
    
    def getTileAtPosition(self, pos):
        """
        Return the tile at a given position
        Assumes that POS represents a valid position inside this room.
        pos: a Position object
        """

        # Determine what center coordinate that position is closest to
        x = math.floor(pos.getX())
        y = math.floor(pos.getY())
        return Position(x, y)
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned using True = clean and False = dirty.
        Assumes that POS represents a valid position inside this room.
        pos: a Position object
        """

        x = math.floor(pos.getX())
        y = math.floor(pos.getY())
        self.room_dict[(x, y)] = True

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.
        Assumes that (m, n) represents a valid tile inside the room.
        m: an integer (EH: A FLOAT)
        n: an integer (EH: A FLOAT)
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.room_dict[(m,n)]
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.
        returns: an integer
        """
        return len(self.room_dict)

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.
        returns: an integer
        """
        return sum(self.room_dict.values())  # Returns number of True Boolean flags in values of room dict

    def getPercentCleanedTiles(self):
        """
        Return the % of tiles in the room that are clean
        returns: a float
        """
        return float(self.getNumCleanedTiles())/float(self.getNumTiles())
    
    def getRandomPosition(self):
        """
        Return a random position inside the room. 
        returns: a Position object.
        """
        # Assign random position from self.room_dict
        return Position(random.random() * self.width, random.random() * self.height)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.
        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return (0 <= pos.getX() < self.width) and (0 <= pos.getY() < self.height)
    
    def __str__(self):
        """Prints a string representation of the RectangularRoom class"""
        return '<RectangularRoom with (w, h) = (%.2f, %.2f), with %.2f clean and %.2f total tiles, for a total of %.2f pct clean tiles>' % (self.width, self.height, self.getNumCleanedTiles(), self.getNumTiles(), float(self.getNumCleanedTiles())/float(self.getNumTiles()))


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    **Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.position = self.room.getRandomPosition()
        self.direction = random.randrange(360)

    def __str__(self):
        '''String representation of Robot object'''
        return '<Robot w/ speed %.2f, position (%.2f, %.2f), direction %.2f>' % (self.speed, self.position.getX(), self.position.getY(), self.direction)
    
    def getRobotPosition(self):
        """
        Return the position of the robot.
        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.
        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.
        position: a Position object.
        """
        self.position = position
        return self.position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction
        return self.direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.
        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        This will be created by the Robot subclass, so this method is empty.
        """
        raise NotImplementedError
        

# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.
    At each time-step, a StandardRobot attempts to move in its current direction; 
    ****when it hits a wall, it chooses a new direction randomly.
    """
    
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        candidatePosition = self.position.getNewPosition(self.direction, self.speed)
        if self.room.isPositionInRoom(candidatePosition):
            self.setRobotPosition(candidatePosition)
            self.room.cleanTileAtPosition(self.position)
        else:
            self.direction = random.randrange(360)
            
        # Add code to cleaning step to print what's happening
        

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type, visualize):
    """
    Runs NUM_TRIALS trials of the simulation and returns
    the mean number of time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    visualize: Boolean; determines whether or not to visualize with an animation
    """
    
    # Step 1 - Create empty list of robots
    total_time_steps = 0.0
    robotCollection = []
    
    # Step 2 - Run trials of simulation
    for t in range(0, num_trials):
        # print 'Starting trial %d' % t
        if visualize:
            anim = ps6_visualize.RobotVisualization(num_robots, width, height)
        room = RectangularRoom(width, height)
        # Loop through robots to add to collection
        # print 'Adding a robot to the list.'
        for i in range(num_robots):
            robotCollection.append(robot_type(room, speed))
        # print 'Number of robots is now %s' % len(robotCollection)
        # If visualizing, at each time-step draw a new frame of the animation
        if visualize:
            anim.update(room, robotCollection)
        # Now update tiles 
        # print 'Starting update position and clean'
        # print 'Current percent cleaned tiles before while loop is: %s' % room.getPercentCleanedTiles()
        while room.getPercentCleanedTiles() < min_coverage:
            for robot in robotCollection:
                # print 'Robot %s cleans tile!' % robot
                robot.updatePositionAndClean()
                # print 'Room now has %d cleaned tiles' % room.getNumCleanedTiles()
            total_time_steps += 1   # Update time steps at each run through robot list
            if visualize:
                anim.update(room, robotCollection)
        if visualize:
            anim.done()
    
    # print 'Total time steps was: %d' % (total_time_steps)
    # print 'Number of trials was: %d' % (num_trials)
    # print 'Average : '
    # Step 3 - Return the mean number of time steps (# time steps / num trials) needed
    return total_time_steps / num_trials
    
    
# === Problem 4
#
# 1) How long does it take to clean 80 percent of a 20 by 20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80 percent of rooms with dimensions 
#	 20x20, 25x16, 40x10, 50x8, 80x5, and 100x4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """ 
    # Pylab plots take x, y : pylab.plot(x, y)
    # Axis labels + titles are made by : pylab.xlabel/ylabel('this is x') & pylab.title('My Plot')
    
    # Step 1. Initialize variables
    num_robots = 10
    width = 20
    height = 20
    min_coverage = .8
    num_trials = 20
    
    # Step 1. Create x-axis - a list of # of robots - and y-axis - an empty list for times
    
    x = range(1, num_robots + 1)
    y = []
    
    # Step 2. Create y-axis - for each robot #, the time it takes to clean 80% of 20 x 20 room
    # Loop through robots in robot list
    for i in x:
        y_val = runSimulation(i, 1, width, height, min_coverage, num_trials, StandardRobot, False)
        y.append(y_val)
    
    # Step 3. Create graph and labels
    pylab.plot(x, y)
    pylab.xlabel('Time to clean 80/% of a 20 x 20 room given a certain number of robots')
    pylab.ylabel('Time / Steps')
    pylab.title('Robots by Time')
    pylab.show()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    
    # Step 1. Initialize variables
    num_robots = 2
    rooms = [(20,20), (25,16), (40,10), (50,8), (80,5), (100,4)]
    min_coverage = .8
    num_trials = 100
    
    x = []
    y = []
    
    # Step 2 - Set x and y values, where x is the ratio of width to height and y is the mean time 
    for room in rooms:
        y_val = runSimulation(num_robots, 1, room[0], room[1], min_coverage, num_trials, StandardRobot, False)
        y.append(y_val)
        x_val = float(room[0]) / float(room[1]) # Ratio width to height
        x.append(x_val)
        
    # Step 3. Create graph and labels
    pylab.plot(x, y)
    pylab.xlabel('Time to clean 80/% of a square room with 2 robots for various room sizes')
    pylab.ylabel('Time / Steps')
    pylab.title('Robots Area')
    pylab.show()

# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.
        Move the robot to a new position using a RANDOM direction and mark the tile it is on as having been cleaned.
        """
        
        random_direction = random.randrange(360)
        candidatePosition = self.position.getNewPosition(random_direction, self.speed)
        if self.room.isPositionInRoom(candidatePosition):
            self.setRobotPosition(candidatePosition)
            self.room.cleanTileAtPosition(self.position)
        else:
            self.direction = random.randrange(360)

# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    
    # Step 0 - Initialize variables
    num_robots = 10
    width = 10
    height = 10
    min_coverage = .8
    num_trials = 20
    
    # Step 1. Create x-axis - a list of # of robots - and y-axis - an empty list for times
    
    x = range(1, num_robots + 1)
    y1 = []
    y2 = []
    
    # Step 2. Create y-axis - for each robot #, the time it takes to clean 80% of 20 x 20 room
    # Standard Robot
    for i in x:
        y_val_1 = runSimulation(i, 1, width, height, min_coverage, num_trials, StandardRobot, False)
        y1.append(y_val_1)
    for i in x:
        y_val_2 = runSimulation(i, 1, width, height, min_coverage, num_trials, RandomWalkRobot, False)
        y2.append(y_val_2)
    
    # Step 3. Create graph and labels
    pylab.plot(x, y1)
    pylab.plot(x, y2)
    pylab.xlabel('Time to clean 80/% of square room with 10 robots')
    pylab.ylabel('Time / Steps')
    pylab.title('Robots by Time')
    
    # pylab.bar([0,1], y1, .5, alpha=0.5, color = 'b', yerr = 0, label = 'Standard')
    # pylab.bar([0,1], y2, .5, alpha=0.5, color = 'r', yerr = 0, label = 'Random')
    # pylab.xlabel('Type of Robot used')
    # pylab.ylabel('Time to clean 80/% of square room with 10 robots')
    # pylab.title('Robots by Type')
    # pylab.legend()
    
    pylab.show()

# # # # Tests
# print '\n\n\n\n===================================='
# myRoom = RectangularRoom(10, 20)
# print 'Initialized myRoom as an instance of RectangularRoom(10, 20)'
# print '======================================='
# print 'Testing __str__ method of RectangularRoom object: '
# print myRoom
# print '======================================='
# pos1 = Position(2.3, 3.4)
# pos2 = Position(3.5, 9.4)
# pos3 = Position(6.0, 7.2)
# pos4 = Position(2.5, 3.5)
# print 'Created four positions'
# print '======================================='
# print 'Testing __str__ method of Position object: '
# print pos1
# print '======================================='
# print '======================================='
# print 'Cleaning tiles at (2.3, 3.4), (3.5, 9.4), (6.0, 7.2), and (2.5, 3.5)'
# myRoom.cleanTileAtPosition(pos1)
# print myRoom
# myRoom.cleanTileAtPosition(pos2)
# print myRoom
# myRoom.cleanTileAtPosition(pos3)
# print myRoom
# myRoom.cleanTileAtPosition(pos4)
# print myRoom
# print '======================================='
# print 'Checking if a tile is cleaned - should be True.'
# print myRoom.isTileCleaned(2, 3)
# print '======================================='
# print 'Getting the number of tiles:'
# print myRoom.getNumTiles()
# print '======================================='
# print 'Getting the number of cleaned tiles:'
# print myRoom.getNumCleanedTiles()
# print '======================================='
# print 'Getting a random position: '
# random_pos = myRoom.getRandomPosition()
# print 'Random position x/y: '
# print random_pos.getX(), random_pos.getY()
# print '======================================='
# print 'Checking if (1.2, 4.3) in room: ',
# print myRoom.isPositionInRoom(Position(1.2, 4.3))
# print 'Checking if (1.2, 21.1) in room:',
# print myRoom.isPositionInRoom(Position(1.2, 21.1))
# print '======================================='
# print 'Initializing myRobot as an instance of Robot(myRoom, 1.0)'
# print '======================================='
# myRobot = Robot(myRoom, 1.0)
# print 'myRobot position is: '
# robot_pos = myRobot.getRobotPosition()
# print 'Robot pos x/y is: ', robot_pos.getX(), robot_pos.getY()
# print '======================================='
# print 'myRobot direction is: '
# print myRobot.getRobotDirection()
# print '======================================='
# print 'Setting myRobot position to pos2'
# print myRobot.setRobotPosition(pos2)
# print myRobot.getRobotPosition().getX()
# print myRobot.getRobotPosition().getY()
# print '======================================='
# rand_dir = random.randrange(0, 361)
# print 'Setting myRobot direction to %.2f ' % rand_dir
# print myRobot.setRobotDirection(rand_dir)
# print myRobot.getRobotDirection()
# print '======================================='
# print 'Setting standard_robot to an instance of StandardRobot():'
# standard_robot = StandardRobot(myRoom, 1.0)
# print standard_robot
# print '======================================='
# print 'Testing updatePositionAndClean method of StandardRobot: '
# print standard_robot.updatePositionAndClean()
# print myRoom
# print standard_robot.updatePositionAndClean()
# print myRoom
# print standard_robot.updatePositionAndClean()
# print myRoom
# print '======================================='
# print 'Testing implementation of runSimulation(): '
# print runSimulation(2, 1, 10, 10, .5, 5, StandardRobot, True)
# print '======================================='
# print 'Running showPlot1(): '
# showPlot1()
# print '======================================='
# print 'Running showPlot2(): '
# showPlot2()
# print '======================================='
# print runSimulation(2, 1, 10, 10, .5, 5, RandomWalkRobot, True)
# print '======================================='
# print 'Testing ShowPlot3() comparing Standard to RandomWalk Robot: '
# showPlot3()