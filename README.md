A script that gets specified number of merged PRs from Github GraphQl and anonymizes sensitive data.

### Required python libraries that need to be installed before running the script
- python_graphql_client (for retrieving PR data from GitHub)
- faker (for anonymizing data)

`pip3 install python_graphql_client`  
`pip3 install faker`

### Usage example  
`python3 src/get_prs.py organization repository number-of-prs-to-get your-github-token`

For getting last 15 merged PRs of https://github.com/symfony/polyfill repository, we would use:   
`python3 src/get_prs.py symfony polyfill 15 my-github-token`

GitHub token 
