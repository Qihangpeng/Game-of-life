import pygame
import numpy as np

class Cell:
    def __init__(self):
        # 1:herbivore
        # 2:carnivore
        # 3:Grass
        # 4:Barren
        # 5:River
        # 6:dead
        self.type=np.random.randint(0, 7)
        self.alive=np.random.randint(0, 2, dtype=bool)

class GameofLife:
    def __init__(self, surface, width=1200, height=800, scale=10, offset=1, active_color=(255, 255, 255), inactive_color=(26, 51, 50)):
        self.surface = surface
        self.width = width
        self.height = height
        self.scale = scale
        self.offset = offset
        self.active_color = active_color
        self.inactive_color = inactive_color

        self.columns = int(height / scale)
        self.rows = int(width / scale)

        self.grid = np.random.randint(0, 2, size=(self.rows, self.columns), dtype=bool)
        self.nodes = [[Cell() for j in range(self.columns)] for i in range(self.rows)]

    
        
    def draw_grid(self):
      """Drawing the grid"""
      
      for row in range(self.rows):
         for col in range(self.columns):
            if self.nodes[row][col].type==1:
                #herbivore: yellow
                pygame.draw.rect(self.surface, (255,255,0), [row * self.scale, col * self.scale, self.scale - self.offset, self.scale - self.offset])
            elif self.nodes[row][col].type==2:
                #carnivore: red
                pygame.draw.rect(self.surface, (255, 0, 0), [row * self.scale, col * self.scale, self.scale - self.offset, self.scale - self.offset])
            elif self.nodes[row][col].type==3:
                #green land: green
                pygame.draw.rect(self.surface, (100, 252, 0), [row * self.scale, col * self.scale, self.scale - self.offset, self.scale - self.offset])

            elif self.nodes[row][col].type==4:
                #barren: white
                pygame.draw.rect(self.surface, (255,248,220), [row * self.scale, col * self.scale, self.scale - self.offset, self.scale - self.offset])
            elif self.nodes[row][col].type==5:
                #water: blue
                pygame.draw.rect(self.surface, (0, 0, 255), [row * self.scale, col * self.scale, self.scale - self.offset, self.scale - self.offset])
 
            else:
                #dead
                pygame.draw.rect(self.surface, self.inactive_color, [row * self.scale, col * self.scale, self.scale - self.offset, self.scale - self.offset])

    def update_grid(self):
       """Updating the grid based on Conway's game of life rules"""
       updated_grid = self.nodes.copy()
       updated_grid_ori = self.grid.copy()
       for row in range(updated_grid_ori.shape[0]):
         for col in range(updated_grid_ori.shape[1]):
            updated_grid[row][col] = self.update_cell(row, col)

       self.nodes = updated_grid


    def update_cell(self, x, y):
       """Update single cell based on Conway's game of life rules"""
       #current_state = self.grid[x, y]
       current_state=self.nodes[x][y].type
       alive_neighbors = 0
       river_neighbors = 0
       grass_neighbors = 0
       grasseater_neighbors = 0
       meateater_neighbors = 0
      # Get to how many alive neighbors
       for i in range(-1, 2):
         for j in range(-1, 2):
            try:
                if i == 0 and j == 0:
                    continue
                elif self.nodes[x + i][y + j].type==1:
                    grasseater_neighbors += 1
                    alive_neighbors += 1
                elif self.nodes[x + i][y + j].type==5:
                    river_neighbors += 1
                elif self.nodes[x + i][y + j].type==3:
                    grass_neighbors += 1
                elif self.nodes[x + i][y + j].type==2:
                    meateater_neighbors += 1
                    alive_neighbors += 1
            except:
                continue

       # Updating the cell's state
       if current_state==1 and river_neighbors==0:
          self.nodes[x][y].type=6

       # grasseater no grass or water
       elif current_state==1 and (river_neighbors == 0 or grass_neighbors == 0):
          self.nodes[x][y].type =6
          
          
       # grasseater too many preditor
       elif current_state==1 and river_neighbors > 0 and grass_neighbors > 0 and meateater_neighbors >3 :
          self.nodes[x][y].type =6
          
       # meateater no grass or water or over population
       elif current_state==2 and (river_neighbors==0 or grasseater_neighbors==0 or meateater_neighbors > 3):
          self.nodes[x][y].type =6
          
       # grass eatten by grasseater
       elif current_state==3 and grasseater_neighbors>=2:
          self.nodes[x][y].type =4
    
       # grass growing back from dirt
       elif current_state==4 and grass_neighbors>=2:
          self.nodes[x][y].type =3
          
       # grass eater reproduction
       elif current_state==6 and grasseater_neighbors >=2 and grasseater_neighbors >= meateater_neighbors:
          self.nodes[x][y].type =1
          
       #meateater reproduction
       elif current_state==6 and meateater_neighbors >=2 and grasseater_neighbors < meateater_neighbors:
          self.nodes[x][y].type =2
       
       #grass reproduction
       elif current_state==6 and alive_neighbors<3 :
          self.nodes[x][y].type =3
       
       
       return self.nodes[x][y]


    def getHerb(self):
        herb_counter = 0
        for row in range(self.rows):
         for col in range(self.columns):
            if self.nodes[row][col].type==1:
                herb_counter += 1

        return herb_counter
    def getCarn(self):
        carn_counter = 0
        for row in range(self.rows):
         for col in range(self.columns):
            if self.nodes[row][col].type==2:
                carn_counter += 1

        return carn_counter
                
    def run(self):
      """"Update and redraw the current grid state"""
      self.draw_grid()
      self.update_grid()


