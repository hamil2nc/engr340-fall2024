import sys


def sliding_window(datas):

    windowWidth = 6

    # I looked this up because I figured there was a more "pythonny" way to find the sum of a list than
    # doing some sort of total = 0, total += data[3] in a for loop
    # https://stackoverflow.com/questions/638048/how-do-i-sum-the-first-value-in-each-tuple-in-a-list-of-tuples-in-python#638055
    windowSum = sum(data[3] for data in datas[:windowWidth])
    maxWindowSum = windowSum

    # After getting the initial windowSum, start the sliding window by
    # subtracting the element leaving the window and adding the element entering the window
    # avoiding a nested loop
    for i in range(windowWidth, len(datas) - windowWidth):

        # The range based for loop is inclusive so I am starting at the windowWidth element, which has already
        # been accounted for in the initial windowSum, so I have to subtract it
        windowSum -= datas[i][3]

        # Then add the new element that is exactly one width away from the one we just subtracted
        windowSum += datas[i + windowWidth][3]

        # If the current window is the biggest we've seen, store the starting data and value
        if windowSum > maxWindowSum:
            maxWindowSum = windowSum

            # The start of the window is i + i because we are removing the i'th element from the window
            # in the previous step
            windowStartDate = datas[i + 1][0]

    return maxWindowSum, windowStartDate


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


def first_question(harrisonburgData, rockinghamData):
    """
    # Write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    :return:
    """

    # Because it is already sorted in ascending data, the first positive case
    # for each will be the 0th element of the first tuple

    print(f"First Harrisonburg positive case: {harrisonburgData[0][0]}")
    print(f"First Rockingham County positive case: {rockinghamData[0][0]}")

    # your code here
    return


def second_question(harrisonburgData, rockinghamData):
    """
    # Write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    :return:
    """

    maxHarrisonburgCases = 0
    maxRockinghamCases = 0


    for info in harrisonburgData:
        if info[3] > maxHarrisonburgCases:
            maxHarrisonburgCases = info[3]
            maxHarrisonburgCasesDate = info[0]

    for info in rockinghamData:
        if info[3] > maxRockinghamCases:
            maxRockinghamCases = info[3]
            maxRockinghamCasesDate = info[0]

    print(f"\nHarrisonburg: Max daily cases was {maxHarrisonburgCases} on {maxHarrisonburgCasesDate}")
    print(f"Rockingham County: Max daily cases was {maxRockinghamCases} on {maxRockinghamCasesDate}\n")

    # your code here
    return


def third_question(harrisonburgData, rockinghamData):
    # Write code to address the following question:Use print() to display your responses.
    # What was the worst 7-day period in either the city and county for new COVID cases?
    # This is the 7-day period where the number of new cases was maximal.

    harrisonburgMaxWindow, harrisonburgWindowStart = sliding_window(harrisonburgData)
    rockinghamMaxWindow, rockinghamWindowStart = sliding_window(rockinghamData)

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

    data = parse_nyt_data('us-counties.csv')

    harrisonburgData = []
    rockinghamData = []

    for info in data:
        if (info[1] == "Harrisonburg city" and info[2] == "Virginia"):
            harrisonburgData.append(info)
        if (info[1] == "Rockingham" and info[2] == "Virginia"):
            rockinghamData.append(info)

    # write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    first_question(harrisonburgData, rockinghamData)

    # write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    second_question(harrisonburgData, rockinghamData)

    # write code to address the following question:Use print() to display your responses.
    # What was the worst seven day period in either the city and county for new COVID cases?
    # This is the 7-day period where the number of new cases was maximal.
    third_question(harrisonburgData, rockinghamData)
