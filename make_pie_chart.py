#!/usr/bin/env python3
"""
The method in this file will extract number of commits per repo
from a users json file and create a pie chart with the distribution
"""
import json
import matplotlib.pyplot as plt


def make_pie(file):
    """
    Args:
        file (str): file name to extract information from
    """
    with open(file) as f:
        parsed_data = json.load(f)

    commit_data_per_repo = parsed_data.get("commit_data_per_repo", {})

    repo_names = []
    commit_counts = []
    other = 0
    to_pop = 0

    for repo_name, repo_data in commit_data_per_repo.items():
        total_commits = repo_data.get("total_commits", 0)
        repo_names.append(repo_name)
        commit_counts.append(total_commits)

    # Sort the lists by commit counts in descending order
    sorted_data = sorted(zip(commit_counts, repo_names), reverse=True)
    commit_counts, repo_names = zip(*sorted_data)
    commit_counts = list(commit_counts)
    repo_names = list(repo_names)

    # Group all repos with less than 2.5% commit volume to 'other'
    threshold = 0.025 * sum(commit_counts)

    for i in range(0, len(commit_counts)):
        if commit_counts[i] < threshold:
            other += commit_counts[i]
            to_pop += 1

    repo_names = repo_names[:-to_pop]
    repo_names.append('Others (' + str(to_pop) + ')')

    commit_counts = commit_counts[:-to_pop]
    commit_counts.append(other)

    plt.figure(figsize=(10, 6))
    plt.pie(commit_counts, labels=repo_names, autopct='%1.1f%%')
    plt.title(username + ' - Commits per Repository')
    plt.show()


if __name__ == "__main__":
    username = 'claybowl'
    file = './json_files/' + username + '_commit_info.json'
    make_pie(file)
