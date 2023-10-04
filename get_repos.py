#!/usr/bin/env python3
"""
This file will return a list of a users github repos
"""
import requests


def get_github_repos(username, access_token):
    """
    Extracts a users GitHub repositories

    Args:
        username (string): GitHub username.
        access_token (string): GitHub personal access token.

    Returns:
        list: A list of all of a users repositories
    """
    base_url = 'https://api.github.com'
    endpoint = f'/users/{username}/repos'
    headers = {
        # 'Authorization': f'Bearer {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Make the API request to get the user's repositories
    try:
        response = requests.get(base_url + endpoint,
                                headers=headers
                                )
        response.raise_for_status()
        repos = response.json()
        repo_list = [repo['name'] for repo in repos]
        return repo_list
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    username = 'bsbanotto'
    access_token = 'ACCESS_TOKEN_HERE'

    repos = get_github_repos(username, access_token)
    if repos:
        print(f"GitHub repositories for {username}:")
        for repo in repos:
            print(repo)
    else:
        print("Failed to retrieve GitHub repositories.")
