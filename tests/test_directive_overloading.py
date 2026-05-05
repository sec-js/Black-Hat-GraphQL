import pytest
from ch05.exploit_directive_overloading import build_directive_payload


class TestBuildDirectivePayload:
    def test_directive_count_matches_multiplier(self):
        payload = build_directive_payload(100)
        assert payload['query'].count('@dos') == 100

    def test_zero_directives(self):
        payload = build_directive_payload(0)
        assert payload['query'].count('@dos') == 0

    def test_single_directive(self):
        payload = build_directive_payload(1)
        assert payload['query'].count('@dos') == 1

    def test_large_multiplier(self):
        payload = build_directive_payload(30000)
        assert payload['query'].count('@dos') == 30000

    def test_query_contains_typename(self):
        payload = build_directive_payload(5)
        assert '__typename' in payload['query']

    def test_query_starts_with_query_keyword(self):
        payload = build_directive_payload(5)
        assert payload['query'].lstrip().startswith('query')

    def test_returns_dict_with_query_key(self):
        payload = build_directive_payload(10)
        assert isinstance(payload, dict)
        assert 'query' in payload

    def test_directives_are_contiguous(self):
        n = 5
        payload = build_directive_payload(n)
        assert '@dos' * n in payload['query']
