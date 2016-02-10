# 6.00 Problem Set 11
#
# ps11.py
#
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
from graph import Digraph, Edge, Node, FeatureEdge

#
# Problem 2: Building up the Campus Map
# Write a couple of sentences describing how you will model the
# problem as a graph)
#

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    mapGraph = Digraph()
    
    print "Loading map from file..."
    inputFile = open(mapFilename)
    for line in inputFile:
        line = line.rstrip()
        splitLine = line.split(' ')
        
        # First, add start node if it doesn't already exist
        if not mapGraph.hasNode(splitLine[0]):
            mapGraph.addNode(splitLine[0])
            
    inputFile.seek(0)        
    
    for line in inputFile:
        line = line.rstrip()
        splitLine = line.split(' ')
            
        # Then, add edge between two nodes
        lineEdge = FeatureEdge(splitLine[0],splitLine[1],splitLine[2],splitLine[3])
        mapGraph.addEdge(lineEdge)
        
    return mapGraph

#
# Problem 3: Finding the Shortest Path using Brute Force Search
# State the optimization problem as a function to minimize
# and the constraints
#

def getDistance(digraph, nodeList, featureDist=False):
    '''Used to implement maxDistance constraints
    Parameters:
        digraph: instance of class Digraph
        nodeList: a list of nodes for which the distance will be calculated
        featureDist: a Boolean representing whether or not feature specific distance should be used. If False, use regular distance. 
    Returns:
        an integer representing the distance (either total or outdoors) between all nodes in path
    '''
    total_distance = 0
    
    if nodeList == None:
        return 0
    for node in nodeList:
        if not digraph.hasNode(node):
            print '!!!!!!! getDistance failed. Invalid node entered: %s' % node
            exit()
    for i in range(len(nodeList)-1):
        # print 'Current node: ',nodeList[i]
        # print 'Next node: ', nodeList[i+1]
        edge = digraph.getEdge(nodeList[i],nodeList[i+1])
        if not digraph.hasEdge(edge):
            print '!!!!!!! getDistance failed. Invalid edge entered: %s' % edge
            exit()
        # print 'Edge between nodes: ',edge
        # print 'Distance between nodes: ',edge.getDistance()
        # print 'Feature between nodes: ',edge.getFeature()
        if not featureDist:
            total_distance += int(edge.getDistance())
        else:
            total_distance += int(edge.getFeature())
        return total_distance

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors, toPrint = False, visited = []):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
        
    if toPrint: #for debugging
        print start, end
        
    if not (digraph.hasNode(start) and digraph.hasNode(end)):
        raise ValueError('Start or end not in graph.')
    
    # Convert path to a list of strings starting w/start node; set visited and shortest variables
    path = [str(start)]
    shortest = None
    
    # Base case - once start = end return path
    if start == end:
        return path
    
    # Iterate thruogh child nodes of the start node
    for node in digraph.childrenOf(start):
        # If haven't already visited node....
        if (str(node) not in visited): #avoid cycles
            # Add the node to the visited list if not yet visited
            visited = visited + [str(node)] # Creating new list rather than mutating - when recursion is unraveled and backtracks, don't want to think we visited something we haven't
            
            # Create a new path by recursively calling shortest path; new path is the shortest path from the current node to the end
            newPath = bruteForceSearch(digraph, node, end, maxTotalDist, maxDistOutdoors, False, visited)
            # If no path found, continue
            if newPath == None:
                continue
            # If path found, check if it is better, worse, or same with previous shortest path
            if (shortest == None or len(newPath) < len(shortest)):
                shortest = newPath
    if shortest != None:
        path = path + shortest
    else:
        path = None
    
    # This may accidentally limit further than desired
    # if getDistance(digraph, path, False) > maxTotalDist or getDistance(digraph, path, True) > maxDistOutdoors:
        # raise ValueError
        
    return path

#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors, toPrint = False, visited = [], memo = {}):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    #TODO
    if not (digraph.hasNode(start) and digraph.hasNode(end)):
        raise ValueError('Start or end not in digraph.')
    
    path = [str(start)]
    if start == end:
        return path
    shortest = None
    for node in digraph.childrenOf(start):
        if (str(node) not in visited):
            visited = visited + [str(node)]
            # FIRST, ask if we know answer. Try to access memo at [node, end]
            try:
                newPath = memo[node, end]
            # If not available yet in memo, run shortestpath recursively
            except:
                newPath = directedDFS(digraph, node, end, maxTotalDist, maxDistOutdoors, False, visited, memo)
            if newPath == None:
                continue
            if (shortest == None or len(newPath) < len(shortest)):
                shortest = newPath
                memo[node, end] = newPath
    if shortest != None:
        path = path + shortest
    else:
        path = None
    # This may accidentally limit further than desired
    # if getDistance(digraph, path, False) > maxTotalDist or getDistance(digraph, path, True) > maxDistOutdoors:
        # raise ValueError
    return path

# Uncomment below when ready to test

