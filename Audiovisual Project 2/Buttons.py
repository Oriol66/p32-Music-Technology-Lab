import pygame

pygame.init()

infoObject = pygame.display.Info()

screen_w = int(infoObject.current_w-50)
screen_h = int(infoObject.current_w/2)

screen = pygame.display.set_mode([screen_w, screen_h])

play = pygame.image.load("play.png").convert_alpha()
pause = pygame.image.load('pausa.png').convert_alpha()

image = pause
its_playing = True


class Button():
    def __init__(self, x, y, play, pause):
        self.play = pygame.transform.scale(play, (100, 100))
        self.pause = pygame.transform.scale(pause, (100, 100))
        self.rect = self.play.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        global image
        image = self.pause

    def draw(self):
        pressed = False
        #get mousse position
        pos = pygame.mouse.get_pos()
        global image
        global its_playing
        #check mouseover and cliked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                pressed = True
                if its_playing:
                    image = self.play
                    its_playing = False

                else:
                    image = self.pause
                    its_playing = True

        #reset self.clicked when mouse isn't pressed
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            pressed = False

        screen.blit(image, (self.rect.x, self.rect.y))

        return pressed

x = screen_w - screen_w/6
y = screen_h/4
play_button = Button(x, y, play, pause)