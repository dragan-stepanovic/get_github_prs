A script that gets specified number of merged PRs from Github GraphQl and anonymizes sensitive data.

#### Required python3 libraries that need to be installed before running the script
- python_graphql_client (for retrieving PR data from GitHub)
- faker (for anonymizing data)

there is a [requirements.txt](https://github.com/dragan-stepanovic/get_github_prs/blob/main/requirements.txt) file, but if you prefer to install it directly:  
- `pip3 install python_graphql_client`  
- `pip3 install faker`

#### Usage 
`python3 src/get_prs.py organization repository number-of-prs-to-get your-github-token`

For example, for getting the last 15 merged PRs from https://github.com/symfony/polyfill repository, you would use:   
`python3 src/get_prs.py symfony polyfill 15 your-github-token`

Personal GitHub token can be generated from [this page](https://github.com/settings/tokens/new) and you'll need to select the `repo` scope in order to get the data needed for the PR analysis (you can see used GraphQl queries in [queries.py](https://github.com/dragan-stepanovic/get_github_prs/blob/main/src/queries.py)).  

If your organization requires SSO, you'll need to authorize the token using SSO in the [Personal access tokens (classic) page](https://github.com/settings/tokens).

#### Data anonymization  
Data that is anonymized are:  
- GitHub user ids used for authoring PRs and providing reviews (`'login'` field in GraphQl response from GitHub) and
- text of comments on the PR (`'bodyText'`)

The only things that is not anonymized from the potentially sensitive data is:  
- name of the repository (if it is private), and
- PR URLs  

There is possibility to anonymize this data as well, but in that case URLs in the [PR analysis report](https://app.co-create.team/) won't work.
