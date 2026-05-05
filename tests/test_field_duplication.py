import pytest
from unittest.mock import patch, MagicMock
from ch05.exploit_threaded_field_dup import build_field_dup_query, DoS


class TestBuildFieldDupQuery:
    def test_content_field_repeated_correctly(self):
        query = build_field_dup_query(repeat=1000)
        assert query['query'].count('content') == 1000

    def test_title_field_repeated_correctly(self):
        query = build_field_dup_query(repeat=1000)
        assert query['query'].count('title') == 1000

    def test_custom_repeat_count(self):
        for n in (1, 5, 50):
            query = build_field_dup_query(repeat=n)
            assert query['query'].count('content') == n
            assert query['query'].count('title') == n

    def test_query_starts_with_query_keyword(self):
        query = build_field_dup_query(repeat=1)
        assert query['query'].lstrip().startswith('query')

    def test_returns_dict_with_query_key(self):
        query = build_field_dup_query(repeat=10)
        assert isinstance(query, dict)
        assert 'query' in query


class TestDoSErrorHandling:
    def test_successful_request_does_not_raise(self):
        query = build_field_dup_query(repeat=1)
        mock_response = MagicMock()
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_response.json.return_value = {'data': {}}
        with patch('ch05.exploit_threaded_field_dup.requests.post', return_value=mock_response):
            DoS('http://localhost:5013/graphql', query)

    def test_exception_handler_no_attribute_error(self):
        """Regression: e.message does not exist in Python 3; str(e) must be used instead."""
        query = build_field_dup_query(repeat=1)
        with patch('ch05.exploit_threaded_field_dup.requests.post') as mock_post:
            mock_post.side_effect = Exception('connection refused')
            # Must not raise AttributeError
            DoS('http://localhost:5013/graphql', query)

    def test_connection_error_is_handled(self):
        import requests as req
        query = build_field_dup_query(repeat=1)
        with patch('ch05.exploit_threaded_field_dup.requests.post') as mock_post:
            mock_post.side_effect = req.exceptions.ConnectionError('refused')
            DoS('http://localhost:5013/graphql', query)
