import argparse
import os

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

parser = argparse.ArgumentParser(
    description='Utility for making animated line graphs.')
parser.add_argument(
    'path',
    help='Relative or absolute path to folder containing data.')
parser.add_argument(
    '--names', '-n', nargs='+',
    help='Names of columns present in data files.')


def data_to_dataframe(path: str, names: list[str]) -> pd.DataFrame:
    data_files = [i for i in os.listdir(path) if i.endswith('dat')]
    dfs = []

    for i in data_files:
        file_path = os.path.join(path, i)
        alpha = int(
            i
            .split('_')[-1]
            .split('.')[0]
            .replace('alpha', '')
            )
        df = (
            pd
            .read_csv(
                file_path, names=names, index_col=False,
                header=None, sep=r'\s+')
            .convert_dtypes()
            )
        dfs.append((alpha, df))
    
    return dfs


def update_line(
        num: int,
        x: pd.Series,
        y: pd.Series,
        line: plt.Line2D) -> plt.Line2D:
    line.set_data(x[:num], y[:num])
    return line,


if args := parser.parse_args():
    data_dir = args.__dict__['path']
    data_names = args.__dict__['names']
    dfs = data_to_dataframe(data_dir, data_names)
else:
    quit()


fig, ax = plt.subplots()
frames = max(len(df) for _, df in dfs)
animations = []

for alpha, df in dfs:
    x_name, y_name, = data_names
    x = df[x_name]
    y = df[y_name]
    line, = ax.plot(x, y)
    animations.append(
        animation.FuncAnimation(
            fig, update_line, frames, fargs=(x, y, line)))

plt.show()