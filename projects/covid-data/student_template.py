import sys
import pandas as pd


def sliding_window(datas):

    # Define the width of the window (6 because it is a 7-day period)
    WINDOW_WIDTH = 6

    # Get the total for the first WINDOW_WIDTH elements to start the sliding window off
    windowSum = sum(data[0] for data in datas[:WINDOW_WIDTH])

    # Set initial conditions so the function doesn't throw an error in the case that the max window size
    # is the first WINDOW_WIDTH days
    maxWindowSum = windowSum
    windowStartDate = datas[0][1]

    # After getting the initial windowSum, start the sliding window by
    # subtracting the element leaving the window and adding the element entering the window
    # avoiding a nested loop
    for i in range(1, len(datas) - WINDOW_WIDTH):

        # The range based for loop is inclusive so I am starting at the WINDOW_WIDTH element, which has already
        # been accounted for in the initial windowSum, so I have to subtract it
        windowSum -= datas[i - 1][0]

        # Then add the new element that is exactly one width away from the one we just subtracted
        windowSum += datas[i + WINDOW_WIDTH][0]

        # If the current window is the biggest we've seen, store the starting data and value
        if windowSum > maxWindowSum:
            maxWindowSum = windowSum

            # The start of the window is i + i because we are removing the i'th element from the window
            # in the previous step
            windowStartDate = datas[i][1]

    return maxWindowSum, windowStartDate


def get_diff(datas):
    diff_data = []

    for i in range(1, len(datas)):
        diff = datas[i][4] - datas[i - 1][4]
        tuple = (diff, datas[i][0])
        diff_data.append(tuple)

    return diff_data

def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date, county, state, cases, deaths) information
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data


def first_question(harrisonburg_df, rockingham_df):
    """
    # Write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    :return:
    """

    # Because it is already sorted in ascending data, the first positive case
    # for each will be the 0th element of the first tuple
    print(f"\nHarrisonburg: First positive case was on {harrisonburg_data[0][0]}")
    print(f"Rockingham County: First positive case was on {rockingham_data[0][0]}")

    # your code here
    return


def second_question(harrisonburg_diff, rockingham_diff):
    """
    # Write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    :return:
    """


    # set Initial conditions so I can compare in the following for loop
    maxHarrisonburgCases = 0
    maxRockinghamCases = 0


    # Compare the number of daily cases for each day in both data sets
    for data in harrisonburg_diff:

        # and if the daily cases is a new max, then reassign the maxCases and grab the date as well
        if data[0] > maxHarrisonburgCases:
            maxHarrisonburgCases = data[0]
            maxHarrisonburgCasesDate = data[1]

    # Repeat for Rockingham County data
    for data in rockingham_diff:
        if data[0] > maxRockinghamCases:
            maxRockinghamCases = data[0]
            maxRockinghamCasesDate = data[1]



    print(f"\nHarrisonburg: Max daily cases was {maxHarrisonburgCases} on {maxHarrisonburgCasesDate}")
    print(f"Rockingham County: Max daily cases was {maxRockinghamCases} on {maxRockinghamCasesDate}\n")

    # your code here
    return


def third_question(harrisonburgData, rockinghamData):
    # Write code to address the following question:Use print() to display your responses.
    # What was the worst 7-day period in either the city and county for new COVID cases?
    # This is the 7-day period where the number of new cases was maximal.

    # Call the sliding_window function to get the max 7-day period for Harrisonburg and Rockingham County
    harrisonburgMaxWindow, harrisonburgWindowStart = sliding_window(harrisonburgData)
    rockinghamMaxWindow, rockinghamWindowStart = sliding_window(rockinghamData)

    # Compare the outputs of the sliding_window function to know which area had a worse 7-day period
    if harrisonburgMaxWindow > rockinghamMaxWindow:
        maxWindow = harrisonburgMaxWindow
        windowStart = harrisonburgWindowStart
        location = "Harrisonburg"
    else:
        maxWindow = rockinghamMaxWindow
        windowStart = rockinghamWindowStart
        location = "Rockingham County"


    print(f"Worst seven day period was in {location}, beginning on {windowStart}, and had {maxWindow} new cases.")
    return


if __name__ == "__main__":

    # data = parse_nyt_data('us-counties.csv')

    # Create lists to contain just the Harrisonburg Data and just the Rockingham County Data
    filePath = 'us-counties.csv'
    df = pd.read_csv(filePath, header=0)
    harrisonburg_data = df[(df['county'] == 'Harrisonburg city') & (df['state'] == 'Virginia')].to_numpy()
    rockingham_data = df[(df['county'] == 'Rockingham') & (df['state'] == 'Virginia')].to_numpy()

    # Check the City/County AND the State column to make sure it is what we are looking for
    # and the add that tuple to its respective list
    # I am doing this in main to avoid having to parse through the entire data set for each question
    # and I changed the parameters for each function to accept the Harrisonburg and Rockingham County lists


    # write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    first_question(harrisonburg_data, rockingham_data)

    # write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    harrisonburg_diff = get_diff(harrisonburg_data)
    rockingham_diff = get_diff(rockingham_data)

    second_question(harrisonburg_diff, rockingham_diff)

    # write code to address the following question:Use print() to display your responses.
    # What was the worst seven-day period in either the city and county for new COVID cases?
    # This is the 7-day period where the number of new cases was maximal.
    third_question(harrisonburg_diff, rockingham_diff)
