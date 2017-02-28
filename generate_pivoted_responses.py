#!/usr/bin/env python3

import sys
import csv
import json

inputfile = 'responses.csv'
configfile = 'config.json'
outputfile = 'parsedresponses.csv'


def parse_csv_into_array(csvfile, columndelimiter):
    parsedresponses = []

    with open(csvfile) as responses:
        responsereader = csv.reader(responses, delimiter=columndelimiter)
        for response in responsereader:
            parsedresponses.append(response)

    return parsedresponses


def load_config(configfile):
    config = {}

    with open(configfile) as configs:
        config = json.load(configs)

    return config


def pivot_data(data):
    return nil


def write_output_file(csvfile, data):
    with open(csvfile, 'w') as outputfile:
        responsewriter = csv.writer(outputfile, delimiter='|')
        responsewriter.writerows(data)


def main():
    # Parse possible skills, interests, and availability from json file; in a perfect world
    # we could infer this from the csv, but google forms does not escape commas in responses,
    # and kludges them together, so we have to be explicit on matching options to properly parse.
    config = load_config(configfile)

    # Convert our csv file of responses into a python dict
    parsedresponses = parse_csv_into_array(inputfile, '|')

    # Parse data into a pivottable from the csv data
    for question, responses in config['DataToPivot'].items():
        # The first line at index 0 is our header, and how we determine where the data to pivot is
        questioncolumn = parsedresponses[0].index(question)

        # Look for a match to each known response
        for response in responses:
            # Add the option to the header
            parsedresponses[0].append(response)

            # Parse each individual response
            for line in parsedresponses[1:]:
                # Add response to line with a true flag and strip the response with trailing comma (if there) from text
                if response in line[questioncolumn]:
                    line.append("true")
                    line[questioncolumn] = line[questioncolumn].replace(response, '', 1).replace(", ", '', 1)
                # If not found, still add the response with false to make data consistent number of columns
                else:
                    line.append("false")

        # Need to parse the write in answers now:
        parsedresponses[0].append(question + " - Other")

        for line in parsedresponses[1:]:
            # if line[questioncolumn]
            # print()
            line.append(line[questioncolumn])

    for row in parsedresponses:
        print(len(row))

    write_output_file(outputfile, parsedresponses)


if __name__ == '__main__':
    sys.exit(main())