# ## Pre tests 
# print '\n\n\n==================================================='
# print 'Testing implementation of load_map: '
# mapGraph = load_map("mit_map.txt")
# print mapGraph
# print '==================================================='
# print 'Testing implementation of getDistance: '
# print "nodeList of ['66','68','76'] should return 51+72 = 123 distance, 0+30 = 30 feature"
# nodeList = ['66','68','76']
# dist = getDistance(mapGraph, nodeList, featureDist = False)
# print 'Distance distance: ',dist
# feature = getDistance(mapGraph, nodeList, featureDist = True)
# print 'Feature distance: ',feature
# print '===================='
# # print "nodeList of ['30','66'] has an invalid node. Test edge case: "
# # getDistance(mapGraph, ['30','66'], featureDist = False)
# # print '===================='
# # print "nodeList of ['18','66'] has no valid edge. Test edge case: "
# # getDistance(mapGraph, ['18','66'], featureDist = False)
# print '==================================================='
# print 'Testing implementation of brute force method: '
# start = '32'
# end = '62'
# testPath = bruteForceSearch(mapGraph, start, end, 1000, 1000, False, [])
# print testPath
# print '==================================================='
# print 'Testing implementation of directedDFS: '
# testPathDFS = directedDFS(mapGraph, start, end, 1000, 1000, toPrint = False, visited = [], memo = {})
# print testPathDFS
## All unit tests passed above.

# print '\n\n\n\n'

# ######### BUILT IN UNIT TESTS #################
# if __name__ == '__main__':
   # # Test cases
   # digraph = load_map("mit_map.txt")

   # LARGE_DIST = 1000000

   # # Test case 1
   # print "---------------"
   # print "Test case 1:"
   # print "Find the shortest-path from Building 32 to 56"
   # expectedPath1 = ['32', '56']
   # brutePath1 = bruteForceSearch(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
   # dfsPath1 = directedDFS(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
   # print "Expected: ", expectedPath1
   # print "Brute-force: ", brutePath1
   # print "DFS: ", dfsPath1

   # # Test case 2
   # print "---------------"
   # print "Test case 2:"
   # print "Find the shortest-path from Building 32 to 56 without going outdoors"
   # expectedPath2 = ['32', '36', '26', '16', '56']
   # brutePath2 = bruteForceSearch(digraph, '32', '56', LARGE_DIST, 0)
   # dfsPath2 = directedDFS(digraph, '32', '56', LARGE_DIST, 0)
   # print "Expected: ", expectedPath2
   # print "Brute-force: ", brutePath2
   # print "DFS: ", dfsPath2

   # # Test case 3
   # print "---------------"
   # print "Test case 3:"
   # print "Find the shortest-path from Building 2 to 9"
   # expectedPath3 = ['2', '3', '7', '9']
   # brutePath3 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
   # dfsPath3 = directedDFS(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
   # print "Expected: ", expectedPath3
   # print "Brute-force: ", brutePath3
   # print "DFS: ", dfsPath3

   # # Test case 4
   # print "---------------"
   # print "Test case 4:"
   # print "Find the shortest-path from Building 2 to 9 without going outdoors"
   # expectedPath4 = ['2', '4', '10', '13', '9']
   # brutePath4 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, 0)
   # dfsPath4 = directedDFS(digraph, '2', '9', LARGE_DIST, 0)
   # print "Expected: ", expectedPath4
   # print "Brute-force: ", brutePath4
   # print "DFS: ", dfsPath4

   # # Test case 5
   # print "---------------"
   # print "Test case 5:"
   # print "Find the shortest-path from Building 1 to 32"
   # expectedPath5 = ['1', '4', '12', '32']
   # brutePath5 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
   # dfsPath5 = directedDFS(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
   # print "Expected: ", expectedPath5
   # print "Brute-force: ", brutePath5
   # print "DFS: ", dfsPath5

   # # Test case 6
   # print "---------------"
   # print "Test case 6:"
   # print "Find the shortest-path from Building 1 to 32 without going outdoors"
   # expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
   # brutePath6 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, 0)
   # dfsPath6 = directedDFS(digraph, '1', '32', LARGE_DIST, 0)
   # print "Expected: ", expectedPath6
   # print "Brute-force: ", brutePath6
   # print "DFS: ", dfsPath6

   # # Test case 7
   # print "---------------"
   # print "Test case 7:"
   # print "Find the shortest-path from Building 8 to 50 without going outdoors"
   # bruteRaisedErr = 'No'
   # dfsRaisedErr = 'No'
   # try:
       # bruteForceSearch(digraph, '8', '50', LARGE_DIST, 0)
   # except ValueError:
       # bruteRaisedErr = 'Yes'
   
   # try:
       # directedDFS(digraph, '8', '50', LARGE_DIST, 0)
   # except ValueError:
       # dfsRaisedErr = 'Yes'
   
   # print "Expected: No such path! Should throw a value error."
   # print "Did brute force search raise an error?", bruteRaisedErr
   # print "Did DFS search raise an error?", dfsRaisedErr

   # # Test case 8
   # print "---------------"
   # print "Test case 8:"
   # print "Find the shortest-path from Building 10 to 32 without walking"
   # print "more than 100 meters in total"
   # bruteRaisedErr = 'No'
   # dfsRaisedErr = 'No'
   # try:
       # bruteForceSearch(digraph, '10', '32', 100, LARGE_DIST)
   # except ValueError:
       # bruteRaisedErr = 'Yes'
   
   # try:
       # directedDFS(digraph, '10', '32', 100, LARGE_DIST)
   # except ValueError:
       # dfsRaisedErr = 'Yes'
   
   # print "Expected: No such path! Should throw a value error."
   # print "Did brute force search raise an error?", bruteRaisedErr
   # print "Did DFS search raise an error?", dfsRaisedErr

