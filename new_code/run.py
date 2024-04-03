import csv
import argparse
from pathlib import Path


# ROOT = Path().absolute()
# PATH = ROOT / "datasets/"


parser = argparse.ArgumentParser()
parser.add_argument("file", help="enter the file name")
args = parser.parse_args()


with open(args.file) as f:
    d_header = csv.DictReader(f)
    print(d_header)
