import graphql

from dataclasses import dataclass
from functools import partial

from .registry import TypeRegistry
from .mapper import MAPPER


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

    def _map_field(self, fn):
        return field_from_fn(fn)  

    def _map_fields(self):
        return {n: field_from_fn(fn) for (n, fn) in self.fields.items()}

    def _map_interfaces(self):
        return []


@MAPPER.add_mapper
def map_custom_type(mapper, obj):
    if isinstance(obj, CustomType):
        return graphql.GraphQLObjectType(
            name=obj.name,
            fields=partial(mapper, obj._map_fields),
            interfaces=partial(mapper, obj._map_interfaces),
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
            query=self.mapper.map(self.query),
            mutation=self.mapper.map(self.mutation)
        )
    