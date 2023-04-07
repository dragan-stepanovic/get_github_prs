import json
import sys
from datetime import datetime

from anonymizer import Anonymizer
from client import GithubClient

TIMESTAMP_FORMAT = "%d-%m-%Y_%H-%M-%S"


def main():
    organization = sys.argv[1]
    repository = sys.argv[2]
    number_of_prs = int(sys.argv[3])
    token = sys.argv[4]

    print(in_yellow("Getting PRs..."))
    filename = save_to_file(Anonymizer().anonymize(GithubClient.get_prs_as_json(organization, repository, number_of_prs, token)))
    print(in_green(f'File saved to {filename}'))


def save_to_file(prs_as_json):
    filename = f'./GitHub_PRs_{datetime.now().strftime(TIMESTAMP_FORMAT)}.json'
    with open(filename, 'w') as into_file:
        json.dump(prs_as_json, into_file)

    return filename


def in_yellow(text):
    return '\033[33m' + text + '\033[0m'


def in_green(text):
    return '\033[32m' + text + '\033[0m'


if __name__ == '__main__':
    main()
