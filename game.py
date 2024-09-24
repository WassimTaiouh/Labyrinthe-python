from random import randint
from time import sleep
from tkinter import *
from wall import Wall
from mouse import Mouse
from memory import Memory, Node
import _thread


actionNames= ["forward", "turnLeft", "turnRight", "touchFront", "touchLeft", "touchRight"]

class Game:

    def __init__(self):
        self.root = Tk()
        self.root.title("Labyrinthe")
        self.width=600
        self.heigth=400 
        self.mouse= Mouse()
        self.memory= Memory()
        self.speed= 0.01
        self.score= 0
        self.canevas = Canvas(self.root, width = self.width, height = self.heigth, background="#FFF")    
        self.canevas.pack()
        self.createWalls()
        self.draw()
        _thread.start_new_thread(self.animation, ())
        #self.root.bind("<Key>", self.onKeyPress)
        self.root.mainloop()

    def createWalls(self):
        self.walls= []
        for x in range(0,self.width,50):
            for y in range(0,self.heigth,50):
                if x==0 or x==(self.width-50) or y==0 or y==(self.heigth-50):
                    self.walls.append(Wall(x, y))
                
                if (x>50 and x<(self.width-100) and y>50 and y<(self.heigth-100)):
                    if(x!=(self.width-150) and y!=100):
                        self.walls.append(Wall(x, y))
                    elif x>(self.width-200) and y <150:
                        continue
                    elif y>50:
                        self.walls.append(Wall(x, y))
    
    def draw(self):
        for i in range(len(self.walls)):
           self.walls[i].draw(self.canevas)
        self.canevasMouse= self.mouse.draw(self.canevas)

    def isColision(self):
        for i in range(len(self.walls)):
            if(self.walls[i].isCollision(self.mouse.coordX, self.mouse.coordY)):
                return True
        return False

    def doAction(self, numAction):
        oldCoord= (self.mouse.coordX, self.mouse.coordY)
        if  numAction==0:
            self.mouse.forward()
        elif numAction==1:
            self.mouse.turnLeft()
        elif numAction==2:
            self.mouse.turnRight()
        elif numAction==3:
            self.mouse.touchFront()
        elif numAction==4:
            self.mouse.touchLeft()
        elif numAction==5:
            self.mouse.touchRight()
        
        collision= self.isColision()
        if collision or numAction>2:
            self.mouse.coordX= oldCoord[0]
            self.mouse.coordY= oldCoord[1]

        self.canevas.delete(self.canevasMouse)
        self.canevasMouse= self.mouse.draw(self.canevas)
        return self.performance(numAction, collision)

    def performance(self, numAction, collision):
        if  numAction==0:
            if collision:
                return -500
            else:
                return 300
        elif numAction==1 or numAction==2:
            return -50
        else:
            if collision:
                return -20
            else:
                return -10

    def animation(self):
        while(True):
            sleep(self.speed)
            action = self.memory.chooseBestAction()
            result= self.doAction(action)
            self.memory.update(Node(action, result))
            self.score+=result
            print("memory size", self.memory.size())
            print(actionNames[action], result, self.score)
        
if __name__== "__main__":
    game= Game()