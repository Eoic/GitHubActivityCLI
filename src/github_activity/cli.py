import sys
import json
import argparse
from urllib.request import urlopen
from urllib.error import HTTPError

URL = lambda username: f'https://api.github.com/users/{username}/events'


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
        contents = urlopen(URL(username))
        parse_user_contents(contents)
    except HTTPError as e:
        if e.status == 404:
            print(f'User "{username}" was not found.', file=sys.stderr)
            return

        print("An error occured while fetching user data.", file=sys.stderr)


def parse_user_contents(contents):
    try:
        data = json.loads(contents.read())
        json_formatted_str = json.dumps(data, indent=2)
        print(json_formatted_str)
    except (json.JSONDecodeError, TypeError) as e:
        print("An error occured while reading user data.", file=sys.stderr)
        print(e)
