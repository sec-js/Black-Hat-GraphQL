import pytest
from ch05.array_based_circular_queries import build_circular_query


def _count_depth(query_string):
    depth = max_depth = 0
    for ch in query_string:
        if ch == '{':
            depth += 1
            max_depth = max(max_depth, depth)
        elif ch == '}':
            depth -= 1
    return max_depth


class TestBuildCircularQuery:
    def test_braces_are_balanced(self):
        query, _ = build_circular_query('pastes', 'owner', 10, 5)
        assert query['query'].count('{') == query['query'].count('}')

    def test_depth_matches_formula(self):
        field_repeat = 10
        query, _ = build_circular_query('pastes', 'owner', field_repeat, 5)
        assert _count_depth(query['query']) == field_repeat * 2 + 1

    def test_depth_with_custom_field_repeat(self):
        for field_repeat in (1, 3, 7):
            query, _ = build_circular_query('pastes', 'owner', field_repeat, 1)
            assert _count_depth(query['query']) == field_repeat * 2 + 1

    def test_typename_appears_exactly_once(self):
        query, _ = build_circular_query('pastes', 'owner', 10, 5)
        assert query['query'].count('__typename') == 1

    def test_array_length_matches_parameter(self):
        _, queries = build_circular_query('pastes', 'owner', 10, 5)
        assert len(queries) == 5

    def test_custom_array_length(self):
        for length in (1, 3, 10):
            _, queries = build_circular_query('pastes', 'owner', 5, length)
            assert len(queries) == length

    def test_query_starts_with_query_keyword(self):
        query, _ = build_circular_query('pastes', 'owner', 10, 5)
        assert query['query'].lstrip().startswith('query {')

    def test_field_names_present_in_query(self):
        query, _ = build_circular_query('nodes', 'edges', 4, 2)
        assert 'nodes' in query['query']
        assert 'edges' in query['query']

    def test_all_array_elements_are_same_query(self):
        query, queries = build_circular_query('pastes', 'owner', 5, 3)
        for q in queries:
            assert q['query'] == query['query']
