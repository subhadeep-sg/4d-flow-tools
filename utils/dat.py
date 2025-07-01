import json
import numpy as np


def create_mesh(nx, ny, nz, xlim, ylim, zlim, dx, filename):
    meshes = []
    for a in range(nx):
        xlim += dx
        for b in range(ny):
            ylim += dx
            for c in range(nz):
                zlim += dx
                meshes.append([a, xlim, b, ylim, c, zlim])
    with open(filename, "w") as fp:
        json.dump(meshes, fp)
    print(f'meshes stored in mesh_list.json...')


def get_mesh(filename):
    with open(filename, 'r') as fp:
        return json.load(fp)


def dataloop(xl, yl, zl, sum_of_mesh, x, y, z, u, v, w):
    """
    # meshes = get_mesh('mesh_list.json')

    # for mesh in meshes:
    #     sum_of_mesh = np.zeros((1, 3))
    #     a, xlim, b, ylim, c, zlim = mesh
    #     avg_mesh, x, y, z, u, v, w = dataloop(xlim, ylim, zlim, sum_of_mesh, x, y, z, u, v, w)
    #     final_u[0][a][b][c] = avg_mesh[0]
    #     final_v[0][a][b][c] = avg_mesh[1]
    #     final_w[0][a][b][c] = avg_mesh[2]
    #     print(avg_mesh)
    #     print('mesh done')
    """
    data_length = len(x)
    flag = 0
    num_points = 0
    epsilon = 1e-100            # A small value to avoid division by zero
    for idx in range(data_length):
        if flag == 1:
            idx -= 1
            flag = 0
        if idx >= len(x):
            # Exiting loop if the list of x, y and z has been covered
            return sum_of_mesh/(num_points + epsilon), x, y, z, u, v, w
        if x[idx] < xl and y[idx] < yl and z[idx] < zl:
            flag = 1
            vect = np.array([u[idx], v[idx], w[idx]])
            sum_of_mesh = np.add(sum_of_mesh, vect)
            num_points += 1
            x.pop(idx)
            y.pop(idx)
            z.pop(idx)
            u.pop(idx)
            v.pop(idx)
            w.pop(idx)
    return sum_of_mesh/(num_points + epsilon), x, y, z, u, v, w


def read_dat(filename, save_to_local=False):
    file = open(filename, "r")
    lines = file.readlines()
    x, y, z, u, v, w, p = [], [], [], [], [], [], []
    for line in lines:
        if 'VARIABLES' in line:
            print(line)
            pass
        elif 'ZONE' in line:
            pass
        else:
            sentence = line.split(' ')
            sentence[-1] = sentence[-1][:-1]
            # sentence = [float(num) for num in sentence]
            x.append(float(sentence[0]))
            y.append(float(sentence[1]))
            z.append(float(sentence[2]))
            u.append(float(sentence[3]))
            v.append(float(sentence[4]))
            w.append(float(sentence[5]))
    file.close()

    if save_to_local:
        new_file = filename.replace(".dat", ".json")
        with open(new_file, 'w') as fp:
            json.dump((x, y, z, u, v, w), fp)
        print(f'Contents of .dat file moved to {new_file}')
    return x, y, z, u, v, w


def get_dat(filename):
    with open(filename, 'r') as fp:
        return json.load(fp)


def make_mask(arr):
    arr[arr != 0.0] = 1
    return arr


class TecPlot:
    def __init__(self, x, y, z, u, v, w, dx):
        self.x = x
        self.y = y
        self.z = z
        self.u = u
        self.v = v
        self.w = w
        self.dx = dx
        self.x_max, self.x_min = max(x), min(x)
        self.y_max, self.y_min = max(y), min(y)
        self.z_max, self.z_min = max(z), min(z)
        self.u_max, self.u_min = max(u), min(u)
        self.v_max, self.v_min = max(v), min(v)
        self.w_max, self.w_min = max(w), min(w)

    def mesh_coords(self):
        arr_x = np.arange(start=self.x_min, stop=self.x_max, step=self.dx)
        arr_y = np.arange(start=self.y_min, stop=self.y_max, step=self.dx)
        arr_z = np.arange(start=self.z_min, stop=self.z_max, step=self.dx)
        return arr_x, arr_y, arr_z

    def direct_uvw(self):
        n = len(self.x)
        xarr, yarr, zarr = self.mesh_coords()
        epsilon = 1e-100
        final_u = final_v = final_w = np.zeros((1, len(xarr), len(yarr), len(zarr)))

        ctrs = np.zeros((1, len(xarr), len(yarr), len(zarr))) + epsilon
        for idx in range(n):
            ix = np.argmin(np.abs(xarr - self.x[idx]))           # np.searchsorted(xarr, x[idx])
            iy = np.argmin(np.abs(yarr - self.y[idx]))           # np.searchsorted(yarr, y[idx])
            iz = np.argmin(np.abs(zarr - self.z[idx]))           # np.searchsorted(zarr, z[idx])

            final_u[0][ix][iy][iz] += self.u[idx]
            final_v[0][ix][iy][iz] += self.v[idx]
            final_w[0][ix][iy][iz] += self.w[idx]
            ctrs[0][ix][iy][iz] += 1

        final_u = np.divide(final_u, ctrs)
        final_v = np.divide(final_v, ctrs)
        final_w = np.divide(final_w, ctrs)

        return final_u, final_v, final_w



