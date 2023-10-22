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
from colors import *
import statistics


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
    labels = ['joy', 'fear', 'anger', 'sadness', 'surprise']
    score_data = {label: [] for label in labels}

    for entry in sentiment_scores_dict[max_repo]:
        for label in labels:
            scores = [i['score'] for i in entry if i['label'] == label]
            if scores:
                score_data[label].extend(scores)

    # Calculate the median value for each emotion
    median_values = {}
    for emotion, scores in score_data.items():
        median = statistics.median(scores)
        median_values[emotion] = median

    # Get the Highest and Second highest values
    sorted_medians = sorted(median_values.items(),
                            key=lambda x: x[1],
                            reverse=True)
    highest = sorted_medians[0][0]
    second_highest = sorted_medians[1][0]

    plt.figure(figsize=(8, 8), facecolor=BLACK)
    violin_parts = plt.violinplot(
        [score_data[label] for label in labels],
        showmeans=False,
        showmedians=True,
        showextrema=False,
    )

    # Customize colors for the violins
    colors = [TEAL, BLUE, NAVY, ORANGE, DARK_TEAL, LIGHT_ORANGE]
    for i, pc in enumerate(violin_parts['bodies']):
        pc.set_facecolor(colors[i])
        pc.set_edgecolor(WHITE)

    # Customize the plot
    plt.xticks(range(1, len(labels) + 1), labels)
    plt.title('Sentiment Analysis for ' + username + '/' + max_repo,
              color=WHITE,
              fontweight='bold',
              fontsize='xx-large',
              )
    plt.xlabel('Sentiment Labels',
               color=WHITE,
               fontweight='bold',
               fontsize='x-large',
               )
    plt.ylabel('Scores',
               color=WHITE,
               fontweight='bold',
               fontsize='x-large',
               )
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().xaxis.set_ticks_position('bottom')
    plt.gca().yaxis.set_ticks_position('left')
    plt.gca().tick_params(axis='both', colors=WHITE)
    plt.gca().set_facecolor(BLACK)

    # Set text color to white
    plt.rcParams['text.color'] = WHITE
    fname = './png_files/' + username + 'sentiment.png'
    plt.savefig(fname=fname, format='png')
