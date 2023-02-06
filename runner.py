import pygame
import sys
from game_of_life import GameofLife
import matplotlib
import matplotlib.pyplot as plt
import datetime

pygame.init()
pygame.display.set_caption("Conway's Game of Life")

WIDTH = 1200
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

conway = GameofLife(screen, scale=13)

clock = pygame.time.Clock()
fps = 0.5
counter = 0
totalHerb = 0
totalCarn = 0

while True:
    clock.tick(fps)
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
         
            
            print("Herb: ", totalHerb/counter)
            print("Carn: ", totalCarn/counter)
            print("total: ", (totalHerb+totalCarn)/counter)


            

            pygame.quit()
            sys.exit()

    conway.run()

    pygame.display.update()
    
    counter += 1 
    totalHerb += conway.getHerb()
    totalCarn += conway.getCarn()
