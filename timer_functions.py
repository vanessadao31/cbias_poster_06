
from timeit import default_timer as timer
import napari
from skimage.io import imread
def timer_func(func):
    def wrapper(*args, **kwargs):
        start = timer()
        result = func(*args, **kwargs)
        end = timer()
        print(f'{func.__name__}() executed in {(end-start):.6f} s')
        # print(f'{(end - start):.6f}')
        return result
    return wrapper

@timer_func
def read_file(filepath):
    image = imread(filepath)
    return image

@timer_func
def open_napari(image):
    viewer = napari.Viewer(ndisplay=2)
    viewer.add_image(image, scale=(1,1,1))
