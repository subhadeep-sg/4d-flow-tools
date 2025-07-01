import numpy as np
import h5py
import time
from utils.dat import get_dat, TecPlot, make_mask, read_dat
from utils.h5 import generate_h5
from dotenv import load_dotenv
import os

"""
Zones are irrelevant to the problem statement and so they are removed.
"""

if __name__ == '__main__':
    st = time.time()

    load_dotenv()
    root_dir = os.getenv('project_root_dir')

    assert os.path.exists(os.path.join(root_dir, 'data')), "data directory doesn't exist"

    # Convert .dat to .json format
    # x, y, z, u, v, w = read_dat('{root_dir}/data/081_thrombus_60.dat', save_to_local=True)

    # Extracting all dimensions of mesh form .json file
    x, y, z, u, v, w = get_dat(f'{root_dir}/data/081_thrombus_60.json')

    # Mesh resolution (smaller the finer)
    dx = 0.05

    # Generating TecPlot with specified resolution dx
    dataset = TecPlot(x, y, z, u, v, w, dx=dx)

    filename = f'{root_dir}/data/081_thrombus_60_{dx}_HR.h5'

    generate_h5(dataset, h5_filename=filename, dx=dx)

    print('Reading h5 file..')
    with h5py.File(name=filename, mode='r') as f:
        print(f.keys())
        for key in f.keys():
            item = np.asarray(f[key])
            print(f'{key} shape: {item.shape}')

    print('Runtime: ', time.time() - st)
