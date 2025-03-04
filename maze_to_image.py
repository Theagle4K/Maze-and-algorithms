from PIL import Image, ImageDraw
import os

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
           
        im.show()
        
maze = Maze("maze3.txt")
maze.convert()