import pygame
import random
import sys
import ai_player
import const
from game import Game

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
        self.game = Game()

        pygame.display.set_caption("Chess AI")

    def main_loop(self):
        game = self.game
        screen = self.screen
        dragger = self.game.dragger

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                

            game.draw_board(screen)

            pygame.display.update()



main = Main()
main.main_loop()
