import pygame

def pause_game(screen, medium_font, width, height):
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                paused = False

        screen.fill(pygame.Color("black"))
        pause_text = medium_font.render("游戏暂停中", True, pygame.Color("white"))
        screen.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2))
        pygame.display.flip()
        pygame.time.Clock().tick(5)
