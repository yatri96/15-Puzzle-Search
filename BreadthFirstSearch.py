#!/usr/bin/env python
# coding: utf-8

# In[1]:


from collections import deque
import time
import psutil 
class BFS_15Puzzle:
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
        
        
        
    def mainBFS(self,nodes_exp):
        """Main function to implement Breadth First Search
        for the 15 Puzzle Problem. It takes number of nodes to 
        be expanded as an argument which contains it's initial value as 0"""
        start_time = time.time()
        moves = { 'UP': 'U', 'DOWN': 'D', 'RIGHT': 'R', 'LEFT': 'L'}
        explored = {} #To check for repeated states. Stores the nodes expanded
        parent = {} #Dictionary/Hash Map to store the parents of current node
        action = {} #Dictionary/Hash Map to store theactions taken to reach current node
        frontier=deque([]) #FIFO queue to store the frontier
        goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
        
        
        ini_state = input("Enter the initial state of the 15-puzzle board:")
        ini_num = list(map(int, ini_state.split()))
        
        #checks for initial state
        if(goal==ini_num):
            end_time = time.time()
            print("Nodes expanded:",nodes_exp)
            print("Memory used (bytes):",psutil.virtual_memory())
            print("Time taken (ms):",(end_time-start_time)*1000)
            return "Moves: 0"
        
        #find children for initial state
        else:
            current_st = ini_num
            
            #creating dictionary for every explored state
            explored[tuple(current_st)] = 1
            #increment by 1 for initial node state
            nodes_exp=nodes_exp+1
            #Parent and action left blank for initial node as it is the root and has no parent
            parent[tuple(current_st)] = ""
            action[tuple(current_st)] = ""
            #to get the endex of the blank tile
            blank  = current_st.index(0)
            possible_actions = self.legalActions(blank)
            
            #Finding successor states from every possible action on root node
            for i in range(0,len(possible_actions)):
                new_st = self.successor(current_st[:],possible_actions[i][:])
                frontier.append(new_st)
                nodes_exp = nodes_exp + 1
                
                #setting root node as parent for new state
                parent[tuple(new_st)] = tuple(current_st)
                action[tuple(new_st)] = moves[possible_actions[i]]
                
                #checking if frontier is empty
            while (frontier):
                current_st = frontier.popleft() #Since it is FIFO queue, pop from left
                nodes_exp = nodes_exp + 1
                if(current_st==goal):
                    end_time = time.time()
                    print("Nodes expanded:",nodes_exp)
                    print("Memory used (bytes):",psutil.virtual_memory())
                    print("Time taken (ms):",(end_time-start_time)*1000)
                    return "Moves:"+self.disp_moves(parent,new_st,action)[::-1]  
                else:
                    
                    #Same as what is done for root node
                    explored[tuple(current_st)] = 1
                    nodes_exp = nodes_exp + 1
                    blank  = current_st.index(0)
                    possible_actions = self.legalActions(blank)
                    for i in range(0,len(possible_actions)):
                        new_st = self.successor(current_st[:],possible_actions[i][:])
                        nodes_exp = nodes_exp + 1
                        
                        #To avoid repeated states
                        if(not tuple(new_st) in explored):
                            parent[tuple(new_st)] = tuple(current_st)
                            action[tuple(new_st)] = possible_actions[i]
                            if(not new_st in frontier):
                                if(new_st!=goal):
                                    frontier.append(new_st)
                                    nodes_exp = nodes_exp + 1
                                else:
                                    end_time = time.time()
                                    print("Nodes expanded:",nodes_exp)
                                    print("Memory used (bytes):",psutil.virtual_memory())
                                    print("Time taken (ms):",(end_time-start_time)*1000)
                                    return "Moves:"+self.disp_moves(parent,new_st,action)[::-1]
                                
            #end of while
            return "frontier empty! failure!" 
                
            
                
obj = BFS_15Puzzle()
kj = obj.mainBFS(0)
print(kj)       
            
        



# In[ ]:





# In[ ]:




