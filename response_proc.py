#!/usr/bin/env python3

import sys
import csv

inputfile = 'response.csv'


def parse_csv_into_array(csvfile):
    parsedresponses = []

    with open(csvfile) as responses:
        responsereader = csv.reader(responses, delimiter = '|')
        for response in responsereader:
            parsedresponses.append(response)

    return parsedresponses


def main():
    parsedresponses = parse_csv_into_array(inputfile)

    print(parsedresponses)
    print(len(parsedresponses))


if __name__ == '__main__':
    sys.exit(main())

