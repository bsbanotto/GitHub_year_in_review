#!/usr/bin/env python3
import requests

def get_user_commits_for_date_range(username, start_date, end_date, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    num_calls = 0

    # Step 2: Retrieve user's repositories
    repos_url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(repos_url, headers=headers)

    if response.status_code != 200:
        print(f'Failed to retrieve repositories: {response.json()["message"]}')
        return

    repositories = response.json()
    # print(repositories)

    # Step 3: Iterate over repositories and retrieve commits
    for repo in repositories:
        repo_name = repo['name']
        commits_url = f'https://api.github.com/repos/{username}/{repo_name}/commits'
        params = {
            'author': username,
            'since': start_date,
            'until': end_date,
            'page': 1,
            'per_page': 100
        }
        while True:
            commits_response = requests.get(commits_url, headers=headers, params=params)
            num_calls += 1
            print("Metrics: " + str(params) + str(repo_name) + str(commits_response), end="\r", flush=False)

            if not commits_response:
                break

            params['page'] += 1

        if commits_response.status_code != 200:
            print(f'Failed to retrieve commits for {repo_name}: {commits_response.json()["message"]}')
            continue

        commits = commits_response.json()

        # Step 4: Filter and print commits authored by the user
        for commit in commits:
            print(f'Repository: {repo_name}, Commit Message: {commit["commit"]["message"]}')

# Replace with your GitHub username, start date, end date, and access token
github_username = 'claybowl'
start_date = '2023-01-01T00:00:00Z'
end_date = '2023-12-31T23:59:59Z'
access_token = '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'

get_user_commits_for_date_range(github_username, start_date, end_date, access_token)
