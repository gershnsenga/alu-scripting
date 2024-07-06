#!/usr/bin/python3
"""
This module contains a recursive function to query the Reddit API
and return titles of all hot articles for a given subreddit.
"""
import requests


def recurse(subreddit, hot_list=None, after=None):
    """
    Recursively queries the Reddit API and returns a list containing
    the titles of all hot articles for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit.
        hot_list (list): List to store hot article titles (default: None).
        after (str): Token for pagination (default: None).

    Returns:
        list: List of hot article titles, or None if subreddit is invalid.
    """
    if hot_list is None:
        hot_list = []

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {
        'User-Agent': 'MyBot/1.0 (by /u/gershom)'
    }
    params = {
        'limit': 100,
        'after': after
    }

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False)

        if response.status_code != 200:
            return None

        data = response.json()
        posts = data['data']['children']

        if not posts:
            return hot_list

        for post in posts:
            hot_list.append(post['data']['title'])

        after = data['data']['after']
        if after:
            return recurse(subreddit, hot_list, after)
        else:
            return hot_list

    except Exception:
        return None


if __name__ == '__main__':
    result = recurse('python')
    if result is not None:
        print(len(result))
    else:
        print("None")
