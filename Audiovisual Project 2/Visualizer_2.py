import librosa
import numpy as np
import pygame
from tkinter import Button, Frame, Tk, PhotoImage


def clamp(min_value, max_value, value):

    if value < min_value:
        return min_value

    if value > max_value:
        return max_value

    return value


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


filename = "Pont Aeri - Flying Free.wav"

time_series, sample_rate = librosa.load(filename)  # getting information from the file

# getting a matrix which contains amplitude values according to frequency and time indexes
stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))

spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix

frequencies = librosa.core.fft_frequencies(n_fft=2048*4)  # getting an array of frequencies

# getting an array of time periodic
times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)

time_index_ratio = len(times)/times[len(times) - 1]

frequencies_index_ratio = len(frequencies)/frequencies[len(frequencies)-1]


def get_decibel(target_time, freq):
    return spectrogram[int(freq * frequencies_index_ratio)][int(target_time * time_index_ratio)]


pygame.init()

infoObject = pygame.display.Info()

screen_w = int(infoObject.current_w/2.5)
screen_h = int(infoObject.current_w/2.5)

# Set up the drawing window
screen = pygame.display.set_mode([screen_w, screen_h])


bars = []


low = np.arange(50, 150, 10)
midlo = np.arange(150,300,50)
midhi = np.arange(300, 1000, 100)
mids = np.arange(1000,4000, 500)
high = np.arange(4000,10000, 1000)
ultrahi = np.arange(10000,20000, 10000)
frequencies = np.concatenate([low,midlo,midhi,mids,high,ultrahi])

r = len(frequencies)


width = screen_w/r

x = (screen_w - width*r)/2
y = 50
mheight = 500

for c in frequencies:

    if c >= 1300:
        bars.append(AudioBar(x, y, c, (200, 0, 50), max_height=mheight, width=width))
    if c >= 2600:
        bars.append(AudioBar(x, y, c, (150, 0, 100), max_height=mheight, width=width))
    if c >= 3900:
        bars.append(AudioBar(x, y, c, (100, 0, 150), max_height=mheight, width=width))
    if c >= 5200:
        bars.append(AudioBar(x, y, c, (50, 0, 200), max_height=mheight, width=width))
    if c >= 6500:
        bars.append(AudioBar(x, y, c, (0, 0, 255), max_height=mheight, width=width))
    if c < 1300:
        bars.append(AudioBar(x, y, c, (255, 0, 0), max_height=mheight, width=width))

    x += width

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


    # Fill the background with white
    screen.fill((0, 0, 0))

    for b in bars:
        b.update(deltaTime, get_decibel(pygame.mixer.music.get_pos()/1000.0, b.freq))
        b.render(screen)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
