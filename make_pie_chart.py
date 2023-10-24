#!/usr/bin/env python3
"""
The method in this file will extract number of commits per repo
from a users json file and create a pie chart with the distribution
"""
import matplotlib.pyplot as plt
from colors import *


def make_pie(username, repo_names, commit_counts):
    """
    Args:
        file (str): file name to extract information from
        username (str): github username
        repo_names (list): list of a users repos
        commit_counts (list): list of commits per repo
    """
    other = 0
    to_pop = 0

    # Sort the lists by commit counts in descending order
    sorted_data = sorted(zip(commit_counts, repo_names), reverse=True)
    commit_counts, repo_names = zip(*sorted_data)
    commit_counts = list(commit_counts)
    repo_names = list(repo_names)

    percent = round((commit_counts[0] / sum(commit_counts)) * 100)

    # print("You were most active in " + repo_names[0] + " with " +
    #       str(percent) + "% of your total commits")

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

    # Build the Pie Chart
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.gca().set_position([0, 0, 1, .9])
    fig.patch.set_facecolor(BLACK)
    ax.set_facecolor(BLACK)

    to_explode = []
    for x in range(0, len(repo_names)):
        to_explode.append(0.01)

    to_explode[0] = 0.05

    colors = [NAVY, ORANGE, BLUE, DARK_TEAL, LIGHT_ORANGE, GREY, TEAL]

    ax.pie(commit_counts,
           autopct='%1.1f%%',
           shadow=True,
           explode=tuple(to_explode),
           startangle=0,
           colors=colors,
           textprops={'color': WHITE}
           )

    ax.set_title(username + ' - Commits per Repository', color=WHITE,
                 fontweight='bold', fontsize='x-large')
    fname = './png_files/' + username + 'piechart.png'
    plt.legend(labels=repo_names,
               )
    plt.savefig(fname=fname, format='png')
