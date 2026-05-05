import pytest
from pathlib import Path
from graphql import build_schema

REPO_ROOT = Path(__file__).parent.parent
CH04_SCHEMA = (REPO_ROOT / 'ch04' / 'sdl.graphql').read_text()
CH05_SCHEMA = (REPO_ROOT / 'ch05' / 'sdl.graphql').read_text()


class TestCh05Schema:
    @pytest.fixture(scope='class')
    def schema(self):
        return build_schema(CH05_SCHEMA)

    def test_parses_without_error(self):
        assert build_schema(CH05_SCHEMA) is not None

    def test_has_query_type(self, schema):
        assert schema.query_type is not None

    def test_has_mutation_type(self, schema):
        assert schema.mutation_type is not None

    def test_has_subscription_type(self, schema):
        assert schema.subscription_type is not None

    def test_query_fields_present(self, schema):
        fields = set(schema.query_type.fields)
        expected = {
            'pastes', 'paste', 'systemUpdate', 'systemDiagnostics',
            'systemDebug', 'systemHealth', 'users', 'readAndBurn',
            'search', 'audits', 'deleteAllPastes', 'me',
        }
        assert expected.issubset(fields)

    def test_mutation_fields_present(self, schema):
        fields = set(schema.mutation_type.fields)
        expected = {
            'createPaste', 'editPaste', 'deletePaste',
            'uploadPaste', 'importPaste', 'createUser', 'login',
        }
        assert expected.issubset(fields)

    def test_paste_object_core_fields(self, schema):
        paste = schema.type_map['PasteObject']
        for field in ('id', 'title', 'content', 'owner', 'burn', 'public'):
            assert field in paste.fields

    def test_owner_object_has_pastes(self, schema):
        owner = schema.type_map['OwnerObject']
        assert 'pastes' in owner.fields

    def test_search_result_union_members(self, schema):
        union = schema.type_map['SearchResult']
        names = {t.name for t in union.types}
        assert names == {'PasteObject', 'UserObject'}

    def test_user_input_required_fields(self, schema):
        user_input = schema.type_map['UserInput']
        for field in ('username', 'email', 'password'):
            assert field in user_input.fields

    def test_show_network_directive_declared(self, schema):
        assert 'show_network' in schema.directives or any(
            d.name == 'show_network' for d in schema.directives
        )

    def test_datetime_scalar_declared(self, schema):
        assert 'DateTime' in schema.type_map

    def test_subscription_has_paste_field(self, schema):
        assert 'paste' in schema.subscription_type.fields


class TestCh04Schema:
    def test_parses_without_error(self):
        assert build_schema(CH04_SCHEMA) is not None

    def test_matches_ch05_schema(self):
        assert CH04_SCHEMA == CH05_SCHEMA
