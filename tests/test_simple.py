import mygraphql
import graphql

def test_simple_schema_creation():
    schema = mygraphql.Schema()

    @schema.mutation()
    def add(a: int, b: int) -> int:
        return a + b

    print(graphql.print_schema(schema.graphql_schema))