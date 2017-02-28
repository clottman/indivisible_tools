#!/usr/bin/env python3

import sys
import csv
import json
import logging

inputfile = 'responses.csv'
configfile = 'config.json'
outputfile = 'parsedresponses.csv'
log_level = logging.DEBUG


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


def write_output_file(csvfile, data, columndelimiter):
    with open(csvfile, 'w') as outputfile:
        responsewriter = csv.writer(outputfile, delimiter=columndelimiter)
        responsewriter.writerows(data)


def main():
    logging.basicConfig(stream=sys.stderr, level=log_level)

    # Parse possible skills, interests, and availability from json file; in a perfect world
    # we could infer this from the csv, but google forms does not escape commas in responses,
    # and kludges them together, so we have to be explicit on matching options to properly parse.
    logging.debug('Loading questions and responses config to pivot from %s' % configfile)
    config = load_config(configfile)

    logging.debug('Parsing responses in %s csv into array' % inputfile)
    parsedresponses = parse_csv_into_array(inputfile, '|')

    logging.debug('Starting to parse questions and responses from the DataToPivot key in %s' % configfile)
    for question, responses in config['DataToPivot'].items():

        logging.debug('Attempting to find the column of the question: "%s"' % question)
        questioncolumn = parsedresponses[0].index(question)

        logging.debug('Looping through responses in config to match each line')
        for response in responses:
            logging.debug('Adding the response option: "%s" to the header row' % response)
            parsedresponses[0].append(response)

            logging.debug('Looping through each individual response (ignoring the header row)')
            for line in parsedresponses[1:]:
                if response in line[questioncolumn]:
                    logging.debug('Found a match for %s in row %s for user %s %s' % (response, parsedresponses.index(line), line[1], line[2]))
                    line.append("true")

                    # Strips out the first instance of the response, then the first comma followed by space found
                    # This allows us to find all the "Other" answers at the end of the response string
                    line[questioncolumn] = line[questioncolumn].replace(response, '', 1).replace(", ", '', 1)
                else:
                    logging.debug('Did not find a match for %s in row %s for user %s %s' % (response, parsedresponses.index(line), line[1], line[2]))
                    line.append("false")

        logging.debug('Adding "%s - Other" header into header row' % question)
        parsedresponses[0].append(question + " - Other")

        for line in parsedresponses[1:]:
            logging.debug('Parsing "%s" write in answer into column "%s - Other" in row %s for user %s %s' % (line[questioncolumn], question, parsedresponses.index(line), line[1], line[2]))
            line.append(line[questioncolumn])

    for row in parsedresponses:
        logging.debug('Row %s has %s columns' % (parsedresponses.index(row), len(row)))

    logging.debug('Writing output file %s' % outputfile)
    write_output_file(outputfile, parsedresponses, '|')

    logging.debug('Success! Input file %s was parsed using config %s and %s has been generated!' % (inputfile, configfile, outputfile))


if __name__ == '__main__':
    sys.exit(main())
