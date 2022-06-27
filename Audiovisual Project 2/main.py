import colorsys
import random
import tkinter as tk
from tkinter import filedialog

from AudioAnalyzer import *
import Buttons


def rnd_color():
    h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
    return [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]


loading = pygame.image.load("LOADING.png").convert_alpha()

#For play the scene and interactive buttons. It must be executed every time
def buttons_play():

    if Buttons.play_button.draw():
        if Buttons.its_playing:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    global shape_option, running, filename, analyzer

    if Buttons.line_button.draw():
        screen.fill("black")
        pygame.draw.rect(screen, '#272727', pygame.Rect(0, screen_h - 110, screen_w, 110))
        screen.blit(loading, (screen_w / 2 - loading.get_width() / 2, screen_h / 2 - loading.get_height() / 2))
        shape_option = 1
        running = False
        pygame.mixer.music.rewind()

    if Buttons.circle_button.draw():
        screen.fill("black")
        pygame.draw.rect(screen, '#272727', pygame.Rect(0, screen_h - 110, screen_w, 110))
        screen.blit(loading, (screen_w / 2 - loading.get_width() / 2, screen_h / 2 - loading.get_height() / 2))
        shape_option = 2
        pygame.mixer.music.rewind()
        running = False

    if Buttons.folder_button.draw():
        screen.fill("black")
        pygame.draw.rect(screen, '#272727', pygame.Rect(0, screen_h - 110, screen_w, 110))
        screen.blit(loading, (screen_w / 2 - loading.get_width() / 2, screen_h / 2 - loading.get_height() / 2))
        root = tk.Tk()
        root.withdraw()
        pygame.mixer.quit()
        new_filename = filedialog.askopenfilename(title="Select a wav file",filetypes=[('WAV files', '*.wav')])
        if new_filename != '':
            filename = new_filename
        analyzer = AudioAnalyzer()
        analyzer.load(filename)
        pygame.mixer.init()
        pygame.mixer.music.load(filename)

        running = False

    pygame.display.flip()


#Clamp function
def clamp(min_value, max_value, value):

    if value < min_value:
        return min_value

    if value > max_value:
        return max_value

    return value

#Audiobar class
class AudioBar:

    def __init__(self, x, y, freq, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):

        self.x, self.y, self.freq = x, y, freq

        self.color = color

        self.width, self.min_height, self.max_height = width, min_height, max_height

        self.height = min_height

        self.min_decibel, self.max_decibel = min_decibel, max_decibel

        self.__decibel_height_ratio = (self.max_height - self.min_height)/(self.max_decibel - self.min_decibel)

    def update(self, dt, decibel):

        desired_height = decibel * self.__decibel_height_ratio + self.max_height

        speed = (desired_height - self.height)/0.1

        self.height += speed * dt

        self.height = clamp(self.min_height, self.max_height, self.height)

    def render(self, screen):

        pygame.draw.rect(screen, self.color, (self.x, self.y + self.max_height - self.height, self.width, self.height))



###############################GLOBAL AND WINDOW VARIABLES#######################

filename = "Demo_3.wav"
analyzer = AudioAnalyzer()
analyzer.load(filename)


pygame.init()

infoObject = pygame.display.Info()

#Measurements definition
screen_w = 1000
screen_h = 600

# Set up the drawing window
screen = pygame.display.set_mode([screen_w, screen_h])

t = pygame.time.get_ticks()
getTicksLastFrame = t

timeCount = 0

avg_bass = 0
bass_trigger = -30
bass_trigger_started = 0

min_decibel = -80
max_decibel = 80


circle_color = (40, 40, 40)
polygon_default_color = [255, 255, 255]
polygon_bass_color = polygon_default_color.copy()
polygon_color_vel = [0, 0, 0]

