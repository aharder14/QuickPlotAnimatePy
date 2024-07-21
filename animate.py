import argparse
import os

import pandas as pd
import matplotlib.pyplot as plt

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
            .assign(alpha=alpha)
            .convert_dtypes()
            )
        dfs.append(df)
    
    df = pd.concat(dfs, ignore_index=True)
    return df


if args := parser.parse_args():
    df = data_to_dataframe(**args.__dict__)
    print(df)