from dataclasses import dataclass
from functools import partial

import graphql

from .field import field_from_fn
from .mapper import BLANK_VALUE, MAPPER
from .registry import TypeRegistry


@dataclass
class FieldDefinition:

    name: str
    fn: callable


class CustomType:

    def __init__(self, name, description=""):
        self.name = name
        self.description = description
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

    def _map_fields(self, mapper):
        return {n: field_from_fn(mapper, fn) for (n, fn) in self.fields.items()}

    def _map_interfaces(self, mapper):
        return []


@MAPPER.add_mapper
def map_custom_type(mapper, obj):
    if isinstance(obj, CustomType):
        if not obj.fields:
            return BLANK_VALUE
        return graphql.GraphQLObjectType(
            name=obj.name,
            fields=partial(obj._map_fields, mapper),
            interfaces=partial(obj._map_interfaces, mapper),
            description=obj.description,
        )



class Schema:
    
    def __init__(self, mapper=None):
        if mapper is None:
            mapper = MAPPER.new()
        self.mapper = mapper
        self.query = CustomType('Query', 'The root query object')
        self.mutation = CustomType('Mutation', 'The root mutation object')

    @property
    def graphql_schema(self):
        return graphql.GraphQLSchema(
            query=self.mapper.map(self.query, default_non_null=False),
            mutation=self.mapper.map(self.mutation, default_non_null=False)
        )
