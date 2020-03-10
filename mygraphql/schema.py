import graphql

from dataclasses import dataclass
from functools import partial

from .registry import TypeRegistry


@dataclass
class FieldDefinition:

    name: str
    fn: callable



class ObjectDefiner:

    def __init__(self):
        self.fields = {}

    def __call__(self, _fn=None, *, name=None):
        if _fn is None:
            return partial(self.__call__, name=name)

        if not callable(_fn):
            raise ValueError('todo')

        if name is None:
            name = _fn.__name__

        if name in self.fields:
            raise ValueError(f"Field named {name} already exists on this schema object")
        self.fields[name] = FieldDefinition(name, _fn)

        print('>>>', name)


class Schema:
    
    def __init__(self):
        self.type_registry = TypeRegistry()
        self.query = ObjectDefiner()
        self.mutation = ObjectDefiner()

    @property
    def graphql_schema(self):
        query_schema = self.query.make_for_schema(self)
        mutation_schema = self.mutation.make_for_schema(self)
        return graphql.GraphQLSchema(query=query_schema, mutation=mutation_schema)
    