import numpy as np
from matplotlib import pyplot as plt

def f(z, c : complex):
    '''
    Function to calculate the next value in a mandelbrot sequence
    '''
    return z**2 + c

def diverge(c : complex, max_iter=20):
    '''
    Function to check whether a given coordinate diverges after max_iter iterations of f
    '''
    z = 0.0j
    for i in range(max_iter):
        if z.real**2 + z.imag**2 >= 4: return i
        z = f(z, c)

    return max_iter

def make_mandelbrot(bbox, res=500, max_iter=100):
    '''
    Function to plot mandelbrot coords
    '''
    mb = np.zeros([res, res])
    x_min, x_max, y_min, y_max = bbox

    for row_index, real in enumerate(np.linspace(x_min, x_max, num=res)):
        for col_index, imag in enumerate(np.linspace(y_min, y_max, num=res)):
            mb[row_index, col_index] = diverge(complex(real, imag), max_iter)

    return mb.T

def zoom(bbox, focal, factor):
    '''
    Function to define zoom feature
    '''
    x, y = focal
    x_min, x_max, y_min, y_max = bbox
    w = (x_max - x_min) / (2 * factor)
    h = (y_max - y_min) / (2 * factor)

    return (x - w, x + w, y - h, y + h)

def draw_mandelbrot(mb):
    '''
    Function to update mandelbrot plot
    '''
    plt.clf()
    plt.imshow(mb, cmap='hot', interpolation='bilinear', extent=[*bbox])
    plt.draw()
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.title('Mandelbrot')

def onclick(event):
    '''
    Function to fit bounding box to zoom size
    '''
    global bbox, focal_point, zoom_factor
    zoom_factor *= 2
    print(f"current focal: {focal_point}")
    print(f"current bbox: {bbox}")
    focal_point = (event.xdata, event.ydata)
    new_bbox = zoom(bbox, focal_point, zoom_factor)
    print(f"new focal: {focal_point}")
    print(f"new bbox: {new_bbox}")
    print(f"zoom: {zoom_factor}")
    mb = make_mandelbrot(new_bbox, max_iter=int(100 + 10*zoom_factor))
    draw_mandelbrot(mb)

bbox = (-2.1, 1, -1.3, 1.3)
focal_point = (-0.749, 0.09)
zoom_factor = 1

plt.figure(dpi=100)

mb = make_mandelbrot(bbox)
draw_mandelbrot(mb)
plt.connect('button_press_event', onclick)
plt.show()