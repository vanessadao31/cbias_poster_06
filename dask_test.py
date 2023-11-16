"""
Using dask to lazily open multi-dimensional data
"""
import napari
from pathlib import Path
import numpy as np
from timeit import default_timer as timer
from aicsimageio import AICSImage
import argparse

from dask import delayed
import dask.array as da

from timer_functions import read_file, open_napari

parser = argparse.ArgumentParser()
parser.add_argument("folder_pattern", help="folders matching this pattern in the parent directory will be searched")
parser.add_argument("file_pattern", help="files with this pattern will be searched")
parser.add_argument("-r", "--rechunking", help="create 2d chunks", action='store_true')

args = parser.parse_args()

folder_path = Path(args.folder_pattern)  # Data/
rechunking = args.rechunking

# image(s) to be read
# file_pattern = '20191104_ABAT029_REG1-CTRL_DAPI_CD31-ENDOM-680_Th-647_hCD45-33-488_aSMA-CY3_aGFP-594.ome.btf'
file_pattern = args.file_pattern  # Fluo-N3DL-TRIF/01/t*.tif

# for stacking files along time dimension into one timeseries
filenames = []
# print('Reading and sorting file paths...')
for file in folder_path.glob(file_pattern):
    filenames = np.append(filenames, file)
filenames = sorted(filenames)

# reads sample file to obtain file shape
print('Reading first file')
read_time = timer()
sample = AICSImage(filenames[0])   # AICSImage object will always be TCZYX
print(f'Reading first file took {timer() - read_time:.6f} s')

# create dask stack of lazy image readers
print('Creating lazy image readers')
lazy_reader = delayed(read_file)  # lazy reader
lazy_arrays = [lazy_reader(fn) for fn in filenames]

print('Creating dask stack')
dask_time = timer()
dask_arrays = [
    da.from_delayed(delayed_reader,
                    shape=sample.shape[-3:],  # to obtain dimension of one volume
                    dtype=sample.dtype) for delayed_reader in lazy_arrays]

# stack into one large dask.array
stack = da.stack(dask_arrays, axis=0)

# rechunking volumes
if rechunking:
    rechunked = da.rechunk(stack, (1, 1, sample.shape[-2], sample.shape[-1]))
    print(f'Creating dask stack took {timer() - dask_time:.6f} s')
    open_napari(rechunked)
else:
    open_napari(stack)


napari.run()

# # to put into napari ipython terminal:
# with open('csv/t_dask_loading.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile, delimiter=',')
#
#     for iteration in np.arange(10):
#         for i in np.arange(viewer.dims.nsteps[0]):
#             load_time = timer()
#             viewer.dims.set_point(0, i)
#             row = timer() - load_time
#             writer.writerow({row:.6f})


