A script gets specified number of last merged PRs from a Github repository, anonymizes sensitive data, and saves the PRs into a file that is later used for PR analysis in the [co-create tool](https://app.co-create.team/).

#### Required python3 libraries that need to be installed before running the script
- `python_graphql_client` (for retrieving PR data from GitHub)
- `faker` (for anonymizing sensitive data)

there is a [requirements.txt](https://github.com/dragan-stepanovic/get_github_prs/blob/main/requirements.txt) file, but if you prefer to install it directly:  
- `pip3 install python_graphql_client`  
- `pip3 install faker`
  
  
#### Usage 
`python3 src/get_prs.py organization repository number-of-prs-to-get your-github-token`

For example, for getting the last 15 merged PRs from https://github.com/symfony/polyfill repository, you would use:   
`python3 src/get_prs.py symfony polyfill 15 your-github-token`  
  
#### GitHub token
Personal GitHub token can be generated from [this page](https://github.com/settings/tokens/new) and you'll need to select the `repo` scope in order to get the data needed for the PR analysis (you can see used GraphQl queries in [queries.py](https://github.com/dragan-stepanovic/get_github_prs/blob/main/src/queries.py)).  

If your organization requires SSO, you'll need to authorize the token using SSO in the [Personal access tokens (classic) page](https://github.com/settings/tokens).
  
  
#### Data anonymization  
Data is anonymized by default.
Data that is anonymized are:  
- GitHub usernames used for authoring and reviewing PRs (`'login'` field in GraphQl response from GitHub), and
- PR comments (`'bodyText'` in GraphQl)

For every username a substitute is used instead. The script also produces a file with the mapping from usernames to substitutes that were used, and it's prefixed with `Username_substitutes`. 

To **_turn off_** anonymization, you can pass `-plain` as the last argument.

Things that are not anonymized from the potentially sensitive data are:  
- name of the repository (if it is private), and
- PR numbers, which are used in the PR URLs in the following format `https://github.com/symfony/polyfill/pull/427` (repository name + PR number)

There is possibility to anonymize this data as well, but in that case URLs in the [PR analysis report](https://app.co-create.team/) won't work.
