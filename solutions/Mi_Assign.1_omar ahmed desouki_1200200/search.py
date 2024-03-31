from problem import HeuristicFunction, Problem, S, A, Solution
from helpers.utils import NotImplemented
from queue import PriorityQueue
from collections import deque



#TODO: Import any modules you want to use
import heapq

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

# class Node:
#     def __init__(self, state, path_cost, parent=None, action=None):
#         self.state = state
#         self.path_cost = path_cost
#         self.parent = parent
#         self.action = action

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:

    if problem.is_goal(initial_state):#condition if first node is the goal
        return [initial_state] #TODO make it a list?

    path=list()
    frontier = deque()
    frontier.append((initial_state, []))  #Use tuples to store both the state and its path
    explored = set()
    frontier_set = set() #3shan el timeout fa batcheck faster using dah

    while frontier:

        node, path = frontier.popleft()
        explored.add(node)

        for action in problem.get_actions(node): #get all possible actions for the node
        
            childstate = problem.get_successor(node, action) #get the child state of the node for this action
            if problem.is_goal(childstate): #goal check
                path = path + [action] 
                return path 
            
            #bycheck lw el child state msh fe el frontier wala el explored
            #el check el 8areb 3shan lazem ytcheck en el child state bs ely msh fel forentier eno momken yb2a mawgod tany be path mokhtlf
            if childstate not in explored and childstate not in frontier_set:
                # extend the path
                new_path = path + [action] #add the childstate to the path before adding the node to the frontier
                # Add the child state we el new path to the frontier
                frontier.append((childstate, new_path))
                frontier_set.add(childstate) #el second frontier for faster checking

    return None
            


def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:

    if problem.is_goal(initial_state):#condition if first node is the goal
        return [initial_state] #TODO make it a list?

    path=list()
    frontier = deque()
    frontier.append((initial_state, []))  #Use tuples to store both the state and its path
    explored = set()
    frontier_set = set() #3shan el timeout fa batcheck faster using dah

    while frontier:

        node, path = frontier.pop()
        explored.add(node)

        if problem.is_goal(node): #Goal check
            return path 
            
        for action in problem.get_actions(node): #action feh kol node momken aroha
        
            childstate = problem.get_successor(node, action)
            #bycheck lw el child state msh fe el frontier wala el explored
            #el check el 8areb 3shan lazem ytcheck en el child state bs ely msh fel forentier eno momken yb2a mawgod tany be path mokhtlf
            if childstate not in explored and childstate not in frontier_set:
                # extend the path
                new_path = path + [action]
                # Add the child state we el new path to the frontier
                frontier.append((childstate, new_path))
                frontier_set.add(childstate) 

    return None    

def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:

    if problem.is_goal(initial_state):
        return [initial_state]

    path = list()
    explored = set()
    frontier = PriorityQueue()
    order =0 #3shan lw el etnen nafs el cost fa byakhod ely expanded el awel
    frontier.put((0,order, initial_state, []))  # Use a priority queue
    frontier_set = set()


    while frontier.queue:

        # print('##################testing################')
        # #print(node)
        # #print(cost) 
        # print(frontier.queue)
        # print('##################testing################')

        temp = frontier.get() #3shan el piority queue lazem ttfk kda
        (cost,_, node, path) = temp 
        explored.add(node)
            
        if problem.is_goal(node): #Goal check
            return path

        for action in problem.get_actions(node): #action feh kol node momken aroha

            order = order + 1
            childstate = problem.get_successor(node, action) #get the child state of the node for this action

            if childstate not in explored and childstate not in frontier_set: #bycheck lw el child state msh fe el frontier wala el explored

                new_path = path + [action] #new path after adding the childstate
                costtochild = problem.get_cost(node, action) #get el cost lel path el gded
                frontier.put((cost + costtochild, order,childstate, new_path)) #ba increment el cost el gded lel cost el adem
                frontier_set.add(childstate)
                 
    return None

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    from typing import Callable
    
    if problem.is_goal(initial_state):
        return [initial_state]

    path = list()
    explored = set()
    frontier = PriorityQueue()
    order =0 #3shan lw el etnen nafs el hfn+cost fa yakhod el expanded el awel
    frontier.put((0,order,0, initial_state, []))  # Use a priority queue
    frontier_set = set()

    #oldhfn = heuristic(problem, initial_state) 

    while frontier.queue:
        # print('##################testing################')
        # #print(node)
        # #print(cost) 
        # print(frontier.queue)
        # print('##################testing################')

        temp = frontier.get() #3shan el piority queue lazem ttfk kda
        #zawedt el old cost 3shan el piority queue hya 3obara 3n el old cost + el hfn bta3et el ana feh bs msh kol ely fat
        (mix,_,oldcost, node, path) = temp 
        explored.add(node)
            
        if problem.is_goal(node):
            return path

        for action in problem.get_actions(node):

            order = order + 1
            childstate = problem.get_successor(node, action)

            if childstate not in explored and childstate not in frontier_set:

                new_path = path + [action]

                #oldcost = mix - oldhfn
                #newcost =  oldcost + problem.get_cost(node, action)
                #newhfn =  heuristic(problem, childstate) 
                #newmix = newcost + newhfn
                mix = oldcost + problem.get_cost(node, action) + heuristic(problem, childstate) #el cost bytgm3 laken el el hfn la
                cost = oldcost + problem.get_cost(node, action)
                frontier.put((mix, order, cost ,childstate, new_path))
               #oldhfn = heuristic(problem, childstate) #basave el adem
                frontier_set.add(childstate)
                 
    return None

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    from typing import Callable
    
    if problem.is_goal(initial_state):
        return [initial_state]

    path = list()
    explored = set()
    frontier = PriorityQueue()
    order =0 #3shan lw el etnen nafs el hfn fa yakhod el expanded el awel
    frontier.put((0,order, initial_state, []))  # Use a priority queue
    frontier_set = set()

    while frontier.queue:

        temp = frontier.get() #3shan el piority queue lazem ttfk kda
        (_,_, node, path) = temp 
        explored.add(node)
            
        if problem.is_goal(node):
            return path

        for action in problem.get_actions(node):

            order = order + 1
            childstate = problem.get_successor(node, action)

            if childstate not in explored and childstate not in frontier_set:

                new_path = path + [action]
                newhfn =  heuristic(problem, childstate) #get huristic function for this childstate, heuristics aren't sumed 
                frontier.put((newhfn, order,childstate, new_path)) 
                frontier_set.add(childstate)
                 
    return None