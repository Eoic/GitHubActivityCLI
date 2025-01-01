import sys
import json
import argparse
from datetime import datetime
from operator import itemgetter
from typing import Dict, List, Tuple
from urllib.request import urlopen
from urllib.error import HTTPError

from github_activity.event_parser import EventParser


def url(username: str):
    return f'https://api.github.com/users/{username}/events'


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='github-activity',
        description='A CLI tool for viewing GitHub user\'s activity.',
        usage='%(prog)s <username>',
    )

    parser.add_argument('username', type=str, help='GitHub username')

    return parser


def process_command(args: argparse.Namespace):
    username = args.username

    try:
        contents = urlopen(url(username))
        summary = parse_user_contents(contents)
        print_summary(summary)
    except HTTPError as e:
        if e.status == 404:
            print(f'User "{username}" was not found.', file=sys.stderr)
            return

        print("An error occured while fetching user data.", file=sys.stderr)


def parse_user_contents(contents):
    try:
        data = json.loads(contents.read())
        summary = EventParser.summarize_events(data)
        return summary
    except (json.JSONDecodeError, TypeError):
        print("An error occured while reading user data.", file=sys.stderr)


def print_summary(summary: Dict):
    print('Output:')

    for date, month_summary in summary.items():
        month_summary = sorted(month_summary, key=itemgetter(1), reverse=True)

        print('  ', date)

        for item in month_summary:
            print(
                '    -',
                itemgetter(0)(item),
                'at',
                itemgetter(1)(item).strftime('%m/%d, %H:%m'),
            )
