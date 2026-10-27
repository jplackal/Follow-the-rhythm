import asyncio
import pygame

pygame.init()

WIDTH = 1300
HEIGHT = 750

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Follow the Rythm")

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
        pygame.display.flip()

        # Required for Pygbag / browser builds
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())
