import heapq
import time
import os
import psutil 
import math
class Astar_15Puzzle:
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
    
    #Function to find index of value in goal state
    def index_2d(self,myList, v):
        for i, x in enumerate(myList):
            if v in x:
                return (i, x.index(v))
        
    
    #Fucntion to calculate the two heuristics
    def h1(self, state, k):
        #To calculate no. of misplaced tiles
        if(k==1):
            goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0] 
            return sum(s != g for (s, g) in zip(state, goal))
        
        #To calculate Manhattan Distance
        elif(k==2):
            s=0
            goal = [[1, 2, 3, 4], [5,6,7,8],[9,10,11,12],[13,14,15,0]]
            nstate = [[state[0],state[1],state[2],state[3]],
                      [state[4],state[5],state[6],state[7]],
                      [state[8],state[9],state[10],state[11]],
                      [state[12],state[13],state[14],state[15]]]
            for l in range(0,4):
                for m in range(0,4):
                    if( not goal[l][m]== nstate[l][m]):
                        val = nstate[l][m]
                        z = self.index_2d(goal, val)
                        s = s + (abs(z[0]-l)+abs(z[1]-m))
            return s
                
    #function to implement A star serach using best first graph search but wuth f(n)=g(n)+h(n)
    def BESTFGS(self):
        start_time = time.time()
        moves = { 'UP': 'U', 'DOWN': 'D', 'RIGHT': 'R', 'LEFT': 'L'}
        explored = {} #To check for repeated states. Stores the nodes expanded
        parent = {} #Dictionary/Hash Map to store the parents of current node
        action = {} #Dictionary/Hash Map to store theactions taken to reach current node
        f = {} 
        g = {} #to store path cost
        frontier = [] #Priority queue to store the frontier 
        goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
        x = 0
        f1 = 0
        
        ini_state = input("Enter the initial state of the 15-puzzle board:")
        ini_num = list(map(int, ini_state.split()))
        j = int(input("Enter your choice of heuristic:\n1.No. of misplaced tiles\n2.Manhattan Distance - "))
        
        g[tuple(ini_num)] = 0
        f[tuple(ini_num)] = g[tuple(ini_num)]+self.h1(ini_num,j)
        heapq.heappush(frontier, (f[tuple(ini_num)], ini_num)) #implementing priority queue with heapq
        parent[tuple(ini_num)] = ""
        action[tuple(ini_num)] = ""
        n = 1
        
        while (frontier):
            x = x+1 #Calculates depth of tree which is used as path cost
            state = heapq.heappop(frontier)
            #checks for goal state
            if(goal==state[1]):
                end_time = time.time()
                print("Nodes expanded:",n)
                return "Moves:"+self.disp_moves(parent,state[1],action)[::-1],start_time,end_time  
            
            #adding expanded node to explored
            explored[tuple(state[1])] = 1
            
            blank = state[1].index(0)
            #genearte list of possible actions
            possible_actions = self.legalActions(blank)
            for i in range(0,len(possible_actions)):
                child = self.successor(state[1],possible_actions[i][:])
                #increment number of nodes expanded by 1 for every child generated
                n=n+1
                #checking if child is already explored i.e., checking for initial states
                if((not tuple(child) in explored)):
                    parent[tuple(child)] = tuple(state[1])
                    action[tuple(child)] = moves[possible_actions[i]]
                    g[tuple(child)] = x
                    
                    #checking if child is in frontier
                    if(not child in frontier):
                        f[tuple(child)] = g[tuple(child)] + self.h1(child,j)
                        heapq.heappush(frontier, (f[tuple(child)], child))

                    #updating f value if child is already in frontier and it has smaller value than before
                    elif (child in frontier):
                        f1 = g[tuple(child)] + self.h1(child,j)
                        if f1 < f[tuple(child)]:
                            del frontier[child]
                            f[tuple(child)] = f1
                            heapq.heappush(frontier, (f[tuple(child)], child))
                            
        return None     
             
            
process = psutil.Process(os.getpid())
initial_memory = process.memory_info().rss / 1024.0    
obj = Astar_15Puzzle()
z,st,et = obj.BESTFGS() 
print(z)
final_memory = process.memory_info().rss / 1024.0
print("Memory used:"+str(final_memory-initial_memory)+" KB")
print("Time taken (ms):",(et-st)*1000)  

