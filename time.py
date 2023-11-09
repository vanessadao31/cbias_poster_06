
from pathlib import Path
import napari
import argparse

from timer_functions import read_file, open_napari

parser = argparse.ArgumentParser()
parser.add_argument("folder_pattern", help="folders matching this pattern in the parent directory will be searched")
args = parser.parse_args()

folder_path = Path(args.folder_pattern)  # Data/

# image(s) to be read
# filepath = 'Data/20191104_ABAT029_REG1-CTRL_DAPI_CD31-ENDOM-680_Th-647_hCD45-33-488_aSMA-CY3_aGFP-594.ome.btf'
filepath = 'Data/20191104_ABAT029_REG1-CTRL_REG2-80ENGR_DAPI_CD31-ENDOM-680_Th-647_hCD45-33-488_aSMA-CY3_aGFP-594.ome.btf'

# time to load image into a numpy array using aicsimageio
image = read_file(filepath)

# time to load numpy array into napari
open_napari(image)

napari.run()

# # to put into napari ipython terminal:
# with open('channels_ram_loading.csv', 'a', newline='') as csvfile:
#     writer = csv.writer(csvfile, delimiter=',')
#
#     for iteration in np.arange(10)
#         for i in np.arange(6):
#             load_time = timer()
#             viewer.dims.set_point(0, i)
#             row = timer() - load_time
#             writer.writerow(f'{row:.6f}')








