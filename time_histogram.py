#!/usr/bin/env python3
"""
This function will get the time stamps for a users commits and create a
histogram to see what time of day they are typically working.
"""
import json
import matplotlib.pyplot as plt
from datetime import datetime
import pytz


def what_times(file):
    """
    Args:
        file (str): file name to extract information from
    """
    commit_dates, commit_lists, commit_hours = [], [], []
    with open(file) as f:
        data = json.load(f)

    commit_data_per_repo = data.get("commit_data_per_repo", {})

    # Get all of the commit messages
    for _, repo_data in commit_data_per_repo.items():
        commit_messages = repo_data.get("commit_messages", 0)
        commit_lists.append(commit_messages)

    # Create a list of all of the timestamps
    for commit_message in commit_lists:
        for commit in commit_message:
            commit_dates.append(commit.get('date'))

    # Convert those timestamps to something usable for the plot
    for date in commit_dates:
        commit_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        utc_timezone = pytz.timezone('UTC')
        central_timezone = pytz.timezone('America/Chicago')
        central_date = utc_timezone.localize(
            commit_date).astimezone(central_timezone)
        commit_hours.append(central_date.hour)

    print(commit_lists)

    # Create a histogram
    bins = [x for x in range(25)]
    labels = ['12AM', '1AM', '2AM', '3AM', '4AM', '5AM', '6AM', '7AM', '8AM',
              '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM',
              '6PM', '7PM', '8PM', '9PM', '10PM', '11PM', '12AM']

    plt.figure(figsize=(10, 6), facecolor='black')
    plt.hist(commit_hours, bins=bins, edgecolor='black', alpha=0.7)
    plt.xlabel('Commit Hour', color='white', fontweight='bold')
    plt.ylabel('Number of Commits', color='white', fontweight='bold')
    plt.title(username + ' Commit Time Distribution (in Hours)',
              color='white', fontweight='bold')
    plt.xticks(bins, labels, rotation=45, ha='right', color='white',
               fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    ax = plt.gca()
    ax.set_facecolor('black')
    plt.show()


if __name__ == "__main__":
    username = 'bsbanotto'
    file = './json_files/' + username + '_commit_info.json'
    what_times(file)
