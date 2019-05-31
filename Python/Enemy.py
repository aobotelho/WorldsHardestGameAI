from Player import Player
class Enemy(Player):
    def __init__(self,enemyNumber,color='Red'):
        Player.__init__(self,color)
        if enemyNumber%2 == 0:
            self.xVel = -1
            self.yVel = 0
        else:
            self.xVel = +1
            self.yVel = 0
        pass
    def MoveEnemy(self,wallCoordinates,finalCoordinates):
        direction = 'Left' if self.xVel < 0 else 'Right'
        moved = self.GoDirection(direction,wallCoordinates,None,finalCoordinates)
        if moved == False:
            self.xVel = self.xVel * -1
            direction = 'Left' if self.xVel < 0 else 'Right'
            moved = self.GoDirection(direction,wallCoordinates,None,finalCoordinates)
        return moved
    
    def CurrentCoordinates(self):
        return (self.xcor(),self.ycor())