#!/usr/bin/env python3
"""
Using Distilbert-base-uncased-emotion model from the Hugging Face Hub to do
sentiment analysis on the list of a users commit messages from their most
committed to repository
"""
from transformers import pipeline
import json
from collections import defaultdict
import matplotlib.pyplot as plt


def sentiment(file, username):
    """
    Args:
        file (str): file name to extract information from
        username (str): github username
    """
    max_repo = ''
    total_commits = 0
    # Dictionary with key = repo name, values = list of commit messages
    commits_dict = {}
    with open(file) as f:
        data = json.load(f)

    commit_data_per_repo = data.get('commit_data_per_repo', {})

    for repo_name, repo_data in commit_data_per_repo.items():
        repo_commits = repo_data.get('total_commits', [])
        if repo_commits > total_commits:
            total_commits = repo_commits
            max_repo = repo_name

    for repo_name, repo_data in commit_data_per_repo.items():
        commit_messages = repo_data.get('commit_messages', [])
        messages = [commit['message'] for commit in commit_messages]
        commits_dict[repo_name] = messages

    # Dictionary with key = repo name, values = list of commit message
    # sentiment analysis score dictionaries
    sentiment_scores_dict = defaultdict(list)

    classifier = pipeline(
        'text-classification',
        model='bhadresh-savani/distilbert-base-uncased-emotion',
        top_k=None
        )

    for repository, commit_messages in commits_dict.items():
        for commit_message in commit_messages:
            sentiment_scores_dict[repository] += classifier(commit_message)

    # Create a violin plot of sentiment
    labels = ['joy', 'fear', 'anger', 'sadness', 'surprise', 'love']
    score_data = {label: [] for label in labels}

    for entry in sentiment_scores_dict[max_repo]:
        for label in labels:
            scores = [i['score'] for i in entry if i['label'] == label]
            if scores:
                score_data[label].extend(scores)

    plt.figure(figsize=(10, 6), facecolor='black')
    violin_parts = plt.violinplot(
        [score_data[label] for label in labels],
        showmeans=False,
        showmedians=True,
        showextrema=False,
    )

    # Customize colors for the violins
    colors = ['purple', 'blue', 'green', 'orange', 'red', 'pink']
    for i, pc in enumerate(violin_parts['bodies']):
        pc.set_facecolor(colors[i])
        pc.set_edgecolor('white')

    # Customize the plot
    plt.xticks(range(1, len(labels) + 1), labels)
    plt.title('Sentiment Analysis for ' + username + '/' + max_repo,
              color='white',
              fontweight='bold',
              fontsize='xx-large',
              )
    plt.xlabel('Sentiment Labels',
               color='white',
               fontweight='bold',
               fontsize='x-large',
               )
    plt.ylabel('Scores',
               color='white',
               fontweight='bold',
               fontsize='x-large',
               )
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().xaxis.set_ticks_position('bottom')
    plt.gca().yaxis.set_ticks_position('left')
    plt.gca().tick_params(axis='both', colors='white')
    plt.gca().set_facecolor('black')

    # Set text color to white
    plt.rcParams['text.color'] = 'white'

    plt.show()
