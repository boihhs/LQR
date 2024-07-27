import car
import pygame
import math
import lqr
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


# Main loop
running = True
clock = pygame.time.Clock()

startx = [500, 500, 0, 0]
car = car.Car(x=startx[0], y=startx[1], vx=startx[2], vy=startx[3], dt = clock.tick(60) / 1000)

dt = clock.tick(60) / 1000
thrust = 200
A = car.A
B = car.B
sec = 10

Q = np.diag(np.diag(np.zeros((len(car.x), len(car.x))) + 50))
Qfinal = np.diag(np.diag(np.zeros((len(car.x), len(car.x))) + 100))
R = np.diag(np.diag(np.zeros((len(car.u), len(car.u))) + .1))

lqr = lqr.LQR(A, B, Q, Qfinal, R, dt, sec)

K = lqr.fhlqr()

for i in range(int(sec/dt)-1):
    car.u = -K[i]@car.x
    car.update()
    car.previous_positions.append((int(car.x[0] + car.width/2), int(car.x[1] + car.height/2)))

car.x = startx


step = 0
totalSteps = int(sec/dt)
while running:
    dt = clock.tick(60) / 1000  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle user input
    keys = pygame.key.get_pressed()

    
    if keys[pygame.K_UP]:
        car.u[1] = -1
    elif keys[pygame.K_DOWN]:
        car.u[1] = 1
    else: 
        car.u[1] = 0
    
    if keys[pygame.K_LEFT]:
        car.u[0] = -1  
    elif keys[pygame.K_RIGHT]:
        car.u[0] = 1
    else: car.u[0] = 0
    
    # Update car dynamics
    #car.previous_positions, costs, action = mppi.allPaths(car.x)
    
    #car.u = action
    if step < totalSteps - 1:
        car.u = -K[step]@car.x
        step += 1
        #print(car.u)
    else:
        car.u = [0,0]
        print(car.x)
    

    car.update()
    screen.fill(WHITE)
    
    for i in range(len(car.previous_positions)):
        screen.set_at((car.previous_positions[i][0] + WIDTH // 2, car.previous_positions[i][1] + HEIGHT // 2), (255,0,0))
        
    """      
    for i in range(len(car.previous_positions[len(car.previous_positions)-1])):
        screen.set_at((car.previous_positions[len(car.previous_positions)-1][i][0] + WIDTH // 2, car.previous_positions[len(car.previous_positions)-1][i][1] + HEIGHT // 2), (0,0,255))
    """
    # Draw everything
    #pygame.draw.rect(screen, (255,255,0), (WIDTH // 2-100, HEIGHT // 2 - 100, 200, 200))
    
    pygame.draw.rect(screen, BLACK, (int(car.x[0]) + WIDTH // 2, int(car.x[1]) + HEIGHT // 2, car.width, car.height))

    pygame.display.flip()

pygame.quit()
