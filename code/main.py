import sys
import json
import os.path
import numpy as np
import matplotlib.pyplot as plt
from Simulation import Simulation
from DriverModel import Driver
from Metrics import Metrics
from Car import Params

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def dist(a, b):
    return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def make_filename(f):
    fsplit = f.rsplit(".", 1)
    name = fsplit[0]
    ext = fsplit[1] if len(fsplit) > 1 else ""
    suff = ""
    i = 1
    while os.path.isfile(f'{name}{suff}.{ext}'): suff = i ; i += 1
    return f'{name}{suff}.{ext}'

def save_data(data, filename, overwrite=False):
    print("Saving data, this might take a while...")
    json.dump(data, open(make_filename(filename) if not overwrite else filename, "w"))

def read_data(filename):
    if not os.path.isfile(filename): return None
    else:
        print("Loading data, this might take a while...")
        return json.load(open(filename, "r"))

def dots_to_image(pixel_plot, filename, mode='L', overwrite=False):
    from PIL import Image
    filename = (make_filename(filename) if not overwrite else filename)

    img = Image.fromarray(pixel_plot.astype('uint8'), mode=mode)
    img.save(filename)

def dots_to_image_notSaved(pixel_plot):
    from PIL import Image

    return Image.fromarray(pixel_plot.astype('uint8'), mode='RGB')

def combine_and_Save(img1, img2, filename, overwrite = False):
    from PIL import Image
    filename = (make_filename(filename) if not overwrite else filename)
    img = Image.blend(img1, img2, 0.5)
    new_image = img.resize((int(img.width * 1),int(img.height *0.2) ), resample= Image.BILINEAR)
    new_image.save(filename)

def show_pygame(data, delta_t):
    import pygame
    SPEED = 5 # playback speed of the data (1 for real time)

    SIZE = WIDTH, HEIGHT = 1000, 100
    SCREEN = pygame.display.set_mode(SIZE)

    CLOCK = pygame.time.Clock()

    pygame.init()

    for datapoint in data:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: SPEED += 1
                if event.key == pygame.K_DOWN: SPEED = max(1, SPEED - 1)

        SCREEN.fill(BLACK)

        for car in datapoint:
            car_surface = pygame.Surface((car['length'], 2))
            car_surface.fill(WHITE)
            car_rect = car_surface.get_rect()
            car_rect.center = car['pos']
            SCREEN.blit(car_surface, car_rect)

        pygame.display.update()
        CLOCK.tick(1./delta_t * SPEED)

if __name__ == "__main__":
    road_length = 50000
    delta_t = 0.3

    # With speed limit
    car_params = Params(T=(1.4, 0.3), a=(2, 0.425), b=(2.5, 0.25), delta=4, s_0=2, s_1=0, length=(4.55, 0.175),
                        thr=(0.3, 0.1), pol=(0.25, 0.125), fail_p=1e-6, right_bias=(0.3, 0.1), fail_steps=600,
                        spawn_weight=139829)

    trucc_params = Params(T=(1.6, 0.3), a=(1, 0.1), b=(1.5, 0.25), delta=4, s_0=2, s_1=0, length=(16.5, 1.25),
                        thr=(0.3, 0.1), pol=(0.25, 0.125), fail_p=1e-6, right_bias=(0.3, 0.1), fail_steps=1200,
                        spawn_weight=7886)

    limits = [60, 80, 100, 120, 140, 160, 180][0:1]
    data_list = []
    for l in limits:
        filename=f'speedlimit_{l}.json'
        data = read_data(filename=filename)
        if data is None:
            print(f'Running simulation for speedlimit={l}')
            filename = make_filename(filename)
            car_params.v_0 = (l/3.6, 5)
            trucc_params.v_0 = (min(l, 80)/3.6, 2.5)

            sim = Simulation([car_params, trucc_params], road_length=road_length, car_frequency=2, delta_t=delta_t)
            data = sim.run()
            save_data(data, filename)
        data_list.append(data)

    #show_pygame(data_list[3], delta_t)
    
    #avg = []
    #med = []
    #for data in data_list:
    #    avg.append(np.average(Metrics.avg_speed(data)))
    #r   med.append(np.median(Metrics.median_speed(data)))

    dots = Metrics.make_dots_bw(data, road_length, time_div=1, delta_x=5)
    dots_to_image(dots, "dots_test.png")

    #plt.plot(limits, avg, marker='o')
    #plt.plot(limits, med, marker='o')
    #plt.bar(limits, avg)
    #plt.bar(limits, med)
    #plt.show()
