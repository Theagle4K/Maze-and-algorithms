import sys
from PIL import Image, ImageDraw

#A Node class to keep certain details about tiles in check
class Node():
    def __init__(self,parent,actions,state):
        self.parent = parent #To know which tile was previous tile
        self.actions = actions #To keep what actions our Maze algorithm can apply
        self.state = state #What state is our Node in
              
#Maze class
class Maze():
    def __init__(self,filename):
        
        #Read the file to create it as a maze puzzle
        with open(filename) as file:
            contents = file.read()
        
        #A represents our Start
        if contents.count("A") != 1:
            raise Exception("Maze must have a start point")
        #B represents our Goal
        if contents.count("B") != 1:
            raise Exception("Maze must have a start point")
        
        #Contents of the file
        self.contents = contents.splitlines()
        #Rows of the maze (Y)
        self.rows = len(self.contents)
        #Columns of our maze (X)
        self.columns = max(len(line) for line in self.contents)
        #Walls of our Maze 
        self.walls = []
        #To keep count of steps
        self.steps = 0
        #To keep count of visited tiles
        self.visited = []
        #
        self.start_cor = []
        #
        self.end_cor = []
        
    #Translates any coordinate to character (exists for testing reasons)    
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
    
            
    def det_props(self):
        row_int = 0; col_int = 0
        for row in self.contents:
            for col in row:
                if col == "A":
                    self.start_cor = [row_int,col_int]
                elif col == "B":
                    self.end_cor = [row_int,col_int]
                elif col == "#":
                    self.walls.append([row_int,col_int])
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
        self.steps = step
        self.visited = visited   

    def BFS_maze(self, Node, goal):
        frontier = []
        visited = []
        step = 0   
        frontier.append(Node)
        
        while True:
            
            if len(frontier) == 0:
                print("No solution")
                break
            if Node.state == goal:
                break
            else:
                visited.append(Node.state)
                del frontier[0]
            if Node.actions != []:
                for action in Node.actions:
                    new_Node = self.app_action(Node,action)
                    new_Node.actions = self.det_actions(new_Node.state)
                    if new_Node.state not in visited:
                        frontier.append(new_Node)
            if len(frontier) != 0:
                Node = frontier[0]               
            step+=1
        self.steps = step
        self.visited = visited    

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
    
    def convert(self):
        im = Image.new(mode="RGB", 
                       size=(self.columns*100,self.rows*100),
                       color=(255,255,255)
                       )
        for wall in self.walls:
            draw = ImageDraw.Draw(im)
            x1 = wall[1]*100
            x2 = x1+100
            y1 = wall[0]*100
            y2 = y1+100
            draw.rectangle(xy = (x1, y1, x2, y2), 
                fill = (0, 0, 0), 
                #outline = (255, 255, 255), 
                #width = 10
            ) 
            #im.show()
        start_cor = self.start_cor
        for cor in self.visited:
                draw.rectangle(xy = (cor[1]*100, cor[0]*100,cor[1]*100 + 100 , cor[0]*100 + 100), 
                fill = (230, 200, 50), 
                #outline = (255, 255, 255), 
                #width = 10
                )
        draw.rectangle(xy = (start_cor[1]*100, start_cor[0]*100,start_cor[1]*100 + 100 , start_cor[0]*100 + 100), 
            fill = (100, 200, 0), 
            #outline = (255, 255, 255), 
            #width = 10
        ) 
        end_cor = self.end_cor
        draw.rectangle(xy = (end_cor[1]*100, end_cor[0]*100,end_cor[1]*100 + 100 , end_cor[0]*100 + 100), 
            fill = (200, 20, 20), 
            #outline = (255, 255, 255), 
            #width = 10
        )
        im.show() 
    
    def solve(self):
        self.det_props()
        start_node = Node(None,self.det_actions(self.start_cor),self.start_cor) 
        self.DFS_maze(start_node,self.end_cor)
        self.convert()
        
maze1 = Maze("maze2.txt")
maze1.solve()