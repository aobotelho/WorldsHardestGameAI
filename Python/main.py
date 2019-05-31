import turtle
from time import sleep
import random
from sys import getsizeof

from Player import Player
from Enemy import Enemy
from Maze_Functions import *

totalNumberOfPlayers = 100

level = ['xxxxxxxxxxxxxxxxxxxxxxxxxx',
  'xssssxxx              fxxx',
  'xssssxxx              xxxx',
  'xssssxxx              xxxx',
  'xssssxxx             xxxxx',
  'xssssxxx           e xxxxx',
  'xssssxxx             xxxxx',
  'xssssxxxe            xxxxx',
  'xssssxxx             xxxxx',
  'xssssxxx           e xxxxx',
  'xssssxxx             xxxxx',
  'xssssxxxe            xxxxx',
  'xssssxxx             xxxxx',
  'xssssxxx           e xxxxx',
  'xssssxxx             xxxxx',
  'xssssxxxe            xxxxx',
  'xssssxxx             xxxxx',
  'xssssxxx           e xxxxx',
  'xssssxxx             xxxxx',
  'xssssxxx             xxxxx',
  'x    xxx   xxxxxxxxxxxxxxx',
  'x          xxxxxxxxxxxxxxx',
  'x          xxxxxxxxxxxxxxx',
  'x          xxxxxxxxxxxxxxx',
  'xxxxxxxxxxxxxxxxxxxxxxxxxx']


wn = turtle.Screen()
wn.bgcolor('Black')
wn.title('Maze')
wn.setup(700,700)
wn.tracer(0)


turtle.listen()
#Press q to quit
turtle.onkey(lambda: wn.bye(),'q')

#Pens and colors
wall = Pen('white')
start = Pen('Yellow Green')
final = Pen('Sea Green')
#7 Enemies
enemyVars = [Enemy(x,'Red') for x in range(7)]

#Print everything on the screen
wallCoordinates,initialCoordinates,finalCoordinates,enemyCoordinates = setup_maze(level,wall,start,final,enemyVars)
checkpointCoordinates = [(-96,-192),(-72,-192),(-48,-192)]

#Put players on random positions indicated by "s" in the maze definition
playerList = PositionPlayers(numberOfPlayers=totalNumberOfPlayers,possibleInitialPositions=initialCoordinates)

go = True
counter = 0
maxSteps = 5
gen = 1
'''while go:
    for maxSteps in range(5,200,5):
        for _ in range(5):
            for _ in range(maxSteps):
                try:                
                    _ = [player.MoveNeuralNetwork(wallCoordinates,initialCoordinates,checkpointCoordinates,finalCoordinates,enemyCoordinates) for player in playerList[::-1] if player.isDead == False]
                    if counter%2 == 0:
                        _ = [enemyVars[i].MoveEnemy(wallCoordinates,finalCoordinates) for i in range(len(enemyVars))]
                        enemyCoordinates = [enemyVars[i].CurrentCoordinates() for i in range(len(enemyVars))]
                        counter = 0
                    else:
                        counter = counter + 1
                    
                    wn.update()
                    _ = [playerList[i].CollisionWithEnemy(enemyCoordinates) for i in range(len(playerList))]

                    somePlayerReachedEnd = sum([1 if playerList[i].endGameFlag == True else 0 for i in range(len(playerList))])

                    someoneStillAlive = False
                    for i in range(len(playerList)):
                        if playerList[i].isDead == False:
                            someoneStillAlive = True
                            break
                    if someoneStillAlive == False:
                        break
                except Exception as e:
                    go = False


            ########################################################################
            # Crossover and mutations now!
            ########################################################################
            wn.update()
            playerList = GeneticAlgorithm(playerList)
            _ = [playerList[i].goto(random.choice(initialCoordinates)) for i in range(len(playerList))]
            _ = [playerList[i].ResetDefaults() for i in range(len(playerList))]
            gen = gen+1
        
            turtle.penup()
            turtle.clear()
            turtle.hideturtle()
            turtle.goto(-300,320)
            turtle.color('red')
            turtle.write('Generation: {}'.format(gen),align='center')
            turtle.goto(-300,310)
            turtle.write('Max Steps: {}'.format(maxSteps),align='center')
'''     
        

while go:
    try:                
        _ = [player.MoveNeuralNetwork(wallCoordinates,initialCoordinates,checkpointCoordinates,finalCoordinates,enemyCoordinates) for player in playerList[::-1] if player.isDead == False]
        if counter%2 == 0:
            _ = [enemyVars[i].MoveEnemy(wallCoordinates,finalCoordinates) for i in range(len(enemyVars))]
            enemyCoordinates = [enemyVars[i].CurrentCoordinates() for i in range(len(enemyVars))]
            counter = 0
        else:
            counter = counter + 1
        
        wn.update()
        _ = [playerList[i].CollisionWithEnemy(enemyCoordinates) for i in range(len(playerList))]

        somePlayerReachedEnd = sum([1 if playerList[i].endGameFlag == True else 0 for i in range(len(playerList))])

        someoneStillAlive = False
        for i in range(len(playerList)):
            if playerList[i].isDead == False:
                someoneStillAlive = True
                break
        if someoneStillAlive == False:

            ########################################################################
            # Crossover and mutations now!
            ########################################################################
            wn.update()
            playerList = GeneticAlgorithm(playerList)
            _ = [playerList[i].goto(random.choice(initialCoordinates)) for i in range(len(playerList))]
            _ = [playerList[i].ResetDefaults() for i in range(len(playerList))]
            gen = gen+1

            turtle.penup()
            turtle.clear()
            turtle.hideturtle()
            turtle.goto(-300,320)
            turtle.color('red')
            turtle.write('Generation: {}'.format(gen),align='center')
            turtle.goto(-300,310)
            turtle.write('Max Steps: {}'.format(maxSteps),align='center')

    except Exception as e:
        go = False