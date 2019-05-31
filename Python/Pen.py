import turtle
class Pen(turtle.Turtle):
    def __init__(self,color='White'):
        turtle.Turtle.__init__(self)
        self.shape('square')
        self.color(color)
        self.penup()
        self.speed(0)
        pass       