# GitHub Year in Review

If you're a Spotify user, or know someone who is, you know what the Spotify Year in Review is.

This project aims to do something similar, except for your GitHub!

## Project Status

This project is currently in development. An ever-evolving punch list is below:

~~- [X] Python files for API call to get a users repos and commit messages in JSON format using a persons access token.~~
- [X] Puthon files for API call to get a users repos and commit messages in JSON format using only their GitHub username.
- [ ] Extract simple statistics for a dashboard.
  - [ ] Total number of repos used.
  - [ ] Total number of commits.
  - [ ] Commits per repo.
- [ ] Create a word map of words used in commits.
- [ ] Sentiment analysis timeline on commit messages (were they useful commits or just fixing typos?).
- [ ] Remote hosting so people don't have to clone the repository, it just returns a nice image of a dashboard.

## Installation and Setup Instructions

I'll add instructions for a user to clone this repository and set up a conda environment to run locally. I think this is safest since as it is right now, they'll need an access token and this way that stays on their machine. If I can figure out that it'll work without needing an access token (should work since it's designed for public repos only) then maybe I can look at hosting on a lambda instance.

## Reflection

This project is something I've been thinking about for a while. I know the spotify year in review is coming up, and I'll be seeing that all over social media, so my goal is to get this wrapped up and mostly functional before then to try and ride that wave and see if I can convince my friends to give it a shot.

Something else I want to learn / focus on is making a good looking repo that's mostly ready for production. What's the correct file structure / heirarchy. How does data move around. These are things we don't really get to touch on a lot at Holberton. I want it to be as professional as possible for something that's mainly fun and farcical.

## Technologies Used

- Python Libraries
  - requests
  - json
  - datetime
- Anaconda
