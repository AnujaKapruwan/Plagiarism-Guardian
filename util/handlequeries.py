import requests


def run_request(queries, exclude_urls=[]):
    result = []
    #key = 'secret'
    #key1 = '7ac1ca7e9d1e4159a30a89f36415db70'
    #key2 = '239cc58c4f184eda978ab3148c2d945c'
    key1='c0a30445de7044f880ba3c391c67bee0'
    key2='ba4a9cafffa24cc0a2a6a4e6337c59e3'
    for query in queries:
        headers = {"Ocp-Apim-Subscription-Key": key1}
        params = {"q": query, "textDecorations": True, "textFormat": "HTML"}
        api_result = requests.get(
            'https://api.cognitive.microsoft.com/bing/v7.0/search',
            headers=headers, params=params)
        if api_result.status_code == 200:
            json = api_result.json()['webPages']
            for i in json['value']:
                add_result(i, result, exclude_urls)

            # Get another page of results from the API, so each query can yield up to 100 results
            if len(json['value']) > 49 and json['__next'] is not None:
                api_result = requests.get(
                    json['__next'] + '&$format=json',
                    auth=(key1, key2))
                if api_result.status_code == 200:
                    json = api_result.json()['d']
                    for i in json['results']:
                        add_result(i, result, exclude_urls)

    return result


def add_result(api_row, result_list, excluded_urls):
    # Second 'and' is explained here: http://stackoverflow.com/questions/3897499/check-if-value-already-exists-within-list-of-dictionaries
    if api_row['url'] not in excluded_urls and not any(dict.get('url', None) == api_row['url'] for dict in result_list):
        result_list.append({'displayurl': api_row['displayUrl'], 'desc': api_row['snippet'], 'url': api_row['url'],
                            'title': api_row['name']})

# Sort list; get top num_queries and return just the text
# chunks_with_scores is a list of tuples; each tuple is the chunk and its score
def build_query_result(chunks_with_scores, num_queries, source=''):
    sorted_chunks = sorted(chunks_with_scores, key=lambda score: score[1], reverse=True)[:num_queries]

    return {'success': True, 'data': [top_text[0] for top_text in sorted_chunks],
            'source': source}