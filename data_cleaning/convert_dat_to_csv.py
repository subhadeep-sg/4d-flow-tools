import pandas as pd
import numpy as np
import time
import os
from dotenv import load_dotenv
from utils.misc import compute_magnitude


def clean_dat(dat_file):
    # Read the .dat file and extract data
    with open(dat_file, 'r') as file:
        lines = file.readlines()

    # Extract header from "VARIABLES = x, y, z, ..."
    # Should look like ...
    # xcoordinate','ycoordinate','zcoordinate','pressure','velocitymagnitude','xvelocity','yvelocity','zvelocity'

    header = lines[0].replace("VARIABLES =", "").replace('"', "").strip()
    columns = [col.strip() for col in header.split(",")]
    lines = [line for line in lines[2:] if 'ZONE' not in line]

    data = []
    for line in lines:
        temp_list = []
        for num in line.strip().split():
            temp_list.append(float(num))
        data.append(temp_list)

    dataframe = pd.DataFrame(data, columns=columns)
    return dataframe


def noise_check(search_string):
    matches = new_df[new_df.apply(lambda row: row.astype(str).str.contains(search_string, na=False).any(), axis=1)]
    # Display rows that contain the search string
    print(matches)


if __name__ == '__main__':
    st = time.time()
    load_dotenv()
    root_dir = os.getenv('project_root_dir')

    os.makedirs(f'{root_dir}/data', exist_ok=True)
    # Input and output file paths
    input_dat_file = f"{root_dir}/data/081_thrombus_60.dat"
    output_csv_file = f"{root_dir}/data/081_thrombus_60_ver3.csv"

    df = clean_dat(input_dat_file)

    df['vel_mag'] = df.apply(lambda row: float(compute_magnitude(u=row['u'], v=row['v'], w=row['w'])), axis=1)
    df = df.dropna()

    new_df = df[['x', 'y', 'z', 'p', 'vel_mag', 'u', 'v', 'w']]

    new_df.columns = ['xcoordinate', 'ycoordinate', 'zcoordinate',
                      'pressure', 'velocitymagnitude', 'xvelocity',
                      'yvelocity', 'zvelocity']

    new_df.to_csv(output_csv_file, index=False)
    print(new_df)
    print(f"CSV file saved as {output_csv_file}")

    # Check for any missed noisy strings (can be time-consuming)
    noise_check("VARIABLES =")

    print('Runtime:', time.time() - st)
