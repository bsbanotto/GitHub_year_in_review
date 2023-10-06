#!/usr/bin/env python3
"""
The functions in this file work together to collect a calendar year's
worth of commit information and store it in a JSON file.
"""
import requests
import json
from datetime import datetime
import os


def get_commit_info(commit):
    """
    Extracts commit information from a GitHub API commit response.

    Args:
        commit (dict): A dictionary containing commit information from GitHub
                       API.

    Returns:
        dict: Extracted commit information including date and message.
    """
    return {
        'date': commit['commit']['author']['date'],
        'message': commit['commit']['message']
    }


def get_commit_metrics(
        username,
        repo_name,
        access_token,
        start_date,
        end_date
        ):
    """
    Retrieves commit metrics (earliest date, latest date, total commits, commit
    messages) for a given repository within a specified date range using GitHub
    API.

    Args:
        username (str): GitHub username.
        repo_name (str): Repository name.
        start_date (datetime): Start date for commit search.
        end_date (datetime): End date for commit search.

    Returns:
        tuple: A tuple containing earliest date, latest date, total commits,
               and commit messages.
    """
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    base_url = f'https://api.github.com/repos/{username}/{repo_name}/commits'
    params = {
        'author': username,
        'since': start_date.isoformat(),
        'until': end_date.isoformat(),
        'page': 1,
        'per_page': 100  # GitHub API max per_page value
    }
    earliest_date = None
    latest_date = None
    total_commits = 0
    commit_messages = []

    try:
        while True:
            response = requests.get(
                base_url,
                params=params,
                headers=headers,
                )

            # Print message to console
            print("Metrics: " + str(repo_name) +
                  "\t\tPage: " + str(params['page']), end="\r", flush=True)

            response.raise_for_status()
            commits = response.json()

            if not commits:
                break

            total_commits += len(commits)

            for commit in commits:
                commit_info = get_commit_info(commit)
                commit_messages.append(commit_info)

                commit_date = datetime.strptime(
                    commit_info['date'], '%Y-%m-%dT%H:%M:%SZ'
                    )

                if earliest_date is None or commit_date < earliest_date:
                    earliest_date = commit_date

                if latest_date is None or commit_date > latest_date:
                    latest_date = commit_date

            params['page'] += 1

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None, None, None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None, None

    return earliest_date, latest_date, total_commits, commit_messages


def get_commit_data_for_repos(
        username,
        repo_names,
        access_token,
        start_date,
        end_date
        ):
    """
    Retrieves commit data (metrics and messages) for a list of repositories.

    Args:
        username (str): GitHub username.
        repo_names (list): List of repository names.
        start_date (datetime object): Start date for query
        end_date (datetime object): End date for query

    Returns:
        dict: A dictionary containing commit data for each repository.
    """
    commit_data_per_repo = {}

    for repo_name in repo_names:
        earliest_date, latest_date, total_commits, commit_messages = \
            get_commit_metrics(
                               username,
                               repo_name,
                               access_token,
                               start_date,
                               end_date
                               )
        if earliest_date and latest_date and total_commits is not None:
            commit_data_per_repo[repo_name] = {
                'earliest_date': earliest_date.isoformat(),
                'latest_date': latest_date.isoformat(),
                'total_commits': total_commits,
                'commit_messages': commit_messages
            }

    return commit_data_per_repo


def create_commit_data_json(username, commit_data_per_repo, output_file):
    """
    Creates a JSON file containing commit data for each repository.

    Args:
        username (str): GitHub username.
        commit_data_per_repo (dict): Dictionary containing commit data for each
        repository.
        output_file (str): Path to the output JSON file.
    """
    data = {
        'username': username,
        'commit_data_per_repo': commit_data_per_repo
    }

    path = 'json_files'
    if not os.path.exists(path):
        os.makedirs(path)

    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)
