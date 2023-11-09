
# created using copilot

import csv

def csv2tab(csvfile, tabfile):
    """Convert a CSV file to a tab-delimited file."""
    with open(csvfile, 'r', errors='ignore') as csvin, open(tabfile, 'w', newline="") as tabout:
        csv.writer(tabout, dialect='excel-tab').writerows(csv.reader(csvin))

if __name__ == '__main__':
    import sys
    csv2tab(sys.argv[1], sys.argv[2])