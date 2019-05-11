import time
import os
import glob

def compare_outputs(out_file):
    
    with open('pa.out', 'r') as f:
        lines = f.read().splitlines()
    
    with open(out_file, 'r') as f:
        lines_ground_truth = f.read().splitlines()
    
    if lines[0] == lines_ground_truth[0]:
        print('\t- Ships correctly identified!')
    else:
        print('\t- Error.')
    if lines[1] == lines_ground_truth[1]:
        print('\t- Advantage time correct!')
    else:
        print('\t- Error. Computed {} | Expected {}'.format(lines[1], lines_ground_truth[1]))

if __name__ == '__main__':
    input_files = sorted(glob.glob('../tests/in/*'))
    output_files = sorted(glob.glob('../tests/out/*'))
    for _in, _out in zip(input_files, output_files):
        start_time = time.time()
        os.system('./executar.sh {} pa.out'.format(_in))
        end_time = time.time() - start_time
        print("{}".format(_in))
        print("\t- Took: {:.3f} seconds".format(end_time))
        compare_outputs(_out)
