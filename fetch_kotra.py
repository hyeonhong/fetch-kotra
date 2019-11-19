#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import argparse
import importlib
import json
import csv
from web_scraping import *


def main():
    parser = argparse.ArgumentParser(description='Web Scraper for KOTRA')
    parser.add_argument('--region', type=str, metavar='', help='Scrape the data for the country (REQUIRED)', required=True)
    parser.add_argument('--output', type=str, metavar='', help='Output to CSV or JSON file')
    parser.add_argument('--post', action='store_true', help='Send HTTP POST using JSON')
    parser.add_argument('--url', type=str, metavar='', help='URL for HTTP POST')
    args = parser.parse_args()
    if bool(args.post) ^ bool(args.url):
        parser.error('--post and --url must be given together')

    if args.region is not None:
        country = args.region.title()

    # Build the list of URL addresses for the country passed in
    url_list = build_list(country)
    with open('url_list.txt', 'w') as list_file:
        for url in url_list:
            list_file.write("%s\n" % url)

    # Scrape the contents in the addresses from the url_list and save them in the entry_list
    entry_list = []
    url_list = open('url_list.txt').read().splitlines()
    while url_list:
        url_list = scrape(url_list, entry_list)

    # Write the entry_list to JSON file
    data = {country: entry_list}
    with open('%s.json' % country.upper(), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

    # Process output option
    if args.output is not None:
        output = args.output.lower()
        if output == 'json':
            pass
        elif output == 'csv':

            # Convert JSON file to CSV file
            with open('%s.csv' % country.upper(), 'w', encoding='utf-8', newline='') as csv_file:
                writer = csv.writer(csv_file)

                # Write column header to CSV file
                if entry_list:
                    writer.writerow(entry_list[0].keys())

                # Write the values to CSV file
                for entry in entry_list:
                    writer.writerow(entry.values())
        else:
            print("Error: unrecognized arguments./n"
                  "-- valid arguments: JSON or CSV")
            sys.exit(1)

    # Read the JSON file and print it in the console
    with open('%s.json' % country.upper(), 'r', encoding='utf-8') as read_file:
        parsed = json.load(read_file)
        print(json.dumps(parsed, ensure_ascii=False, indent=4))

    if args.url is not None:
        post_url = args.url.lower()

        # Read JSON file and send HTTP POST request to the designated url
        with open('%s.json' % country.upper(), 'r', encoding='utf-8') as read_file:
            data = json.load(read_file)
        headers = {'Content-type': 'application/json'}
        for item in data[country]:
            try:
                response = requests.post(post_url, data=json.dumps(item, ensure_ascii=False).encode('utf-8'), headers=headers)
            except requests.RequestException as e:
                print(e)
                sys.exit(1)
            if response.status_code != 200:
                print("error occured!")

    print('Web scraping for ' + country + ' is complete.')
    os.remove('url_list.txt')

if __name__ == '__main__':
    main()
