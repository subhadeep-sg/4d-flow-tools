import numpy as np
import cv2
import h5py
import numpy as np
import matplotlib.pyplot as plt
from utils.dat import make_mask, TecPlot


def check_h5_contents(input_path):
    with h5py.File(input_path, mode='r') as hf:
        print(hf.keys())
        # print(np.asarray(hf['dx']))
        # print(np.asarray(hf['u_max']))
        # print(np.asarray(hf['v_max']))
        # print(np.asarray(hf['w_max']))

        # print(np.asarray(hf['venc_v']))
        # print(np.asarray(hf['venc_w']))
        # arr = np.asarray(hf['mask'][0][3])
        # sum_ = np.sum(arr, axis=1).tolist()
        # print(sum_)
        # data_count = len(hf.get("mask"))
        # print('data count: ', data_count)
        for key in hf.keys():
            item = np.asarray(hf[key])
            print(key, 'minimum', item.min())
            print(key, 'maximum', item.max())
            print(f'{key} shape: {item.shape}')


def compare_h5_files(input_path, second_path):
    with h5py.File(input_path, mode='r') as hf:
        u = np.asarray(hf['u'])
        # u = np.pad(u, ((0, 0), (0, 0), (0, 2), (0, 0)), 'constant')

        v = np.asarray(hf['v'])
        # v = np.pad(v, ((0, 0), (0, 0), (0, 2), (0, 0)), 'constant')

        w = np.asarray(hf['w'])
        # w = np.pad(w, ((0, 0), (0, 0), (0, 2), (0, 0)), 'constant')

    with h5py.File(second_path, mode='r') as hf:
        second_u = np.asarray(hf['u'])
        second_v = np.asarray(hf['v'])
        second_w = np.asarray(hf['w'])

    print(u.shape)
    print(second_u.shape)

    print(f'Distance: {np.linalg.norm(u - second_u)}')
    print(f'Distance: {np.linalg.norm(v - second_v)}')
    print(f'Distance: {np.linalg.norm(w - second_w)}')


def generate_h5(dataset, h5_filename, dx):
    final_u, final_v, final_w = dataset.direct_uvw()

    final_u = final_u[:, 1:, :, 1:]
    final_v = final_v[:, 1:, :, 1:]
    final_w = final_w[:, 1:, :, 1:]

    u_max = dataset.u_max
    v_max = dataset.v_max
    w_max = dataset.w_max

    final_avg = np.add(final_u, final_v, final_w) / 3
    mask = make_mask(final_avg)

    with h5py.File(name=h5_filename, mode='w') as f:
        f.create_dataset('u', data=final_u)
        f.create_dataset('v', data=final_v)
        f.create_dataset('w', data=final_w)
        f.create_dataset('dx', data=np.array([dx, dx, dx]))
        f.create_dataset('u_max', data=np.array([u_max]))
        f.create_dataset('v_max', data=np.array([v_max]))
        f.create_dataset('w_max', data=np.array([w_max]))
        f.create_dataset('mask', data=mask)
    print(f'h5 file {h5_filename} written.')


def load_h5_volume(filepath):
    with h5py.File(filepath, mode='r') as file:
        u = np.asarray(file['u'])
        v = np.asarray(file['v'])
        w = np.asarray(file['w'])
    return u, v, w


if __name__ == '__main__':

    check_h5_contents('081_60_HR.h5')

