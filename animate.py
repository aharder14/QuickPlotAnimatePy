import argparse
import os
from textwrap import dedent
import warnings

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

parser = argparse.ArgumentParser(
    description='Script for making animated line graphs from simple 2D data.')
parser.add_argument(
    'files', nargs='+',
    help='Names of files in directory to parse. File should share a format.')
parser.add_argument(
    '--directory', '-d', default=None,
    help='Relative or absolute path to directory containing data.')

fig_parser = parser.add_argument_group(
    title='Figure Arguments',
    description='Arguments controlling figure settings.')
fig_parser.add_argument(
    '--title', '-t', default=None,
    help='Title of the animated figure.')
fig_parser.add_argument(
    '--size', '-s', default=None, type=float, nargs='*',
    help='Size of the figure to plot.')
fig_parser.add_argument(
    '--ylog', '-y', action='store_true',
    help='Set y axis scale to be logarithmic.')
fig_parser.add_argument(
    '--xlog', '-x', action='store_true',
    help='Set x axis scale to be logarithmic.')

file_parser = parser.add_argument_group(
    title='File and Plot Arguments',
    description=(
        'Arguments controlling individual plot behavior. '
        'Lists should follow same order as files.'
        ))
file_parser.add_argument(
    '--names', '-n', nargs='*', default=None,
    help='Names of columns present in data and labels of x, y axises.')
file_parser.add_argument(
    '--inverse', '-i', action='store_true',
    help='Flip the x and y axis for resulting plots.')
file_parser.add_argument(
    '--header', '-H', type=int, default=None,
    help='Index of the row containing the table names.')
file_parser.add_argument(
    '--separator', '-Sp', default=None,
    help='Separator to use when parsing CSV like files.')
file_parser.add_argument(
    '--labels', '-l', nargs='*', default=[],
    help='Plot label for line produced for each file.')
file_parser.add_argument(
    '--colors', '-c', nargs='*', default=[],
    help='Plot colors for line produced for each file.')
file_parser.add_argument(
    '--markers', '-m', nargs='*', default=[],
    help='Plot markers for line produced for each file.')

output_parser = parser.add_argument_group(
    title='File and Plot Arguments',
    description='Arguments controlling the script output.')
output_parser.add_argument(
    '--save', '-S', default=None,
    help='Path to desired save file.')
output_parser.add_argument(
    '--verbose', '-v', action='store_true',
    help='Print to standard output information on each line.')
output_parser.add_argument(
    '--display', '-D', action='store_true',
    help='Display plot in interactive window.')


animations = []


def data_to_dataframes(
        paths: list[str],
        names: list[str] | None = None,
        header: int | None = None,
        sep: str = r'\s+') -> list[pd.DataFrame]:
    dfs = []
    used_files = []

    for i in paths:
        basename = os.path.basename(i)

        match i.split('.'):
            case _, 'csv' | 'dat':
                df = pd.read_csv(i, index_col=False, header=header, sep=sep)
            case _, 'xls' | 'xlsx':
                df = pd.read_excel(i, index_col=False, header=header)
            case _, t:
                warn = f'Skipping "{basename}": unacceptable type "{t}".'
                warnings.warn(warn)
                continue

        if names:
            df = df.set_axis(names, axis=1)
        
        dfs.append(df.convert_dtypes())
        used_files.append(basename)

    if not dfs:
        raise ValueError('No valid file types provided.')
    
    return dfs, used_files


def update_line(
        num: int,
        x: pd.Series,
        y: pd.Series,
        line: plt.Line2D) -> plt.Line2D:
    line.set_data(x[:num], y[:num])
    return line,


def create_animated_plots(
        fig: plt.Figure,
        ax: plt.Axes,
        frames: int,
        x: pd.Series,
        y: pd.Series,
        **line_args):
    line, = ax.plot(x, y, **line_args)
    ani = animation.FuncAnimation(
        fig,update_line, frames, fargs=(x, y, line))
    animations.append(ani)


def main(
        files: list[str],
        directory: str | None,
        verbose: bool,
        display: bool,
        save: str | None,
        xlog: bool,
        ylog: bool,
        names: list[str],
        header: int,
        separator: str,
        title: str,
        size: str,
        inverse: bool,
        labels: list[str],
        colors: list[str],
        markers: list[str]):
    def null_unpack(**kwargs) -> tuple:
        return {k: v for k, v in kwargs.items() if not v is None}
    
    def safe_list_unpack(l: list, idx: int) -> object:
        try:
            return l[idx]
        except IndexError:
            return None
        
    if directory:
        paths = [os.path.join(directory, i) for i in files]
    else:
        paths = files

    dfs, df_files = data_to_dataframes(
        **null_unpack(
            **dict(
                paths=paths, names=names, header=header, sep=separator)))
    fig, ax = plt.subplots()

    if size:
        fig.set_size_inches(*size)

    frames = max(len(df) for df in dfs) + 1

    if not names:
        names = set.intersection(*[set(df.columns) for df in dfs])

        try:
            x_name, y_name = list(names)[:2]
        except IndexError:
            raise IndexError(
                'Not enough common columns between files to select names.')

    else:
        x_name, y_name, = names
    
    line_args_keys = (
        ('label', labels), ('color', colors), ('marker', markers)
        )

    if inverse:
        x_name, y_name = y_name, x_name

    for i, df in enumerate(dfs):
        x = df[x_name]
        y = df[y_name]
        line_args = {
            k: safe_list_unpack(l, i) for k, l in line_args_keys
            }
        create_animated_plots(
            fig, ax, frames, x, y,
            **null_unpack(**line_args))
        
        if verbose:
            message = dedent(
                f'''---- Figure Number {i} ----
                    File Name: {df_files[i]}
                    Label: {line_args.get('label')}
                    Marker: {line_args.get('marker')}
                    Color: {line_args.get('color')}
                    Data:
                        {df}
                    ---------------------------
                    ''')
            print(message)

    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)

    if title:
        ax.set_title(title)

    if labels:
        fig.legend()

    if ylog:
        ax.set_yscale('log')

    if xlog:
        ax.set_xscale('log')

    if display:
        plt.show()
    

if args := parser.parse_args():
    main(**args.__dict__)    
else:
    quit()