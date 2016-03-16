#!/usr/bin/python
from bs4 import BeautifulSoup
import requests
import sys
import re
__author__ = 'Daniel Pasacrita'
__date__ = '3/16/16'


def scrape(url, htmlheaders):
    """
    Scrape the eqs page and parse the data.
    :param url: The EQS url.
    :param htmlheaders: HTML headers to use in the request statement.
    :return: soup: The eqs site data.
    """
    r = requests.get(url, headers=htmlheaders)
    # check the status code of the response to make sure the request went well
    if r.status_code != 200:
        print("scrape denied!")
        sys.exit(UNKNOWN)
    else:
        pass
    # Beautiful Soup
    soup = BeautifulSoup(r.text, 'lxml')
    return soup


def data_finder(eqssoup):
    """
    Scrape the eqs page and parse the data.
    :param eqssoup: The EQS soup output.
    :return: nagios: The data that nagios will read.
    """
    # Set Count and Nagios Values - These will hold the values printed back to Nagios
    health = ['Alive', 'Alive', 'Alive', 'Alive']
    time = ['Ready', 'Ready', 'Ready', 'Ready']
    count = 0

    # Find all the matches for "Dead"
    health_matches = re.findall('Dead', eqssoup.text)
    for match in health_matches:
        health[count] = match
        count += 1

    # Reset Count
    count = 0

    # Find all the matches for High time.
    expression = '[1-999999999999999999999999]..\...s'
    time_matches = re.findall(expression, eqssoup.text)
    for match in time_matches:
        time[count] = match
        count += 1
    nagios = [health, time]
    return nagios

if __name__ == "__main__":

    # Declare some constant variables
    # Nagios Exit Codes
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3
    # EQS Values
    eqs_url = 'http://xxx.xxx.xxx.xxx/'
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5)",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
        "accept-encoding": "gzip,deflate,sdch",
        "accept-language": "en-US,en;q=0.8",
    }

    # Run the scrape module. This will grab a kind of readable version of the EQS page
    eqs = scrape(eqs_url, headers)

    # Grab the values from the scrape
    data = data_finder(eqs)

    # Here's a very, very sloppy way to do the check; if ANY are bad, alert.
    check = 0
    for value in data[0]:
        if value != "Alive":
            check = 1
    for value in data[1]:
        if value != "Ready":
            check = 1

    # Now we print out the results! Basically if check = 1, it's bad.
    # If it's still 0, it's good! Either way we print everything.
    if check == 1:
        print("CRITICAL - "+data[0][0]+"/"+data[1][0]+", "+data[0][1]+"/"+data[1][1]+", "+data[0][2]+"/"+data[1][2]+", "+data[0][3]+"/"+data[1][3])
        sys.exit(CRITICAL)
    else:
        print("OK - "+data[0][0]+"/"+data[1][0]+", "+data[0][1]+"/"+data[1][1]+", "+data[0][2]+"/"+data[1][2]+", "+data[0][3]+"/"+data[1][3])
