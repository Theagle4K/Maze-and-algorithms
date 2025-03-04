import sys
from PIL import Image


class Node():
    def __init__(self,parent,actions,state):
        self.parent = parent
        self.actions = actions
        self.state = state
              
        
A = Node(None,[1],1)
B = Node(A,[1,3],2)
C = Node(B,[1],3)
D = Node(C,[1],4)
E = Node(B,[1],5)
F = Node(E,[1],6)

NodeArray = [A, B, C, D, E, F]
def Action(state,action):
    for node in NodeArray:
        if node.state == state + action:
            return node
        

def DFS(Node = Node, goal = int):
    frontier = []
    visited = []
    step = 0
    
    frontier.append(Node)
    
    while True:
        
        if len(frontier) == 0:
            print("No Solution")
            break
        
        if Node.state == goal:
            break
        else:
            visited.append(Node)
            frontier.pop()
            for action in Node.actions:
                if Action(Node.state, action) is not None:
                    frontier.append(Action(Node.state, action))
            if len(frontier) != 0:        
                Node = frontier[-1]    
            
        step+=1
    return step

def BFS(Node = Node, goal = int):
    frontier = []
    visited = []
    step = 0
    
    frontier.append(Node)
    
    while True:
        
        if len(frontier) == 0:
            print("No Solution")
            break
        
        if Node.state == goal:
            break
        else:
            visited.append(Node)
            del frontier[0]
            for action in Node.actions:
                if Action(Node.state, action) is not None:
                    frontier.append(Action(Node.state, action))
            if len(frontier) != 0:        
                Node = frontier[0]    
            
        step+=1
    return step

#print(BFS(A,6))

class Maze():
    def __init__(self,filename):
        
        
        with open(filename) as file:
            contents = file.read()
        
        if contents.count("A") != 1:
            raise Exception("Maze must have a start point")
        if contents.count("B") != 1:
            raise Exception("Maze must have a start point")
        
        self.contents = contents.splitlines()
        self.rows = len(self.contents)
        self.columns = max(len(line) for line in self.contents)
        self.walls = self.det_wall()
        
    def cor_to_char(self,cor): #cor = [x,y], which x = row, y = col 
        if cor[0] > self.rows:
            raise Exception("Cordinates must be within the maze!") 
        if cor[1]  > self.columns:
            raise Exception("Cordinates must be within the maze!")
#        if cor[0] is not int:
#            raise Exception("Cordinates must be a number!")  
#        if cor[1] is not int:
#            raise Exception("Cordinates must be a number!")  
        return self.contents[cor[0]][cor[1]]
    
    def det_wall(self): # All wall cordinates must be gathered in one [], which can be used to determine which action is possible
        row_int = 0
        col_int = 0
        walls = []
        for row in self.contents:
            for col in row:
                if col == '#':
                    walls.append([row_int,col_int]) 
                col_int+=1
            row_int+=1
            col_int = 0
        return walls  
    
    def det_Start(self): # All wall cordinates must be gathered in one [], which can be used to determine which action is possible
        row_int = 0
        col_int = 0
        cor = []
        for row in self.contents:
            for col in row:
                if col == 'A':
                    cor = [row_int,col_int] 
                    return cor
                else: 
                    col_int+=1
            row_int+=1
            col_int = 0
     
    def app_action(self,node,action):
        newnode = Node(node,[],[node.state[0] + action[0],node.state[1] + action[1]])
        return newnode      
            
    def DFS_maze(self, Node, goal):
        frontier = []
        visited = []
        step = 0
        
        frontier.append(Node) 
        
        while True:
            
            if len(frontier) == 0:
                print("No Solution")
                break
            
            if Node.state == goal:
                break
            else:
                visited.append(Node.state)
                
                frontier.pop()
                if Node.actions != []:
                    for action in Node.actions:
                        new_Node = self.app_action(Node,action)
                        new_Node.actions = self.det_actions(new_Node.state)
                        if new_Node.state not in visited:
                            frontier.append(new_Node)
                if len(frontier) != 0:       
                    Node = frontier[-1]    
                
            step+=1
        return step      
    
    
    def det_actions(self,cor):
        actions = []
        # Up action = row - 1, col + 0
        # Down action = row + 1, col + 0
        # Right action = row + 0, col + 1
        # Left action = row + 0, col - 1
        if cor[0] > self.rows or cor[1] > self.columns:
            raise Exception("Cordinates must be within the maze!")
        else:
            if cor[0] - 1 >= 0 and [cor[0] - 1, cor[1]] not in self.walls:
                actions.append([-1,0])
            if cor[0] + 1 < self.rows and [cor[0] + 1, cor[1]] not in self.walls:
                actions.append([1,0])
            if cor[1] - 1 >= 0 and [cor[0], cor[1] - 1] not in self.walls:
                actions.append([0,-1])
            if cor[1] + 1 < self.columns and [cor[0], cor[1] + 1] not in self.walls:
                actions.append([0,1])  
        return actions    
    
    def solve(self):
        start_cor = self.det_Start()
        start_node = Node(None,self.det_actions(start_cor),start_cor) 
        steps = self.DFS_maze(start_node,[0,5])
        return steps
        
maze1 = Maze("maze3.txt")
#print(maze1.det_wall())
#print(maze1.det_actions([5,0]))
#print(maze1.det_Start())
#start_cor = maze1.det_Start()
#start_node = Node(None,maze1.det_actions(start_cor),start_cor) 
#print(maze1.app_action(start_node,maze1.det_actions(start_cor)[0]).actions)
print(maze1.solve())