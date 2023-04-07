import json
import sys
from datetime import datetime

from anonymizer import Anonymizer
from github_client import GithubClient

TIMESTAMP_FORMAT = "%d-%m-%Y_%H-%M-%S"


def main():
    organization = sys.argv[1]
    repository = sys.argv[2]
    number_of_prs = int(sys.argv[3])
    token = sys.argv[4]

    print(in_yellow("Getting PRs..."))
    anonymized_prs, usernames_to_substitutes = Anonymizer() \
        .anonymize(GithubClient.get_prs_as_json(organization, repository, number_of_prs, token))

    print(in_green(f'PRs saved to {save_to_file(anonymized_prs, "GitHub_PRs")}'))
    print(in_green(f'Username substitutes saved to {save_to_file(usernames_to_substitutes, "Username_substitutes")}'))


def save_to_file(prs_as_json, prefix):
    filename = f'./{prefix}_{datetime.now().strftime(TIMESTAMP_FORMAT)}.json'
    with open(filename, 'w') as into_file:
        json.dump(prs_as_json, into_file)

    return filename


def in_yellow(text):
    return '\033[33m' + text + '\033[0m'


def in_green(text):
    return '\033[32m' + text + '\033[0m'


if __name__ == '__main__':
    main()
