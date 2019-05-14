import os
import glob
import sys

import numpy as np
import pandas as pd

if __name__ == '__main__':
    input_files = sorted(glob.glob('in/*'))
    rows = []
    header = ['exp', 'size', 'mean_time', 'std_time',  'mean_memory', 'std_memory']
    for i, _in in enumerate(input_files):
        print(_in)
        times = []
        memories = []
        row = []
        f = _in.split('/')[-1]
        if len(f.split('-')) > 2:
            row.append(f.split('-')[0])
            row.append(f.split('-')[1].split('_')[0])
        else:
            row.append(f.split('-')[0].split('_')[1])
            row.append(f.split('-')[0].split('_')[0])
        for x in range(10):
            os.system('./executar.sh {} o.out'.format(_in))
            with open('o.out', 'r') as f:
                times.append(float(f.readline()))
                memories.append(float(f.readline()))
        
        times = np.array(times)    
        memories = np.array(memories)

        row.append(times.mean())
        row.append(times.std())

        row.append(memories.mean())
        row.append(memories.std())
        rows.append(row)
        print(f"{i + 1} of {len(input_files)} completed.")
    
    df = pd.DataFrame(data=rows, columns=header)
    df.to_csv('stats.csv', index=False)