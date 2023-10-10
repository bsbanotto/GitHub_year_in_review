# GitHub Year in Review

If you're a Spotify user, or know someone who is, you know what the Spotify Year in Review is.

This project aims to do something similar, except for your GitHub!

## Project Status

This project is currently in development. An ever-evolving punch list is below:

- [X] Python files for API call to get a users repos and commit messages in JSON format using a persons access token.

~~- [X] Puthon files for API call to get a users repos and commit messages in JSON format using only their GitHub username.~~

- [ ] Extract simple statistics for a dashboard.
  - [ ] Total number of repos used.
  - [ ] Total number of commits.
  - [X] Commits per repo.
  - [X] What times are you typically committing.
- [X] Create a word map of words used in commits.
- [ ] Sentiment analysis timeline on commit messages (were they useful commits or just fixing typos?).
- [ ] Remote hosting so people don't have to clone the repository, it just returns a nice image of a dashboard.

## Installation and Setup Instructions

To run this file in a conda environment:

```bash
git clone https://github.com/bsbanotto/GitHub_year_in_review.git
cd <cloned_repo>
conda env create -f environment.yml
conda activate GitHub_year_in_review
python3 ./run.py <username> <access_token>
```

If you want to remove the conda environment when you're done, follow these instructions.

```bash
conda deactivate
conda remove --name GitHub_year_in_review --all
```

 When prompted

```bash
Proceed ([y]/n)?
```

enter 'Y'

If you don't want to use a conda environment, the Python libraries for this code are below in the Technologies section. You can install locally and run without anaconda.

- Comming Soon - Google COLAB notebook so you won't have to worryabout a conda environment
- Comming Soon - Optional usage without access token (may not get all of your commits due to API limits)

## Reflection

This project is something I've been thinking about for a while. I know the spotify year in review is coming up, and I'll be seeing that all over social media, so my goal is to get this wrapped up and mostly functional before then to try and ride that wave and see if I can convince my friends to give it a shot.

Something else I want to learn / focus on is making a good looking repo that's mostly ready for production. What's the correct file structure / heirarchy. How does data move around. These are things we don't really get to touch on a lot at Holberton. I want it to be as professional as possible for something that's mainly fun and farcical.

## Technologies Used

- Python Libraries
  - requests
  - json
  - datetime
  - pytz
  - matplotlib
  - sys
  - os
  - imageio
- Anaconda
