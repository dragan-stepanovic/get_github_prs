import json
import sys
from datetime import datetime

from anonymizer import Anonymizer
from github_client import GithubClient

TIMESTAMP_FORMAT = "%d-%m-%Y_%H-%M-%S"


def main():
    organization = sys.argv[1]
    repo = sys.argv[2]
    number_of_prs = int(sys.argv[3])
    token = sys.argv[4]

    to_anonymize = True
    if len(sys.argv) == 6:
        to_anonymize = sys.argv[5]

    print(in_yellow("Getting PRs..."))
    prs_as_json, number_of_prs = GithubClient.get_prs_as_json(organization, repo, number_of_prs, token)

    if should_not_anonymize(to_anonymize):
        print(in_green(f'Not anonymized PRs saved to {save_prs(prs_as_json, repo, number_of_prs)}'))
        return

    anonymized_prs, usernames_to_substitutes = Anonymizer().anonymize(prs_as_json)
    print(in_green(f'Anonymized PRs saved to {save_prs(anonymized_prs, repo, number_of_prs)}'))
    print(in_green(f'Usernames substitutes saved to {save_substitutes(usernames_to_substitutes)}'))


def should_not_anonymize(to_anonymize):
    return to_anonymize == '--plain'


def save_prs(anonymized_prs, repo, number_of_prs):
    return save_to_file(anonymized_prs, f'GitHub_last_{number_of_prs}_merged_PRs_in_{repo}')


def save_substitutes(usernames_to_substitutes):
    return save_to_file(usernames_to_substitutes, "Username_substitutes")


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
