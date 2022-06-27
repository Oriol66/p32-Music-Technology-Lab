import pygame

global screen
global infoObject
global screen_h
global screen_w

pygame.init()
pygame.mixer.init()
infoObject = pygame.display.Info()

screen_w = 1000
screen_h = 600

screen = pygame.display.set_mode([screen_w, screen_h])

play = pygame.image.load("images/play.png").convert_alpha()
pause = pygame.image.load('images/pausa.png').convert_alpha()
line = pygame.image.load("images/line_image.png").convert_alpha()
circle = pygame.image.load("images/circle_image.png").convert_alpha()
folder = pygame.image.load("images/search.png").convert_alpha()
folder_text = pygame.image.load("images/Search a song!.png").convert_alpha()
select_text = pygame.image.load("images/select_text.png").convert_alpha()


image1 = pause
image2 = folder

image10 = line
image11 = circle

shape_number = 1
its_playing = True


#######################RIGHT PART CLASSES######################
#1
class Button_play():
    def __init__(self, x, y, play, pause):
        self.play = pygame.transform.scale(play, (90, 90))
        self.pause = pygame.transform.scale(pause, (90, 90))
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
        self.folder = pygame.transform.scale(folder, (80, 80))
        self.text = pygame.transform.scale(folder_text, (150, 30))
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
        screen.blit(self.text, (self.rect.x + 100, self.rect.y + 50))
        return pressed

#######################DOWN PART CLASSES################
#10
class Button_line():
    def __init__(self, xline, yline, line):
        self.line = pygame.transform.scale(line, (80, 80))
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
        self.circle = pygame.transform.scale(circle, (80, 80))
        self.text = pygame.transform.scale(select_text, (150, 30))
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
        screen.blit(self.text, (self.rect.x - 200, self.rect.y))

        return pressed


###########################PLAY PAUSA BUTTON##################
x = int(screen_w/2) - 45
y = screen_h - 100
play_button = Button_play(x, y, play, pause)


###########################SEARCH BUTTON##################
xfolder = 50
yfolder = screen_h - 90
folder_button = Button_folder(xfolder, yfolder, folder)


#####################VISUALIZER TYPE BUTTONS######################
xcircle = screen_w - 200
ycircle = screen_h - 90
circle_button = Button_circle(xcircle, ycircle, circle)

xline = xcircle + 100
yline = screen_h - 90
line_button = Button_line(xline, yline, line)