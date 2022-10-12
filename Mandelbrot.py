from os import fpathconf
from matplotlib.backend_bases import MouseButton
import numpy as np
from matplotlib import pyplot as plt
from typing import Tuple

def f(z, c : Tuple[int,int]):
    '''
    Function to calculate the next value in a mandelbrot sequence
    '''
    return z**2 + c

def diverge(c : Tuple[int,int], max_iter):
    '''
    Function to check whether a given coordinate diverges after max_iter iterations of f
    '''
    z = 0
    c = complex(*c)

    for i in range(max_iter):
        if z.real**2 + z.imag**2 >= 4: return i
        z = f(z, c)

    return 0

def make_grid(bbox, res=150):
    '''
    Function to create a coordinate grid and return it as a list of coordinates
    '''
    x_min, x_max, y_min, y_max = bbox

    x, y = np.meshgrid(np.linspace(x_min, x_max, res),np.linspace(y_min, y_max, res))

    return list(zip(x.ravel(), y.ravel()))


def make_mandelbrot(coords, max_iter=20, plot=True):
    '''
    Function to plot mandelbrot coords
    '''
    mandelbrot = np.array([diverge(c, max_iter) for c  in coords])
    res = np.sqrt(np.array(coords).shape[0]).astype(int)
    
    mandelbrot = mandelbrot.reshape(res, res)

    return mandelbrot

def zoom(bbox, focal, factor):
    x, y = focal

    x_min, x_max, y_min, y_max = bbox

    w = (x_max - x_min) / (2 * factor)
    h = (y_max - y_min) / (2 * factor)

    return (x - w, x + w, y - h, y + h)

def onclick(event):
    global bbox, focal_point, zoom_factor, ax
    focal_point = (event.x, event.y)
    bbox = zoom(bbox, focal_point, zoom_factor)
    coords = make_grid(bbox, res=500)
    mb = make_mandelbrot(coords, max_iter=int(50*zoom_factor))
    plt.clf()
    plt.imshow(mb)
    plt.draw() #redraw

bbox = (-2.1, 1, -1.3, 1.3)
focal_point = (-0.749, 0.09)
zoom_factor = 2

# for i in range(16):
#     bbox = zoom(bbox, focal_point, zoom_factor)
#     coords = make_grid(bbox, res=300)
#     mb = make_mandelbrot(coords, max_iter=50 + 1*50)

bbox = zoom(bbox, focal_point, zoom_factor)
coords = make_grid(bbox, res=500)
mb = make_mandelbrot(coords, max_iter=int(50*zoom_factor))

fig, ax = plt.subplots()
ax.imshow(mb)
plt.connect('button_press_event', onclick)
plt.show()

        



