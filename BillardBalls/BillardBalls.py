import pygame
import random
import math
import numpy as np

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION
)

pygame.init()

#simulation variables
screenWidth = 1920 
screenHeight = 1080
rate = 144 # FPS
dt = 1 / rate
damp = 100

class Circle():
    def __init__(self, x = 0, y = 0, velX = 0, velY = 0, color = (255, 255, 255), radius = 5):
        self.x = x
        self.y = y
        self.velX = velX
        self.velY = velY
        self.color = color
        self.radius = radius

#create multiples circles

numberOfCircles = 100
circles = []
for i in range(numberOfCircles):
    circle = Circle()
    circle.x = random.randint(1, screenWidth - 1)
    circle.y = random.randint(1, screenHeight - 1)
    circle.velX = random.randint(-500, 500)
    circle.velY = random.randint(-500, 500)
    circle.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    circle.radius = 10
    circles.append(circle)



def border_collision_detection(x, y, radius):    
    return None

screen = pygame.display.set_mode([screenWidth, screenHeight])

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 0, 0))
    
    #draw circles
    for circle in circles:
        pygame.draw.circle(screen, circle.color, (circle.x, circle.y), circle.radius)
        circle.x = circle.x + circle.velX * dt 
        circle.y = circle.y + circle.velY * dt
        circle.velY = circle.velY + 1000 * dt
    
    #dedect border collision
    for circle in circles:
        if circle.x >= screenWidth - circle.radius:
            circle.x = screenWidth - circle.radius
            circle.velX = -circle.velX + damp
        if circle.x <= circle.radius:
            circle.x = circle.radius
            circle.velX = -circle.velX - damp
        if circle.y >= screenHeight - circle.radius:
            circle.y = screenHeight - circle.radius
            circle.velY = -circle.velY + damp
        if circle.y <= circle.radius:
            circle.y = circle.radius
            circle.velY = -circle.velY - damp
  
    #dedect circle collision
    for circle in circles:
        for circle2 in circles:
            if circle != circle2:
                distanceSquared = (circle.x - circle2.x)**2 + (circle.y - circle2.y)**2 
                if distanceSquared <= (circle.radius + circle2.radius)**2:
                    #2D elastic collision
                    dotProduct = (circle.velX - circle2.velX) * (circle.x - circle2.x) + (circle.velY - circle2.velY) * (circle.y - circle2.y)
                    circle.velX = circle.velX - dotProduct * (circle.x - circle2.x) / distanceSquared
                    circle.velY = circle.velY - dotProduct * (circle.y - circle2.y) / distanceSquared
                    circle2.velX = circle2.velX + dotProduct * (circle.x - circle2.x) / distanceSquared
                    circle2.velY = circle2.velY + dotProduct * (circle.y - circle2.y) / distanceSquared
                    #move circles out of each other
                    distance = math.sqrt(distanceSquared)
                    overlap = 0.5 * (distance - circle.radius - circle2.radius)
                    circle.x = circle.x - overlap * (circle.x - circle2.x) / distance
                    circle.y = circle.y - overlap * (circle.y - circle2.y) / distance
                    circle2.x = circle2.x + overlap * (circle.x - circle2.x) / distance
                    circle2.y = circle2.y + overlap * (circle.y - circle2.y) / distance
              
    pygame.display.flip()
    clock.tick(rate)
    
pygame.quit()
