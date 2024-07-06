#!/usr/bin/python3
"""
This module contains a recursive function to query the Reddit API,
parse hot article titles, and count specified keywords.
"""
import re
import requests


def count_words(subreddit, word_list, after=None, word_count=None):
    """
    Recursively queries the Reddit API, parses hot article titles,
    and counts occurrences of specified keywords.

    Args:
        subreddit (str): The name of the subreddit.
        word_list (list): List of keywords to count.
        after (str): Token for pagination (default: None).
        word_count (dict): Dictionary to store word counts (default: None).

    Returns:
        dict: Dictionary with word counts, or None if subreddit is invalid.
    """
    if word_count is None:
        word_count = {}
        for word in word_list:
            word_count[word.lower()] = 0

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {
        'User-Agent': 'MyBot/1.0 (by /u/YourUsername)'
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
            print_results(word_count)
            return word_count

        for post in posts:
            title = post['data']['title'].lower()
            for word in word_list:
                word = word.lower()
                count = len(re.findall(r'\b{}\b'.format(re.escape(word)), title))
                word_count[word] += count

        after = data['data']['after']
        if after:
            return count_words(subreddit, word_list, after, word_count)
        else:
            print_results(word_count)
            return word_count

    except Exception:
        return None


def print_results(word_count):
    """
    Prints the word count results in the specified format.

    Args:
        word_count (dict): Dictionary with word counts.
    """
    sorted_counts = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
    for word, count in sorted_counts:
        if count > 0:
            print(f"{word.lower()}: {count}")


if __name__ == '__main__':
    count_words('programming', ['python', 'java', 'JavaScript'])
