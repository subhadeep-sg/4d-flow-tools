# 4DFlow Data Processing and Visualization

Preprocessing utilities for adapting 4DFlowNet to work with TecPlot .dat files instead of the original.h5/DICOM format

---

## Workflow Overview

1. **Convert raw TecPlot DAT files**  
   - Use `data_cleaning/convert_dat_to_csv.py` to clean `.dat` files and output standardized CSVs.  
   - Alternatively, skip CSV if using HDF5 pipeline directly.

2. **Generate volumetric data**  
   - Use `data_cleaning/extract_dat.py` to convert cleaned JSON data into regular grids in HDF5 format.

3. **Visualize results**  
   - Run `multi_file_plot.py` to create interactive 3D scatter plots comparing high-res (HR) and low-res (LR) data across x, y, or z slices.

4. **Explore outputs**  
   - Open generated HTML files in `plots/` for interactive inspection.

---

## Key Components

### Scripts

- **multi_file_plot.py**
  - Purpose: Interactive 3D visualization comparing HR/LR volumetric flow data.
  - Key Functions:
    - `plot_multi_files()`: Generates side-by-side 3D scatter plots with slicing.
    - `volume_plot_pipeline()`: Full workflow from data files to visualization.

- **data_cleaning/convert_dat_to_csv.py**
  - Purpose: Converts TecPlot `.dat` files to cleaned CSV format.
  - Key Functions:
    - `clean_dat()`: Parses raw DAT files into DataFrames.
    - `compute_magnitude()`: Calculates velocity magnitude from u, v, w components.
    - `noise_check()`: Identifies parsing artifacts.

- **data_cleaning/extract_dat.py**
  - Purpose: Converts cleaned JSON data into regular volumetric grids saved as HDF5.
  - Key Steps:
    1. Convert DAT → JSON
    2. Load velocity data from JSON
    3. Generate TecPlot dataset with specified resolution (dx)
    4. Write grids and metadata to HDF5

---

### utils/ modules

- **utils/volume.py**
  - `generate_dataframe_from_volume()`: Converts 4D velocity arrays to DataFrame (filters non-zero points).
  - `generate_axis_ranges()`: Creates coordinate slicing ranges.
  - `multi_slices()`: Generates slices along specified x/y/z ranges.

- **utils/h5.py**
  - `generate_h5()`: Creates HDF5 volumes from TecPlot datasets with binary masks.
  - `load_h5_volume()`: Loads velocity components from existing HDF5 files.
  - `check_h5_contents()`: Debug utility to inspect HDF5 file structures.
  - `compare_h5_files()`: Compares two HDF5 datasets.

- **utils/dat.py**
  - `TecPlot` class: Converts scattered velocity data into regular grids.
    - `mesh_coords()`: Creates x/y/z arrays for the grid.
    - `direct_uvw()`: Maps scattered points to nearest grid cells.
  - `read_dat()`: Parses TecPlot DAT files → saves as JSON.
  - `get_dat()`: Loads JSON velocity data.
  - `make_mask()`: Generates binary masks from velocity magnitudes.

- **utils/misc.py**
  - `factors()`: Computes factors of a number (general-purpose utility).

---

## Requirements

- Dependencies listed in `requirements.txt`

Install with:
```bash
pip install -r requirements.txt
```