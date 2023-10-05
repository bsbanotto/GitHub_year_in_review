#!/usr/bin/env python3
"""
This function will get the time stamps for a users commits and create a
histogram to see what time of day they are typically working.
"""
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def what_times(file):
    """
    Args:
        file (str): file name to extract information from
    """
    commit_dates, commit_lists, commit_hours = [], [], []
    offset = timedelta(hours=-6)
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
        commit_date += offset
        commit_hours.append(commit_date.hour)

    # Create a histogram
    plt.figure(figsize=(10, 6))
    plt.hist(commit_hours, bins=24, range=(0, 24), edgecolor='black', alpha=0.7)
    plt.xlabel('Commit Hour')
    plt.ylabel('Number of Commits')
    plt.title('Commit Time Distribution (in Hours)')
    plt.xticks(range(0, 25))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


if __name__ == "__main__":
    username = 'sarahmarkland'
    file = './json_files/' + username + '_commit_info.json'
    what_times(file)