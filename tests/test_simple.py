import mygraphql

def test_simple_schema_creation():
    schema = mygraphql.Schema()

    @schema.mutation()
    def add(a: int, b: int) -> int:
        return a + b

    print(schema.graphql_schema)