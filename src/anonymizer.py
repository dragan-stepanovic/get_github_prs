from faker import Faker


class Anonymizer:

    def __init__(self):
        self.faker = Faker()

    def anonymize(self, prs_as_json):
        self.anonymize_usernames(prs_as_json, self.usernames_to_substitutes(prs_as_json))
        self.anonymize_comments(prs_as_json)
        return prs_as_json

    def usernames_to_substitutes(self, prs_as_json):
        return {username: self.faker.user_name() for username in self.unique(self.all_usernames_in(prs_as_json))}

    def anonymize_usernames(self, json_data, logins_to_substitutes):
        results = []
        if isinstance(json_data, list):
            for item in json_data:
                results += self.anonymize_usernames(item, logins_to_substitutes)
        elif isinstance(json_data, dict):
            for key, value in json_data.items():
                if key == 'login':
                    json_data[key] = logins_to_substitutes[json_data[key]]
                else:
                    results += self.anonymize_usernames(value, logins_to_substitutes)
        return results

    def anonymize_comments(self, json_data):
        results = []
        if isinstance(json_data, list):
            for item in json_data:
                results += self.anonymize_comments(item)
        elif isinstance(json_data, dict):
            for key, value in json_data.items():
                if key == 'bodyText':
                    json_data[key] = self.anonymize_comment(json_data[key])
                else:
                    results += self.anonymize_comments(value)
        return results

    def all_usernames_in(self, json_data):
        results = []
        if isinstance(json_data, list):
            for item in json_data:
                results += self.all_usernames_in(item)
        elif isinstance(json_data, dict):
            for key, value in json_data.items():
                if key == 'login':
                    results.append(value)
                else:
                    results += self.all_usernames_in(value)
        return results

    def anonymize_comment(self, comment):
        words = comment.split()
        return self.faker.sentence(nb_words=len(words), variable_nb_words=False)

    @classmethod
    def unique(cls, duplicates):
        return list(set(duplicates))
