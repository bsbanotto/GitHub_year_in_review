#!/usr/bin/env python3
"""
Extracts relevant information from JSON file
"""
import json


def extract(filename):
    """
    Args:
        filename (str): path to appropriate user JSON file

    Returns:
        repo_names (list): list of all of a users repos
        commit_counts (list): list of commit counts per repo
        num_repos (int): total number of repos committed to
        num_commits (int): total number of commit messages
    """ 
    with open(filename) as f:
        parsed_data = json.load(f)

    commit_data_per_repo = parsed_data.get("commit_data_per_repo", {})

    repo_names = []
    commit_counts = []

    for repo_name, repo_data in commit_data_per_repo.items():
        total_commits = repo_data.get('total_commits', 0)
        repo_names.append(repo_name)
        commit_counts.append(total_commits)

    num_repos = len(repo_names)
    num_commits = sum(commit_counts)

    return repo_names, commit_counts, num_repos, num_commits
