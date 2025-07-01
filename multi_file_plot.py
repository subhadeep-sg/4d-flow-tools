import pandas as pd
import h5py
import numpy as np
import time
import plotly.express as px
from utils.dat import TecPlot, get_dat
from utils.h5 import load_h5_volume
from utils.volume import generate_dataframe_from_volume, generate_axis_ranges, multi_slices
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
from dotenv import load_dotenv
import os

load_dotenv()
root_dir = os.getenv('project_root_dir')


def plot_multi_files(data_hr, data_lr, x_range, y_range, z_range, selected_dim, dist):
    """
    Generate a dynamic multi-file, multi-subplot interactive 3D scatter plot with color coding.
    Each file has its own set of subplots for slicing.
    """
    num_files = 2
    files_data = {'hr': data_hr, 'lr': data_lr}
    files_names = ['High-Res', 'Low-Res']

    # Create a grid for files, each file will have its own subplots
    fig = make_subplots(
        rows=num_files,
        cols=1,  # One column per file
        specs=[[{"type": "scatter3d"}] for _ in range(num_files)],
        subplot_titles=[f"{files_names[i]}" for i in range(num_files)],
        vertical_spacing=0.2
    )

    for file_idx, (file_name, data_frame) in enumerate(files_data.items()):
        print(file_name)
        # Slice the data for this file
        if selected_dim == 'x':
            data_slices = multi_slices(data_frame=data_frame, x_range=x_range)
        elif selected_dim == 'y':
            data_slices = multi_slices(data_frame=data_frame, y_range=y_range)
        elif selected_dim == 'z':
            data_slices = multi_slices(data_frame=data_frame, z_range=z_range)
        elif selected_dim == 'all':
            data_slices = multi_slices(data_frame=data_frame, z_range=z_range, x_range=x_range, y_range=y_range)

        # Dynamically calculate sub-subplot positions
        num_slices = len(data_slices)
        cols = math.ceil(math.sqrt(num_slices))  # Number of columns per file
        rows = math.ceil(num_slices / cols)  # Number of rows per file

        # Add sub-subplots for each slice
        subplot_positions = [(row, col) for row in range(1, rows + 1) for col in range(1, cols + 1)]
        for slice_idx, (key, slice_df) in enumerate(data_slices.items()):
            if slice_idx >= len(subplot_positions):
                break
            row, col = subplot_positions[slice_idx]

            fig.add_trace(
                go.Scatter3d(
                    x=slice_df["x"],
                    y=slice_df["y"],
                    z=slice_df["z"],
                    mode="markers",
                    marker=dict(
                        size=5,
                        color=slice_df['cu'],  # Color based on 'cu'
                        colorscale='Viridis',  # You can choose other color scales
                        # colorbar=dict(title=f'{cu}')  # Add a colorbar for context
                    ),
                    name=f"{file_name} - {key}"
                ),
                row=file_idx + 1,  # Assign to the main subplot row
                col=1  # Single column for the file
            )

    # Update layout for better readability
    fig.update_layout(
        title="Dynamic 3D Scatter Plots with Slices",
        height=400 * num_files,  # Adjust height for all files
        width=800,
    )

    os.makedirs(f'{root_dir}/plots', exist_ok=True)
    plot_name = f'{root_dir}/plots/{selected_dim}_MULTI_800by400_{dist}_{dx}_{filename}.html'
    plot_name_minus_root = os.path.relpath(plot_name, root_dir)
    fig.write_html(plot_name)
    print(f'Plot written into {plot_name_minus_root}')

    return fig


def volume_plot_pipeline(filename, dx, dist, selected_dim):
    x, y, z, u, v, w = get_dat(f'{root_dir}/data/{filename}.json')
    tec = TecPlot(x, y, z, u, v, w, dx=dx)
    x_coord, y_coord, z_coord = tec.mesh_coords()

    high_res_filepath = f'{root_dir}/data/{filename}_{dx}_HR.h5'
    low_res_filepath = f'{root_dir}/data/{filename}_{dx}_LR.h5'

    u, v, w = load_h5_volume(high_res_filepath)
    lu, lv, lw = load_h5_volume(low_res_filepath)

    # xyz = []

    high_res_dataframe = generate_dataframe_from_volume(x_coord, y_coord, z_coord, u, v, w)
    low_res_dataframe = generate_dataframe_from_volume(x_coord, y_coord, z_coord, lu, lv, lw)

    x_list_ranges = generate_axis_ranges(high_res_dataframe['x'], dist=dist)
    y_list_ranges = generate_axis_ranges(high_res_dataframe['y'], dist=dist)
    z_list_ranges = generate_axis_ranges(high_res_dataframe['z'], dist=dist)

    plot_multi_files(data_hr=high_res_dataframe, data_lr=low_res_dataframe,
                     x_range=x_list_ranges, y_range=y_list_ranges, z_range=z_list_ranges,
                     selected_dim=selected_dim, dist=dist)


if __name__ == '__main__':
    st = time.time()

    dx = 0.05
    filename = '081_thrombus_60'
    distance_separation = 1
    selected_dimension = 'z'

    volume_plot_pipeline(filename=filename, dx=dx,
                         dist=distance_separation, selected_dim=selected_dimension)

    print('Time taken: ', time.time() - st)
