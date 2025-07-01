import numpy as np
import pandas as pd


def generate_dataframe_from_volume(x_coord, y_coord, z_coord, u, v, w):
    new_x, new_y, new_z = [], [], []
    cu, cv, cw = [], [], []

    non_zero_idx = np.nonzero(u)
    for idx0, idx1, idx2, idx3 in zip(*non_zero_idx):
        new_x.append(x_coord[idx1])
        new_y.append(y_coord[idx2])
        new_z.append(z_coord[idx3])
        cu.append(u[idx0][idx1][idx2][idx3])
        cv.append(v[idx0][idx1][idx2][idx3])
        cw.append(w[idx0][idx1][idx2][idx3])

    data_dict = {'x': new_x, 'y': new_y, 'z': new_z, 'cu': cu, 'cv': cv, 'cw': cw}

    return pd.DataFrame(data_dict)


def generate_axis_ranges(dataframe, dist):
    arr = np.arange(dataframe.min(), dataframe.max(), dist)
    dim_list = [[round(arr[i], 3), round(arr[i + 1], 3)] for i in range(len(arr) - 1)]
    dim_list.append([dataframe.min(), dataframe.max()])
    return dim_list


def multi_slices(data_frame, z_range=None, x_range=None, y_range=None):
    """
    Generate slices of the data based on x, y or z-range.
    """
    slices = {}
    if x_range is not None:
        for xr in x_range:
            slice_x = data_frame[(data_frame['x'] >= xr[0]) & (data_frame['x'] <= xr[1])]
            slices[f'X: {xr[0]}-{xr[1]}'] = slice_x

    if y_range is not None:
        for yr in y_range:
            slice_y = data_frame[(data_frame['y'] >= yr[0]) & (data_frame['y'] <= yr[1])]
            slices[f'Y: {yr[0]}-{yr[1]}'] = slice_y

    if z_range is not None:
        for zr in z_range:
            slice_z = data_frame[(data_frame['z'] >= zr[0]) & (data_frame['z'] <= zr[1])]
            slices[f'Z: {zr[0]}-{zr[1]}'] = slice_z

    if z_range is not None and x_range is not None and y_range is not None:
        for xr in x_range:
            for yr in y_range:
                for zr in z_range:
                    slice_z = data_frame.loc[data_frame['z'] >= zr[0]]
                    slice_z = slice_z.loc[slice_z['z'] <= zr[1]]

                    slice_x = slice_z.loc[slice_z['x'] >= xr[0]]
                    slice_x = slice_x.loc[slice_x['x'] <= xr[1]]

                    slice_y = slice_x.loc[slice_x['y'] >= yr[0]]
                    slice_y = slice_y.loc[slice_y['y'] <= yr[1]]

                    slices[f'{xr}{yr}{zr}xyz'] = slice_y

    return slices

