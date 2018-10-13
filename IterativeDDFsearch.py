


from collections import deque
import time
import os
import psutil 
class IDS_15Puzzle:
    def __init__(self):
        pass
    
    def legalActions(self,blank_tile):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']       

        if (blank_tile % 4 == 0):
            possible_actions.remove('LEFT')
        if (blank_tile < 4):
            possible_actions.remove('UP')
        if (blank_tile % 4 == 3):
            possible_actions.remove('RIGHT')
        if (blank_tile > 11):
            possible_actions.remove('DOWN')
            
        return possible_actions
        
    def successor(self, state, action):
        """Return the next/successor state given the current state and action. 
        Thus, it implements a successor function"""
        blank  = state.index(0)
        new_state = list(state)
        move_by = {'UP': -4, 'DOWN': 4, 'RIGHT': 1, 'LEFT': -1}
        neighbour = blank+move_by[action]
        new_state[blank], new_state[neighbour] = new_state[neighbour], new_state[blank]
        return new_state
        
    def disp_moves(self,parent,state,actions):
        """Returns the solution in the form of moves to be made to reach
        the goal from the initial state.Takes the parent dictionary, 
        actions dictionary and the current state as input"""
        moves = ""
        while (parent[tuple(state)]!=""):
            moves = moves+actions[tuple(state)][0]
            state = parent[tuple(state)]
            
        return moves
    
    #function that is called recursively for every child node in depth limited search
    def recursive_DLS(self,state,limit,parent,action,moves,goal,explored,n):
        #checks for goal state
        if(goal==state):
            print("Nodes expanded:",n)
            return "Moves:"+self.disp_moves(parent,state,action)[::-1] 
        # cutoff indicates no solution within depth limit
        elif (limit==0):
            return "cutoff"
        
        else:
            cutoff_occured = False
            #adding expanded node to explored
            explored[tuple(state)] = 1
            blank  = state.index(0)
            #genearte list of possible actions
            possible_actions = self.legalActions(blank)
            for i in range(0,len(possible_actions)):
                child = self.successor(state[:],possible_actions[i][:])
                #increment number of nodes expanded by 1 for every child generated
                n=n+1
                #checnking if child is already explored i.e., checking for initial states
                if((not tuple(child) in explored)):
                    parent[tuple(child)] = tuple(state)
                    action[tuple(child)] = moves[possible_actions[i]]
                    
                    #recursively calling Depth limited search for every child generated
                    result = self.recursive_DLS(child, limit-1,parent,action,moves,goal,explored,n)
                    if (result=="cutoff"):
                        cutoff_occured = True
                        
                    # failure is when there is no solution for given input
                    elif (not result == "failure"):
                        return result
            if (cutoff_occured):
                return "cutoff"
            else:
                return "failure"
            
     #function to implement depth limited search for particular depth limit      
    def mainDLS(self,limit,ini_num,parent,action,n):
        moves = { 'UP': 'U', 'DOWN': 'D', 'RIGHT': 'R', 'LEFT': 'L'}
        
        explored = {} #To check for repeated states. Stores the nodes expanded
        goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
        
        result = self.recursive_DLS(ini_num[:],limit,parent,action,moves,goal[:],explored,n)
        return result
    
    #Main iterative deepening depth first search function which calls depth limited search for various depth limits
    def IDS(self):
        
        start_time = time.time()
        ans = False
        depth = 0
        parent = {} #Dictionary/Hash Map to store the parents of current node
        action = {} #Dictionary/Hash Map to store the actions taken to reach current node
        ini_state = input("Enter the initial state of the 15-puzzle board:")
        ini_num = list(map(int, ini_state.split()))
        parent[tuple(ini_num)] = ""
        action[tuple(ini_num)] = ""
        nodes_exp = 1
        
        while (not ans):
            result  = self.mainDLS(depth,ini_num,parent,action,nodes_exp)
            if(not result == "cutoff"):
                ans = True
                end_time = time.time()
                return result,start_time,end_time
            depth = depth+1
             
            
process = psutil.Process(os.getpid())
initial_memory = process.memory_info().rss / 1024.0        
obj = IDS_15Puzzle()
x,st,et = obj.IDS() 
print(x)
final_memory = process.memory_info().rss / 1024.0
print("Memory used:"+str(final_memory-initial_memory)+" KB")
print("Time taken (ms):",(et-st)*1000)  




            
        


