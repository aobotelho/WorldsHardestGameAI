from Pen import Pen
import random
import numpy as np

class Player(Pen):
    def __init__(self,color='Blue'):
        self.playerColor = color
        Pen.__init__(self,self.playerColor)
        #Flag if player is dead
        self.isDead = False
        #Flag if player collided with enemy
        self.enemyCollisionFlag = False
        #Flag if player reached the end
        self.endGameFlag = False
        #Flag if reached checkpoint
        self.reachedCheckpoint = False
        #Limit of steps in same position to declare it dead
        self.limitStepsSameCoordinates = 20
        #Default Metrics
        self.minDistEnemyLeftAbove = 10000
        self.minDistEnemyRightAbove = 10000
        self.minDistWallLeft = 10000
        self.minDistWallRight = 10000
        self.distFinalX = 10000
        self.distFinalY = 10000
        self.fitness = 10000
        self.stepsInSameCoordinates = 0
        #Generate random weights values
        #Weights Format: (<Number of nodes in layer>,<Number of nodes in previous layer>)
        #All values between [-1,1]
        #6 input variables
        #6 nodes in hidden layer1
        #4 nodes in hidden layer2
        #4 nodes in output layer (left,up,right,down)
        self.hiddenLayer1Weights = np.random.rand(6,6)*2 -1
        self.hiddenLayer2Weights = np.random.rand(4,6)*2 -1
        self.outputLayerWeights = np.random.rand(4,4)*2 -1
        pass

    def ResetDefaults(self):
        self.color(self.playerColor)
        self.isDead = False
        self.enemyCollisionFlag = False
        self.endGameFlag = False
        self.reachedCheckpoint = False
        self.minDistEnemyLeftAbove = 10000
        self.minDistEnemyRightAbove = 10000
        self.minDistWallLeft = 10000
        self.minDistWallRight = 10000
        self.distFinalX = 10000
        self.distFinalY = 10000
        self.fitness = 10000
        self.stepsInSameCoordinates = 0
        pass

    def GoDirection(self,keyPressed,wallCoordinates,checkpointCoordinates,finalCoordinates):
        moved = False
        if self.isDead == False:
            #Define next position from button 'pressed'
            if keyPressed == 'Up':
                coordGoTo = (self.xcor(),self.ycor() + 24)
            elif keyPressed == 'Down':
                coordGoTo = (self.xcor(),self.ycor() - 24)
            elif keyPressed == 'Left':
                coordGoTo = (self.xcor() - 24,self.ycor())
            elif keyPressed == 'Right':
                coordGoTo = (self.xcor() + 24,self.ycor())
            else:
                coordGoTo = (self.xcor() + 24,self.ycor())
            
            #Check if new coordinates is a wall. 
            #If not goes to that position
            #If it is does nothing
            if coordGoTo not in wallCoordinates:
                self.goto(coordGoTo)
                moved = True
            else:
                coordGoTo = (self.xcor(),self.ycor())
            
            #Check if new coordinates is in checkpoint coordinates
            #If it is we'll set the flag that it has reached checkpoint
            if checkpointCoordinates != None and coordGoTo in checkpointCoordinates:
                self.reachedCheckpoint = True 

            #Check if new coordinates is in final position coordinates
            #If it is we'll set the flag that it has reached final position
            if finalCoordinates != None and coordGoTo in finalCoordinates:
                self.endGameFlag = True 
        return moved
    
    def CollisionWithEnemy(self,enemyCoordinates):
        #Check if collision ocurred. 
        #If current coordinates is in any of enemies coordinates flag isDead is set to True
        #If current coordinates is in any of enemies coordinates collision flag is set to True
        if (self.xcor(),self.ycor()) in enemyCoordinates:
            self.isDead = True
            self.enemyCollisionFlag = True
            self.color('cornflower blue')
        pass

    def MoveRandom(self,wallCoordinates,checkpointCoordinates,finalCoordinates):
        #Moves a random position from list.
        #To be replaced by neural network
        possibleSteps = ['Up','Left','Down','Right']
        return self.GoDirection(random.choice(possibleSteps),wallCoordinates,checkpointCoordinates,finalCoordinates)
    
    def dist(self,x1,x2): 
        #Calculates distance between tuples and current position
        return np.sqrt((x1[0] - x2[0])**2 + (x1[1] - x2[1])**2)
    def distPlayer(self,x): 
        #Calculates distance between tuples and current position
        return self.dist(x,(self.xcor(),self.ycor()))

    def distX(self,x): 
        #Distance between the X value from a tuple and current x position
        return x[0] - self.xcor()
    def distY(self,x): 
        #Distance between the y value from a tuple and current y position
        return x[1] - self.ycor()
    def distXAbs(self,x): 
        #Absolute distance between the X value from a tuple and current x position
        return abs(self.distX(x))
    def distYAbs(self,x): 
        #Absolute distance between the y value from a tuple and current y position
        return abs(self.distY(x))

    def MetricsCalculation(self,wallCoordinates,initialCoordinates,checkpointCoordinates,finalCoordinates,enemyCoordinates):
        #Filter only enemies on left and above and gets minimal distance (closes enemy)
        enemysLeftAbove = [x for x in enemyCoordinates if x[0] <= self.xcor() and x[1] >= self.ycor()]
        try:
            self.minDistEnemyLeftAbove = min(list(map(self.distPlayer,enemysLeftAbove)))
        except:
            self.minDistEnemyLeftAbove = 0

        #Filter only enemies on right and above and gets minimal distance (closes enemy)
        enemysRightAbove = [x for x in enemyCoordinates if x[0] >= self.xcor() and x[1] >= self.ycor()]
        try:
            self.minDistEnemyRightAbove = min(list(map(self.distPlayer,enemysRightAbove)))
        except:
            self.minDistEnemyRightAbove = 0
        
        #Calculates distance to closes wall on left
        wallsSameLevelLeft = [x for x in wallCoordinates if x[0] < self.xcor() and x[1] == self.ycor()]
        try:
            self.minDistWallLeft = min(list(map(self.distXAbs,wallsSameLevelLeft)))
        except:
            self.minDistWallLeft = 0

        #Calculates distance to closes wall on right
        wallsSameLevelRight = [x for x in wallCoordinates if x[0] > self.xcor() and x[1] == self.ycor()]
        try:
            self.minDistWallRight = min(list(map(self.distXAbs,wallsSameLevelRight)))
        except:
            self.minDistWallRight = 0
        
        #Calculates x and y distance to final coordinates
        self.distFinalX = min(list(map(self.distX,finalCoordinates)))
        self.distFinalY = min(list(map(self.distY,finalCoordinates)))
        pass
    
    def CalculateFitness(self,initialCoordinates,finalCoordinates):
        ###########################################################################################
        # Based on this level design we'll check wether the player reached checkpoint
        # If the player hasn't reached we'll calculate the distance between
        # him and the exit and add to that the distance between the exit and the final coordinates
        ###########################################################################################
        if self.reachedCheckpoint == False:
            halfCheckPoint = (-72, -192)
            self.fitness = (1/(self.dist(halfCheckPoint,finalCoordinates[0]) + self.distPlayer(halfCheckPoint)))**2
        else:
            self.fitness = (1/(self.distPlayer(finalCoordinates[0])))**2

    def ForwardPropagation(self):
        inputValues = np.asarray([
            self.minDistEnemyLeftAbove,
            self.minDistEnemyRightAbove,
            self.minDistWallLeft,
            self.minDistWallRight,
            self.distFinalX,
            self.distFinalY
        ]).reshape((1,-1))

        Z1 = np.matmul(self.hiddenLayer1Weights,inputValues.T)
        Z1 = np.tanh(Z1)
        Z2 = np.matmul(self.hiddenLayer2Weights,Z1)
        Z2 = np.tanh(Z2)
        output = np.matmul(self.outputLayerWeights,Z2)
        return output
    
    def MoveNeuralNetwork(self,wallCoordinates,initialCoordinates,checkpointCoordinates,finalCoordinates,enemyCoordinates):
        outputDict = {
            0:'Left',
            1:'Up',
            2:'Right',
            3:'Down'
        }

        self.MetricsCalculation(wallCoordinates,initialCoordinates,checkpointCoordinates,finalCoordinates,enemyCoordinates)

        output = self.ForwardPropagation()
        #Output will be a vector of 4 values. We'll get the max
        directionToGo = outputDict[np.argmax(output)]

        moved = self.GoDirection(directionToGo,wallCoordinates,checkpointCoordinates,finalCoordinates)
        if moved == False:
            self.stepsInSameCoordinates = self.stepsInSameCoordinates + 1
            if self.stepsInSameCoordinates >= self.limitStepsSameCoordinates:
                self.isDead = True
                self.color('cornflower blue')
        else:
            self.stepsInSameCoordinates = 0
        
        self.CalculateFitness(initialCoordinates,finalCoordinates)
        
        return moved
