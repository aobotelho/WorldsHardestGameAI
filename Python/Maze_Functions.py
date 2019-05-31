from Pen import Pen
from Player  import Player
import numpy as np
import random

def setup_maze(level,wallVar,startVar,finalVar,enemyVarList):
    wallCoordinates = []
    startCoordinates = []
    finalCoordinates = []
    enemyCoordinates = []
    backVar = Pen('Gray')
    enemies = 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            
            screen_x = -288 + (x*24)
            screen_y =  288 - (y*24)
            
            if character == 'x':
                wallVar.goto(screen_x,screen_y)
                wallVar.stamp()
                wallCoordinates.append((screen_x,screen_y))
            elif character == 's':
                startVar.goto(screen_x,screen_y)
                startVar.stamp()
                startCoordinates.append((screen_x,screen_y))
            elif character == 'f':
                finalVar.goto(screen_x,screen_y)
                finalVar.stamp()
                finalCoordinates.append((screen_x,screen_y))
            elif character == 'e':
                backVar.goto(screen_x,screen_y)
                backVar.stamp()
                enemyVarList[enemies].goto(screen_x,screen_y)
                enemies = enemies + 1
                enemyCoordinates.append((screen_x,screen_y))
            else:
                backVar.goto(screen_x,screen_y)
                backVar.stamp()
            
    Pen('Gray')
    return wallCoordinates,startCoordinates,finalCoordinates,enemyCoordinates

def clear_maze(level):
    clearVar = Pen('Gray')
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            
            screen_x = -288 + (x*24)
            screen_y =  288 - (y*24)
            clearVar.goto(screen_x,screen_y)
            clearVar.stamp()
    pass

def PositionPlayers(numberOfPlayers,possibleInitialPositions,playerColors='blue'):
    playerList = [Player(playerColors) for x in range(numberOfPlayers)]
    _ = [playerList[i].goto(random.choice(possibleInitialPositions)) for i in range(len(playerList))]
    return playerList

def GeneticAlgorithm(playerList):
    #Sorting by fitness value. 
    #The lowest the fitness the better
    playerList = sorted(playerList,key=lambda x: x.fitness,reverse=True)
    #Number of parent to survive
    numberOfParents = int(0.2*len(playerList))
    #numberOfParents = 1
    
    #Iterate over all child players
    for childPlayer in playerList[numberOfParents:]:
        #For each node in the layers we'll get one of the parent's weights, randomly
        #Number of nodes = .shape[0]
        #Weights = .shape[1]
        for node in range(childPlayer.hiddenLayer1Weights.shape[0]):
            childPlayer.hiddenLayer1Weights[node] = np.random.choice(playerList[:numberOfParents]).hiddenLayer1Weights[node]

        for node in range(childPlayer.hiddenLayer2Weights.shape[0]):
            childPlayer.hiddenLayer2Weights[node] = np.random.choice(playerList[:numberOfParents]).hiddenLayer2Weights[node]

        for node in range(childPlayer.outputLayerWeights.shape[0]):
            childPlayer.outputLayerWeights[node] = np.random.choice(playerList[:numberOfParents]).outputLayerWeights[node]
    
    #Now all the childs have crossover genes. Lets mutate them
    #We'll choose two nodes from each layer and change its weight
    for childPlayer in playerList[numberOfParents:]:
        #Choose two random indexes in hidden layer 
        for randIndex in np.random.choice(range(childPlayer.hiddenLayer1Weights.shape[0]),size=(2)):
            childPlayer.hiddenLayer1Weights[randIndex] = np.clip(childPlayer.hiddenLayer1Weights[randIndex] + np.random.choice(np.arange(-0.3,0.3,step=0.001),size=(childPlayer.hiddenLayer1Weights.shape[1]),replace=False),-1,1)
        for randIndex in np.random.choice(range(childPlayer.hiddenLayer2Weights.shape[0]),size=(2)):
            childPlayer.hiddenLayer2Weights[randIndex] = np.clip(childPlayer.hiddenLayer2Weights[randIndex] + np.random.choice(np.arange(-0.3,0.3,step=0.001),size=(childPlayer.hiddenLayer2Weights.shape[1]),replace=False),-1,1)
        for randIndex in np.random.choice(range(childPlayer.outputLayerWeights.shape[0]),size=(2)):
            childPlayer.outputLayerWeights[randIndex] = np.clip(childPlayer.outputLayerWeights[randIndex] + np.random.choice(np.arange(-0.3,0.3,step=0.001),size=(childPlayer.outputLayerWeights.shape[1]),replace=False),-1,1)
    
    return playerList
