from math import sqrt
from bisect import insort
import sys


def shortest_path(M,start,goal):
    print("shortest path called")
    extension = set()
    frontier = [start] # list of tuples (node, f_cost), ordered by cost (lowest to highest)
    frontier_set = set([start])# added to test membership in frontier
    gcost = {start:0} # real cost from start
    hcost = {start:heuristic(start, goal, M.intersections)}# heuristic cost
    g_predecessor = {start:None}
    while frontier:
        # Choose best node from frontier
        best_node = frontier.pop(0)
        frontier_set.remove(best_node) # synced with frontier
        
        # Choose best_node and extend it
        extension.add(best_node)
        if best_node == goal:
            continue
        
        # Update extension nodes costs coming from best_node
        neighbours = M.roads[best_node]
        for neighbour in neighbours:
            # Calculate the real cost for the node
            neighbour_cost = gcost[best_node] + distance(M.intersections[best_node], M.intersections[neighbour])
            if neighbour not in extension:
                if neighbour not in frontier_set:
                    insort(frontier, neighbour) # we assume frontier is already sorted
                    frontier_set.add(neighbour) # synced with frontier
                    gcost[neighbour] = neighbour_cost
                    hcost[neighbour] = heuristic(neighbour, goal, M.intersections)
                    g_predecessor[neighbour] = best_node
                    # Order frontier by f=g+h
                    frontier.sort(key=lambda x:gcost[x]+hcost[x])
               
                elif neighbour_cost < gcost[neighbour]:
                    # Update cost
                    gcost[neighbour] = neighbour_cost
                    hcost[neighbour] = heuristic(neighbour, goal, M.intersections)
                    g_predecessor[neighbour] = best_node
                    # Order frontier by f=g+h
                    frontier.sort(key=lambda x:gcost[x]+hcost[x])
    
    
    # Get the solution
    result = []
    node = goal
    while node != None:
        result.insert(0, node)
        node = g_predecessor[node] # predecessor
    return result
    
def heuristic(node, goal, coords):
    """ Heuristic. Distance from current to goal. """
    return distance(coords[node], coords[goal])

def distance(node1, node2):
    x2, y2 = node2[0], node2[1]
    x1, y1 = node1[0], node1[1]
    return sqrt( (x2-x1)**2 + (y2-y1)**2 )