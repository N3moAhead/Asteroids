import pygame

pygame.init()

screen = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill((255, 0, 0))
    pygame.draw.rect(screen, (20, 20, 20), (100, 100, 50, 50))
    clock.tick(45)
