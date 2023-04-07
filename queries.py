def total_prs_count_query_for(organization, repository):
    return '''{
  repository(owner: "''' + organization + '''", name: "''' + repository + '''") {
    pullRequests(last: 1, states: MERGED) {
      totalCount
    }
  }
}
'''


def prs_query_for(organization, repository, batch_of_prs, before):
    return '''{
  repository(owner: "''' + organization + '''", name: "''' + repository + '''") {
    pullRequests(last: ''' + str(
        batch_of_prs) + ', states: MERGED, orderBy: {field: CREATED_AT, direction: ASC}' + before + ''')
    {
      pageInfo{
        startCursor
      }
      nodes {
        number
        url
        author {
          login
        }
        createdAt
        mergedAt
        additions
        deletions
        changedFiles
        timelineItems(first: 1, itemTypes: REVIEW_REQUESTED_EVENT) {
          nodes {
            ... on ReviewRequestedEvent {
              __typename
              createdAt
            }
          }
        }
        commits(first: 200) {
          totalCount
          nodes {
            commit {
              authoredDate
              additions
              deletions
              changedFiles
            }
          }
        }
        comments(first: 50) {
          nodes {
            author {
              login
            }
            createdAt
            bodyText
          }
        }
        reviews(first: 50) {
          nodes {
            author {
              login
            }
            createdAt
            bodyText
            comments(first: 50) {
              nodes {
                author {
                  login
                }
                createdAt
                bodyText
              }
            }
          }
        }
      }
    }
  }
}
'''
