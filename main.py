"""
Name: Daniel Bhatti
Date: 14 October 2024
Description: 

to run test quick: python3 main.py data/MTA_Subway_Stations_20241013.csv
"""

import argparse

def main():
    args = parse_args()
    print(args)


def parse_args():
    """Parse command line arguments (build-graph files)."""
    parser = argparse.ArgumentParser(description='parsing command line arguments')
    parser.add_argument('network_filename', help='path to build-graph file')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()