#!/usr/bin/python3
"""
This module contains a function to query the Reddit API
and return the number of subscribers for a given subreddit.
"""
import requests


def number_of_subscribers(subreddit):
    """
    Queries the Reddit API and returns the number of subscribers
    for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit.

    Returns:
        int: The number of subscribers. Returns 0 for invalid subreddits.
    """
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = {
        'User-Agent': 'MyBot/1.0 (by /u/gershom)'
    }

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code == 200:
            data = response.json()
            return data['data']['subscribers']
        return 0
    except Exception:
        return 0


if __name__ == "__main__":
    subscribers = number_of_subscribers('python')
    print(f"Number of subscribers: {subscribers}")
