"""Analyse enemy fleet and create intel report"""

import argparse


def main(args):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyse enemy fleet and create intel report.')

    parser.add_argument('-i', '--input-path', type=str, dest='input_path',
                        help='Input path where the radar data can be found')
    parser.add_argument('-o', '--output-path', type=str, dest='output_path',
                        help='Output path to which the generated intel report must be saved.')

    main(parser.parse_args())
