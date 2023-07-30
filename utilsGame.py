from utils import *
import pygame
import os

HEIGTH = 720
WIDTH = 1080

OPTION_HEIGTH = 80
OPTION_WIDTH = 100

WHITE = (255, 255, 255)

pygame.init()
pygame.display.set_caption("Jokenpo")
screen = pygame.display.set_mode((WIDTH, HEIGTH))
font = pygame.font.SysFont(None, 48)

rock_image = pygame.image.load(os.path.join('images', 'pedra.png'))
paper_image = pygame.image.load(os.path.join('images', 'papel.png'))
scissor_image = pygame.image.load(os.path.join('images', 'tesoura.png'))

class Button_Image():
    def __init__(self, x, y, image, heigth, width):
        self.image = pygame.transform.scale(image, (width, heigth))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x , y)
        self.clicked = False
    
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        return action