import argparse
import requests
import json
from datetime import datetime

# endpoint used by the official reporters in Romania
data_url = 'https://di5ds1eotmbx1.cloudfront.net/latestData.json'

# The counties that I want to display besides the nation-wide numbers
# TODO: Implement this. After the numbers for nation-wide are displayed nicely
watched_counties = ['BN', 'CJ', 'MM']


# Extracts relevant data (for me) and returns a list of dictionaries
def extract_current_day_data(json_data):
    result = []

    # First, extract nation-wise numbers
    current_day_data = json_data['currentDayStats']
    if not current_day_data['complete']:
        print('Warning: Complete flag for current day is set to false')

    tmp_result = {'days_ago': 0, 'name': 'Romania', 'infected': current_day_data['numberInfected']}
    result.append(tmp_result)

    # Then, extract data for watched counties
    for county in current_day_data['countyInfectionsNumbers']:
        if county in watched_counties:
            tmp_result1 = {'days_ago': 0, 'name': county,
                           'infected': current_day_data['countyInfectionsNumbers'][county]}
            result.append(tmp_result1)

    return result


def fetch_data():
    if args.cached:
        print('Using cached data')
        f = open('latest_data.json')
        json_data = json.load(f)
        f.close()
    else:
        raw_data = requests.get(data_url)
        if raw_data.status_code is not 200:
            print('Error. Endpoint returned status code %s' % raw_data.status_code)
            exit(1)

        json_data = json.loads(raw_data.text)
        # Write the response to a file
        f = open('latest_data.json', 'w')
        json.dump(json_data, f, indent=4)
        f.close()

    return json_data


def main():
    data = fetch_data()

    # Display when the data is from
    time = datetime.fromtimestamp(data['lasUpdatedOn'])
    print('Using data from %s' % time)

    # Obtain the data that I'm interested in
    current_day_data = extract_current_day_data(data)
    print(current_day_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='See the latest data about Covid-19 in Romania')

    parser.add_argument('--cached',
                        required=False,
                        action='store_true',
                        help='Use data cached in ./latest_data.json')

    parser.add_argument('--days',
                        required=False,
                        default=7,
                        type=int,
                        help='How many days should be displayed. Defaults to 7')

    args = parser.parse_args()

    main()


