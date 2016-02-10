# 6.00 Problem Set 11
#
# graph.py
#
# A set of data structures to represent graphs
#

class Node(object):
   def __init__(self, name):
       self.name = str(name)
   def getName(self):
       return self.name
   def __str__(self):
       return self.name
   def __repr__(self):
      return self.name
   def __eq__(self, other):
      return self.name == other.name
   def __ne__(self, other):
      return not self.__eq__(other)

class Edge(object):
   def __init__(self, src, dest):
       self.src = src
       self.dest = dest
   def getSource(self):
       return self.src
   def getDestination(self):
       return self.dest
   def __str__(self):
       return str(self.src) + '->' + str(self.dest)

# Added #       
class FeatureEdge(Edge):
    def __init__(self, src, dest, distance, feature):
        '''Initialize the same way you would an edge'''
        Edge.__init__(self, src, dest)
        self.feature = feature
        self.distance = distance
    def getDistance(self):
        return self.distance
    def getFeature(self):
        return self.feature
    def __str__(self):
       return str(self.src) + '->' + str(self.dest) + '\tDistance: '+str(self.distance)+'  Feature: '+str(self.feature)
       
class Digraph(object):
   """
   A directed graph
   """
   def __init__(self):
       self.nodes = set([])
       self.edges = {}
       # Testing edgeList
       self.edgeList = []
   def addNode(self, node):
       if node in self.nodes:
           raise ValueError('Duplicate node')
       else:
           self.nodes.add(node)
           self.edges[node] = []
   def addEdge(self, edge):
       '''Adds a dictionary of source:destination nodes. Not really adding an Edge instance.
       Each new destination point is added as part of the linked list to the source'''
       src = edge.getSource()
       dest = edge.getDestination()
       if not(src in self.nodes and dest in self.nodes):
           raise ValueError('Node not in graph')
       self.edges[src].append(dest)
       
       # Testing edgeList
       if not edge in self.edgeList:
           self.edgeList.append(edge)
   
   def getEdge(self, node1, node2):
       for edge in self.edgeList:
           if edge.getSource() == node1 and edge.getDestination() == node2:
                found_edge = edge
       try:
           found_edge
           return found_edge
       except NameError:
           print 'No edge found between nodes %s and %s' % (node1, node2)
           raise
   
   def childrenOf(self, node):
       return self.edges[node]
   def hasNode(self, node):
       return node in self.nodes
   def hasEdge(self, edge):
       return edge in self.edgeList
   def __str__(self):
       res = ''
       for k in self.edges:
           for d in self.edges[k]:
               res = res + str(k) + '->' + str(d) + '\n'
       return res[:-1]
   def printEdges(self):
        ''' prints edges. largely for testing.'''
        for edge in self.edgeList:
            print edge


# # ############### TESTS ###############
# print '\n\n\n#############################################'
# print 'Testing implementation of Node'
# startBuilding = Node('10')
# endBuilding = Node('32')
# building2 = Node('20')
# building3 = Node('30')
# print startBuilding, endBuilding
# print '#############################################'
# print 'Testing implementation of FeatureEdge'  # Tested Edge, changing to FeatureEdge
# startToEndEdge = FeatureEdge(startBuilding,endBuilding, 10, 8)
# print '#############################################'
# print '#######Testing implementation of Digraph#####'
# buildingGraph = Digraph()
# print buildingGraph
# print 'Testing addNode...adding startBuilding and endBuilding'
# buildingGraph.addNode(startBuilding)
# buildingGraph.addNode(endBuilding)
# buildingGraph.addNode(building2)
# buildingGraph.addNode(building3)
# print buildingGraph
# print 'Testing addEdge...adding edge'
# buildingGraph.addEdge(startToEndEdge)
# print buildingGraph
# print 'Testing childrenOf...should return endBuilding as child of Start Building'
# print buildingGraph.childrenOf(startBuilding)
# print 'Testing hasNode...should return TRUE for endBuilding'
# print buildingGraph.hasNode(endBuilding)
# # # print 'Testing getNodeAt...'
# # # print buildingGraph.getNodeAt('32')
# print '#############################################'
# print 'Testing implementation of FeatureEdge'
# startToEndFeatureEdge = FeatureEdge(building2,building3, 200, 40)
# newEdge = FeatureEdge(startBuilding,building3, 200, 40)
# print startToEndFeatureEdge
# print 'Testing getFeature'
# print startToEndFeatureEdge.getFeature()
# print 'Testing getDistance'
# print startToEndFeatureEdge.getDistance()
# print '#############################################'
# print 'Testing printing of Digraph'
# buildingGraph.addEdge(startToEndFeatureEdge)
# buildingGraph.addEdge(newEdge)
# print buildingGraph
# print '#############################################'
# print 'Testing printEdges of Digraph'
# buildingGraph.printEdges()
# print '#############################################'
# print 'Testing getEdge of Digraph: '
# print 'Testing getEdge(building2, building3). Should return an edge'
# found_edge = buildingGraph.getEdge(building2,building3)
# print found_edge
# print 'Testing getEdge(endBuilding, building3). Should return FALSE'
# found_edge2 = buildingGraph.getEdge(endBuilding,building3)
# print found_edge2
# print '#############################################'