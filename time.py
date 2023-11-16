
from pathlib import Path
import napari
import argparse

from timer_functions import read_file, open_napari

parser = argparse.ArgumentParser()
parser.add_argument("folder_pattern", help="folders matching this pattern in the parent directory will be searched")
parser.add_argument("file_pattern", help="files with this pattern will be searched")
args = parser.parse_args()

folder_path = Path(args.folder_pattern)  # Data/Fluo-N3DL-TRIF/01

# image(s) to be read
# file_pattern = 'Data/20191104_ABAT029_REG1-CTRL_DAPI_CD31-ENDOM-680_Th-647_hCD45-33-488_aSMA-CY3_aGFP-594.ome.btf'
file_pattern = args.file_pattern  # t*.tif

# time to load image into a numpy array using aicsimageio
image = read_file(file_pattern)

# time to load numpy array into napari
open_napari(image)

napari.run()

# # to put into napari ipython terminal:
# with open('csv/t_ram_loading.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile, delimiter=',')
#
#     for iteration in np.arange(10)
#         for i in np.arange(viewer.sims.nsteps[0]):
#             load_time = timer()
#             viewer.dims.set_point(0, i)
#             row = timer() - load_time
#             writer.writerow({row:.6f})








