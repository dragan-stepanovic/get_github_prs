from python_graphql_client import GraphqlClient

from queries import *


class GithubClient:
    GRAPHQL_URL = "https://api.github.com/graphql"
    BATCH_SIZE = 20

    @classmethod
    def get_prs_as_json(cls, org, repo, number_of_prs, token):
        number_of_prs_in_the_repo = cls.number_of_prs_in_repo(org, repo, token)
        prs_as_json = cls.get_prs_in_batches(org, repo, token,
                                             cls.batches_of_prs_to_get(number_of_prs, number_of_prs_in_the_repo,
                                                                       cls.BATCH_SIZE))
        return cls.remove_superfluous_fields(prs_as_json)

    @classmethod
    def number_of_prs_in_repo(cls, org, repo, token):
        response = GraphqlClient(cls.GRAPHQL_URL).execute(query=(total_prs_count_query_for(org, repo)),
                                                          headers=cls.include(token))
        return cls.prs_part_from(response)['totalCount']

    @classmethod
    def get_prs_in_batches(cls, organization, repository, token, batches):
        responses = []
        before = ''
        for batch in batches:
            query = prs_query_for(organization, repository, batch, before)
            response = GraphqlClient(cls.GRAPHQL_URL).execute(query=query, headers=cls.include(token))
            before = cls.before(cls.start_cursor_in(response))
            responses.append(response)

        return cls.assemble_to_a_single_response(responses)

    @classmethod
    def batches_of_prs_to_get(cls, total_number_asked, total_number_in_repo, batch_size):
        total_number_to_get = cls.total_number_of_prs_to_get(total_number_asked, total_number_in_repo)
        return cls.remove_empty_ones(
            cls.all_but_the_last_batch(batch_size, total_number_to_get) +
            cls.last_batch(batch_size, total_number_to_get))

    @classmethod
    def assemble_to_a_single_response(cls, responses):
        cumulative_response = cls.first_of(responses)
        [cls.add_prs_to(cumulative_response, a_response) for a_response in responses[1:]]
        return cumulative_response

    @classmethod
    def total_number_of_prs_to_get(cls, total_number_asked, total_number_in_repo):
        return min(total_number_asked, total_number_in_repo)

    @classmethod
    def all_but_the_last_batch(cls, batch_size, total_number):
        return (total_number // batch_size) * [batch_size]

    @classmethod
    def remove_empty_ones(cls, batches):
        return [batch for batch in batches if batch != 0]

    @classmethod
    def last_batch(cls, batch_size, total_number):
        return [total_number % batch_size]

    @classmethod
    def add_prs_to(cls, cumulative_response, this_response):
        cls.prs_part_from(cumulative_response)['nodes'] = \
            cls.prs_nodes_from(this_response) + cls.prs_nodes_from(cumulative_response)

    @classmethod
    def start_cursor_in(cls, response):
        return cls.prs_part_from(response)['pageInfo']['startCursor']

    @classmethod
    def prs_nodes_from(cls, response):
        return cls.prs_part_from(response)['nodes']

    @classmethod
    def prs_part_from(cls, response):
        return response['data']['repository']['pullRequests']

    @classmethod
    def before(cls, start_cursor):
        return f' before:"{start_cursor}"'

    @classmethod
    def include(cls, token):
        return {'Authorization': 'Bearer ' + token}

    @classmethod
    def first_of(cls, responses):
        return responses[0]

    @classmethod
    def remove_superfluous_fields(cls, prs_as_json):
        del prs_as_json['data']['repository']['pullRequests']['pageInfo']
        return prs_as_json
