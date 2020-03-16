import graphql
import mygraphql


def test_simple_fn():
    schema = mygraphql.Schema()

    @schema.query
    def hello() -> str:
        return 'world'

    query = '{ hello }'
    result = graphql.graphql_sync(schema.graphql_schema, query)
    assert result.data == {'hello': 'world'}


def test_fn_with_args():
    schema = mygraphql.Schema()

    @schema.query
    def hello(greeting: str) -> str:
        return greeting

    query = '{ hello(greeting: "Bob") }'
    result = graphql.graphql_sync(schema.graphql_schema, query)
    assert result.data == {'hello': 'Bob'}


def test_fn_with_defaults():
    schema = mygraphql.Schema()

    @schema.query
    def hello(who: str='World') -> str:
        return f'Hello {who}'

    query = '{ hello }'

    result = graphql.graphql_sync(schema.graphql_schema, query)
    assert result.data == {'hello': 'Hello World'}

    query = '{ hello(who: "Me") }'
    result = graphql.graphql_sync(schema.graphql_schema, query)
    assert result.data == {'hello': 'Hello Me'}
