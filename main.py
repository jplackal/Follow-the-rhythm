import asyncio
import pygame

pygame.init()
screen_mult = 1.2
WIDTH =500
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Follow the Rythm")
background = pygame.image.load("assets/image_assets/ftr_bg.png").convert()
start_button = pygame.image.load("assets/image_assets/start.png").convert_alpha()
start_button = pygame.transform.smoothscale(start_button, ((start_button.get_height())*0.1, (start_button.get_width())*0.1))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)

#mv ~/Downloads/start.png ~/Desktop/hack_club_projects/follow_the_rythm/assets/image_assets/



async def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(start_button, (150, 400))
        pygame.display.flip()

        # Required for Pygbag / browser builds
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())
