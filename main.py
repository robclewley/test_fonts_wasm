# /// script
# dependencies = [
#     "pygame-ce",
#     "python-i18n"
# ]
# ///
import asyncio
import pygame
import pygame_gui
import i18n

from pygame_gui.core import ObjectID


async def main():
    gui_dims = (800, 600)
    screen = pygame.display.set_mode(gui_dims, pygame.SRCALPHA)
    pygame.font.init()
    pygame.freetype.init()
    pygame.display.init()

    gui_manager = pygame_gui.UIManager(gui_dims,
                                       "test_fonts/ui_theme.json")
#                             pygame_gui.PackageResource(package="test_fonts",
#                                                 resource='ui_theme.json'))

    text = pygame_gui.elements.UILabel(
            pygame.Rect(50, 50, 250, 30),
            "These are working TTF fonts!",
            manager=gui_manager,
            object_id=ObjectID("@test")
    )

    background = pygame.Surface(gui_dims)
    background.fill("#333333")

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

        dt = clock.tick(60) / 1000
        screen.blit(background, (0, 0))
        gui_manager.draw_ui(screen)

        gui_manager.update(dt)
        pygame.display.update()
        await asyncio.sleep(0)
    pygame.quit()

asyncio.run(main())
