#!/usr/bin/env python3
"""
Given our JSON containing commit messages, create a word cloud
"""
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json
from colors import *


def make_wordcloud(file, username):
    """
    Args:
        file (str): file name to extract information from
    """
    commit_lists = []
    with open(file) as f:
        data = json.load(f)

    commit_data_per_repo = data.get("commit_data_per_repo", {})

    # Get all of the commit messages
    for _, repo_data in commit_data_per_repo.items():
        commit_messages = repo_data.get("commit_messages", 0)
        commit_lists.append(commit_messages)

    all_words = []

    for inner_list in commit_lists:
        for item in inner_list:
            message = item.get('message', '')
            words = message.split()
            all_words.extend(words)

    # Create a word frequency dictionary
    word_frequencies = {}
    for word in all_words:
        word_frequencies[word] = word_frequencies.get(word, 0) + 1

    # Remove words with integers
    keys_to_remove = []
    for key, value in word_frequencies.items():
        if any(char.isdigit() for char in str(key)):
            keys_to_remove.append(key)

    for key in keys_to_remove:
        word_frequencies.pop(key, None)

    # Create a WordCloud object
    wordcloud = WordCloud(
        width=768,
        height=768,
        background_color='black',
        colormap='Set2').generate_from_frequencies(
        word_frequencies
        )

    # Display the word cloud using matplotlib
    plt.figure(figsize=(8, 8), facecolor='black')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    fname = './png_files/' + username + 'wordcloud.png'
    plt.savefig(fname=fname, format='png')
