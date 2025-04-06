import pygame

pygame.init
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
runing = True
walking = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
    
    screen.fill("black")
    pygame.draw.circle(screen, "green", player_pos, 40)

    keys = pygame.key.get_pressed()
        

    if keys[pygame.K_w]:
        while True:
            player_pos.y -= 300*dt
            if walking == False:
                break
            
    if keys[pygame.K_s]:
        player_pos.y += 300*dt
        
    # if keys[pygame.K_d]:
    #     player_pos.x += 300*dt
    # if keys[pygame.K_a]:
    #     player_pos.x -= 300*dt

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()


