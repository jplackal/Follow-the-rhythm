import asyncio
import pygame

pygame.init()
screen_mult = 1.2
WIDTH =500
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Follow the Rythm")
background = pygame.image.load("assets/image_assets/ftr_bg.png").convert()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)


async def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        pygame.display.flip()

        # Required for Pygbag / browser builds
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())
