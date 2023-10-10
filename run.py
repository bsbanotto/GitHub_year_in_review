#!/usr/bin/env python3
"""
Entry point
"""
import sys
from datetime import datetime
import os


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 run.y <username> <access_token>")
        sys.exit(1)

    username = sys.argv[1]
    access_token = sys.argv[2]
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    filename = './json_files/' + username + '_commit_info.json'

    # First, get all of a users repositories
    get_github_repos = __import__('get_repos').get_github_repos
    repo_names = get_github_repos(username, access_token)

    # Second, get all of the commit messages they authored and save to JSON
    get_commit_data_for_repos = __import__(
        'get_repo_commits'
        ).get_commit_data_for_repos
    commit_info_per_repo = get_commit_data_for_repos(
        username,
        repo_names,
        access_token,
        start_date,
        end_date
        )

    create_commit_data_json = __import__(
        'get_repo_commits'
        ).create_commit_data_json

    create_commit_data_json(username, commit_info_per_repo, filename)

    # Create a pie chart
    make_pie = __import__('make_pie_chart').make_pie
    make_pie(filename, username)

    # Create a histogram
    make_histogram = __import__('time_histogram').what_times
    make_histogram(filename, username)

    # Create a word cloud
    make_wordcloud = __import__('make_word_cloud').make_wordcloud
    make_wordcloud(filename)

    # Sentiment Analysis Violin Plot
    sentiment_analysis = __import__('sentiment_analysis').sentiment
    sentiment_analysis(filename, username)