shape_option = 1    #line
main_running = True
#########################THE MAIN###################
while main_running:

    ##########################LINE########################################################################
    if(shape_option == 1):

        analyzer = AudioAnalyzer()
        analyzer.load(filename)

        time_series, sample_rate = librosa.load(filename)  # getting information from the file

        # getting a matrix which contains amplitude values according to frequency and time indexes
        stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048 * 4))

        spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix

        frequencies = librosa.core.fft_frequencies(n_fft=2048 * 4)  # getting an array of frequencies

        # getting an array of time periodic
        times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sample_rate, hop_length=512,
                                            n_fft=2048 * 4)

        time_index_ratio = len(times) / times[len(times) - 1]

        frequencies_index_ratio = len(frequencies) / frequencies[len(frequencies) - 1]


        def get_decibel(target_time, freq):
            return spectrogram[int(freq * frequencies_index_ratio)][int(target_time * time_index_ratio)]

        bars = []

        low = np.arange(50, 150, 10)
        midlo = np.arange(150, 250, 25)
        midhi = np.arange(250, 1000, 50)
        mids = np.arange(1000, 4000, 100)
        high = np.arange(4000, 10000, 500)
        ultrahi = np.arange(10000, 20000, 10000)
        frequencies = np.concatenate([low, midlo, midhi, mids, high, ultrahi])

        r = len(frequencies)

        width = screen_w / 2 / r

        x = 150
        y = 50
        mheight = 400

        for c in frequencies:

            if c >= 250:
                bars.append(AudioBar(x, y, c, (64, 224, 208), max_height=mheight, width=width))
            if c >= 1000:
                bars.append(AudioBar(x, y, c, (223, 255, 0), max_height=mheight, width=width))
            if c >= 2500:
                bars.append(AudioBar(x, y, c, (255, 127, 80), max_height=mheight, width=width))
            if c >= 4000:
                bars.append(AudioBar(x, y, c, (222, 49, 99), max_height=mheight, width=width))
            if c < 250:
                bars.append(AudioBar(x, y, c, (100, 149, 237), max_height=mheight, width=width))

            x += 10
            #y += 2 * np.pi + width

        t = pygame.time.get_ticks()
        getTicksLastFrame = t

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(0)


        # Run until the user asks to quit
        running = True

        while running:


            t = pygame.time.get_ticks()
            deltaTime = (t - getTicksLastFrame) / 1000.0
            getTicksLastFrame = t

            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    main_running = False

            # Fill the background with black
            screen.fill((0, 0, 0))


            for b in bars:
                b.update(deltaTime, get_decibel(pygame.mixer.music.get_pos() / 1000.0, b.freq))
                b.render(screen)

            pygame.draw.rect(screen, '#272727', pygame.Rect(0, screen_h - 110, screen_w, 110))

            buttons_play()

    ###########CIRCLE##########################################################################

    if (shape_option == 2):
        analyzer = AudioAnalyzer()
        analyzer.load(filename)

        circle_color = (0, 0, 0)
        polygon_default_color = [255, 255, 255]
        polygon_bass_color = polygon_default_color.copy()
        polygon_color_vel = [0, 0, 0]

        poly = []
        poly_color = polygon_default_color.copy()

        circleX = int(screen_w / 2)
        circleY = int(screen_h / 2  - 50)

        min_radius = 60 #Inner circle
        max_radius = 100
        radius = min_radius
        radius_vel = 0

        # FREQUENCIES
        bass = {"start": 50, "stop": 100, "count": 12}
        heavy_area = {"start": 120, "stop": 250, "count": 40}
        low_mids = {"start": 251, "stop": 2000, "count": 50}
        high_mids = {"start": 2001, "stop": 6000, "count": 20}

        freq_groups = [bass, heavy_area, low_mids, high_mids]

        bars = []

        tmp_bars = []

        length = 0

        for group in freq_groups:

            g = []

            s = group["stop"] - group["start"]

            count = group["count"]

            reminder = s % count

            step = int(s / count)

            rng = group["start"]

            for i in range(count):

                arr = None

                if reminder > 0:
                    reminder -= 1
                    arr = np.arange(start=rng, stop=rng + step + 2)
                    rng += step + 3
                else:
                    arr = np.arange(start=rng, stop=rng + step + 1)
                    rng += step + 2

                g.append(arr)

                length += 1

            tmp_bars.append(g)

        angle_dt = 340 / length

        ang = 0

        for g in tmp_bars:
            gr = []
            for c in g:
                gr.append(
                    RotatedAverageAudioBar(circleX + radius * math.cos(math.radians(ang - 90)),
                                           circleY + radius * math.sin(math.radians(ang - 90)), c, (255, 0, 255),
                                           angle=ang,
                                           width=8, max_height=180)) ## TOCAT
                ang += angle_dt

            bars.append(gr)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(0)

        running = True
        while running:

            avg_bass = 0
            poly = []

            t = pygame.time.get_ticks()
            deltaTime = (t - getTicksLastFrame) / 1000.0
            getTicksLastFrame = t

            timeCount += deltaTime

            screen.fill(circle_color)


            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    main_running = False

            for b1 in bars:
                for b in b1:
                    b.update_all(deltaTime, pygame.mixer.music.get_pos() / 1000.0, analyzer)

            for b in bars[0]:
                avg_bass += b.avg

            avg_bass /= len(bars[0])

            if avg_bass > bass_trigger:
                if bass_trigger_started == 0:
                    bass_trigger_started = pygame.time.get_ticks()
                if (pygame.time.get_ticks() - bass_trigger_started) / 1000.0 > 2:
                    polygon_bass_color = rnd_color()
                    bass_trigger_started = 0
                if polygon_bass_color is None:
                    polygon_bass_color = rnd_color()
                newr = min_radius + int(
                    avg_bass * ((max_radius - min_radius) / (max_decibel - min_decibel)) + (max_radius - min_radius))
                radius_vel = (newr - radius) / 0.15

                polygon_color_vel = [(polygon_bass_color[x] - poly_color[x]) / 0.15 for x in range(len(poly_color))]

            elif radius > min_radius:
                bass_trigger_started = 0
                polygon_bass_color = None
                radius_vel = (min_radius - radius) / 0.15
                polygon_color_vel = [(polygon_default_color[x] - poly_color[x]) / 0.15 for x in range(len(poly_color))]

            else:
                bass_trigger_started = 0
                poly_color = polygon_default_color.copy()
                polygon_bass_color = None
                polygon_color_vel = [0, 0, 0]

                radius_vel = 0
                radius = min_radius

            radius += radius_vel * deltaTime

            for x in range(len(polygon_color_vel)):
                value = polygon_color_vel[x] * deltaTime + poly_color[x]

                #Cast value in between range 0-255
                value = max(0, value)
                value = min(value, 255)
                poly_color[x] = value

            for b1 in bars:
                for b in b1:
                    b.x, b.y = circleX + radius * math.cos(math.radians(b.angle - 90)), circleY + radius * math.sin(
                        math.radians(b.angle - 90))
                    b.update_rect()

                    poly.append(b.rect.points[3])
                    poly.append(b.rect.points[2])

            pygame.draw.polygon(screen, poly_color, poly)
            pygame.draw.circle(screen, circle_color, (circleX, circleY), int(radius))

            pygame.draw.rect(screen, '#272727', pygame.Rect(0, screen_h - 110, screen_w, 110))

            buttons_play()


pygame.quit()