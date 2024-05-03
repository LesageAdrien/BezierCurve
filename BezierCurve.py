import pygame as pg
import numpy as np
SCREEN_SIZE = (1000,800)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
DARK_GREY = (70,70,70)
BLUE = (100,100,255)
class BezierCurve():
    def __init__(self, n = 100):
        self.points = None
        self.curve = []
        self.temp = []
        self.animationTime = 0
        self.n = n
    def add(self, point):
        if type(self.points) == type(None):
            self.points = np.array(point)
        else:
            self.points = np.vstack((self.points,np.array(point)))
            self.compute()
    def disp(self,scr):
        if len(self.curve) != 0:
            print(self.curve.shape)
            pg.draw.lines(scr, BLUE, False, self.curve.T, 4)
            for i in range(len(self.points)):
                pg.draw.circle(s, DARK_GREY, self.points[i], 3)
        elif type(self.points) != type(None):
            pg.draw.circle(s, WHITE, self.points, 3)
    def compute(self):
        t = np.matrix(np.linspace(0,1,self.n)).T
        T = np.diag(np.linspace(0,1,self.n))
        L = []
        r = self.points.shape[0]

        Tmp_L = []
        for i in range(len(self.points[0])):
            Tmp_L.append( np.array(t*np.matrix(self.points[1:,i])  +   (1-t) * np.matrix(self.points[:-1,i])))
        L.append(Tmp_L)

        if r > 2:
            for j in range(r-2):
                Tmp_L = []
                for M in L[-1]:
                    Tmp_L.append( T.dot(M[:,1:] - M[:,:-1]) +  M[:,:-1] )
                L.append(Tmp_L)
        self.temp = L[:-1]
        self.curve =  np.array(L[-1]).reshape((2,100))
    def animation(self, scr, speed = 1):
        self.animationTime = (self.animationTime + speed)%100
        i = int(self.animationTime)
        if len(self.curve) != 0:

            pg.draw.lines(scr, DARK_GREY, False, self.points)
            for L in self.temp:
                for j in range(L[0].shape[1]-1):
                    pg.draw.line(scr, DARK_GREY, (L[0][i,j], L[1][i,j]), (L[0][i,j+1], L[1][i,j+1]), 1)
            pg.draw.circle(scr, RED, self.curve[:,i], 10)
pg.init()

bc = BezierCurve()

scr = pg.display.set_mode(SCREEN_SIZE)
s = pg.Surface(SCREEN_SIZE)
s.fill(BLACK)
running = True
clicking = False
clock = pg.time.Clock()
while running:
    scr.blit(s,(0,0))
    bc.animation(scr, 0.3)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False ; print("STOP")

    if pg.mouse.get_pressed()[2]:
        bc = BezierCurve()
        s.fill(BLACK)
    if pg.mouse.get_pressed()[0]:
        if not clicking:
            bc.add(pg.mouse.get_pos())
            s.fill(BLACK)
            bc.disp(s)
            clicking = True
    else:
        clicking = False
    pg.display.flip()
    clock.tick(60)

pg.quit()
