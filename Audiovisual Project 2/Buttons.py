import pygame
import time

import sys
from os import path
global screen
global infoObject
global screen_h
global screen_w

pygame.init()
pygame.mixer.init()
infoObject = pygame.display.Info()

screen_w = int(infoObject.current_w)
screen_h = int(infoObject.current_w/2 +25)

screen = pygame.display.set_mode([screen_w, screen_h])

play = pygame.image.load("play.png").convert_alpha()
pause = pygame.image.load('pausa.png').convert_alpha()
line = pygame.image.load("line_image.png").convert_alpha()
circle = pygame.image.load("circle_image.png").convert_alpha()
folder = pygame.image.load("Search a song!.png").convert_alpha()
forward = pygame.image.load("adelante.png").convert_alpha()
back = pygame.image.load("anterior.png").convert_alpha()
select_text = pygame.image.load("select_text.png").convert_alpha()


image1 = pause
image2 = folder
image3 = forward
image4 = back

image10 = line
image11 = circle

shape_number = 1
its_playing = True


#######################RIGHT PART CLASSES######################
#1
class Button_play():
    def __init__(self, x, y, play, pause):
        self.play = pygame.transform.scale(play, (50, 50))
        self.pause = pygame.transform.scale(pause, (50, 50))
        self.rect = self.play.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        global image1
        image1 = self.pause

    def draw(self):
        pressed = False
        #get mousse position
        pos = pygame.mouse.get_pos()
        global image1
        global its_playing
        #check mouseover and cliked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                pressed = True
                if its_playing:
                    image1 = self.play
                    its_playing = False

                else:
                    image1 = self.pause
                    its_playing = True

        #reset self.clicked when mouse isn't pressed
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            pressed = False

        screen.blit(image1, (self.rect.x, self.rect.y))

        return pressed


#2
class Button_folder():
    def __init__(self, xfolder, yfolder, folder):
        self.folder = pygame.transform.scale(folder, (100, 100))
        self.rect = self.folder.get_rect()
        self.rect.topleft = (xfolder, yfolder)
        self.clicked = False
        global image2
        image2 = self.folder

    def draw(self):
        pressed = False
        pos = pygame.mouse.get_pos()
        #check mouseover and cliked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                pressed = True
            else:
                pressed = False

        screen.blit(image2, (self.rect.x, self.rect.y))
        return pressed
#3
class Button_forward():
    def __init__(self, xforward, yforward, forward):
        self.forward = pygame.transform.scale(forward, (50, 50))
        self.rect = self.forward.get_rect()
        self.rect.topleft = (xforward, yforward)
        self.clicked = False
        global image3
        image3 = self.forward

    def draw(self):
        pressed = False
        pos = pygame.mouse.get_pos()
        #check mouseover and cliked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:

                self.clicked = True
                pressed = True

            else:
                pressed = False

        screen.blit(image3, (self.rect.x, self.rect.y))
        return pressed
#4
class Button_back():
    def __init__(self, xback, yback, back):
        self.back = pygame.transform.scale(back, (50, 50))
        self.rect = self.back.get_rect()
        self.rect.topleft = (xback, yback)
        self.clicked = False
        global image4
        image4 = self.back

    def draw(self):
        pressed = False
        pos = pygame.mouse.get_pos()
        #check mouseover and cliked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                pressed = True

            else:
                pressed = False

        screen.blit(image4, (self.rect.x, self.rect.y))
        return pressed


#######################DOWN PART CLASSES################
#10
class Button_line():
    def __init__(self, xline, yline, line):
        self.line = pygame.transform.scale(line, (100, 100))
        self.rect = self.line.get_rect()
        self.rect.topleft = (xline, yline)
        self.clicked = False
        global image10
        image10 = self.line

    def draw(self):
        pressed = False
        #get mousse position
        pos = pygame.mouse.get_pos()

        #check mouseover and cliked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                pressed = True

            else:
                pressed = False

        screen.blit(image10, (self.rect.x, self.rect.y))
        return pressed
#11
class Button_circle():
    def __init__(self, xcircle, ycircle, circle):
        self.circle = pygame.transform.scale(circle, (100, 100))
        self.text = pygame.transform.scale(select_text, (250, 50))
        self.rect = self.circle.get_rect()
        self.rect.topleft = (xcircle, ycircle)
        self.clicked = False
        global image11
        image11 = self.circle

    def draw(self):
        pressed = False
        #get mousse position
        pos = pygame.mouse.get_pos()

        #check mouseover and cliked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                pressed = True
                shape_number = 2
            else:
                pressed = False

        screen.blit(image11, (self.rect.x, self.rect.y))
        screen.blit(self.text, (self.rect.x - 300, self.rect.y))

        return pressed


###########################RIGHT PART##################
x = int(screen_w/2) - 30
y = screen_h - screen_h/8
play_button = Button_play(x, y, play, pause)

xfolder = 50
yfolder = y - 10
folder_button = Button_folder(xfolder, yfolder, folder)

xforward = x + 100
yforward = y
forward_button = Button_forward(xforward, yforward, forward)
xback = x - 100
yback = y
back_button = Button_back(xback, yback, back)


#####################DOWN PART######################
xcircle = screen_w - 250
ycircle = y
circle_button = Button_circle(xcircle, ycircle, circle)

xline = xcircle + 110
yline = y
line_button = Button_line(xline, yline, line)